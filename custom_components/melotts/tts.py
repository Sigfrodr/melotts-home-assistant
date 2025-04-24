"""MeloTTS platform for Home Assistant."""
import logging
import aiohttp
from homeassistant.components.tts import Provider
from homeassistant.core import HomeAssistant
from .const import CONF_HOST, CONF_PORT, CONF_SPEED, DEFAULT_HOST, DEFAULT_PORT, DEFAULT_SPEED

_LOGGER = logging.getLogger(__name__)

async def async_get_engine(hass: HomeAssistant, config, discovery_info=None):
    """Set up MeloTTS speech component."""
    host = config.get(CONF_HOST, DEFAULT_HOST)
    port = config.get(CONF_PORT, DEFAULT_PORT)
    speed = config.get(CONF_SPEED, DEFAULT_SPEED)
    return MeloTTSProvider(hass, host, port, speed)

class MeloTTSProvider(Provider):
    """The MeloTTS provider."""

    def __init__(self, hass: HomeAssistant, host: str, port: int, speed: float):
        """Initialize MeloTTS provider."""
        self.hass = hass
        self._host = host
        self._port = port
        self._speed = speed
        self.name = "MeloTTS"

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return ["en", "fr", "es", "zh", "jp", "kr"]

    @property
    def default_language(self):
        """Return the default language."""
        return "en"

    @property
    def supported_options(self):
        """Return list of supported options."""
        return ["speaker_id", "speed"]

    async def async_get_tts_audio(self, message: str, language: str, options: dict = None):
        """Generate audio from text using POST request."""
        try:
            url = f"http://{self._host}:{self._port}/convert/tts"
            headers = {"Content-Type": "application/json"}

            # Validate language
            if language.lower() not in self.supported_languages:
                _LOGGER.error("Unsupported language: %s. Supported: %s", language, self.supported_languages)
                return (None, None)

            # Convert language to uppercase (e.g., 'en' -> 'EN', 'fr' -> 'FR')
            language_code = language.upper()

            # Default speaker_id based on language
            default_speaker_id = "EN-Default" if language_code == "EN" else language_code
            speaker_id = options.get("speaker_id", default_speaker_id) if options else default_speaker_id

            # Validate speed
            try:
                speed = float(options.get("speed", self._speed)) if options else self._speed
            except (ValueError, TypeError):
                _LOGGER.error("Invalid speed value: %s. Using default: %s", options.get("speed"), self._speed)
                speed = self._speed

            payload = {
                "text": message,
                "language": language_code,  # Always uppercase (EN, FR, etc.)
                "speaker_id": speaker_id,
                "speed": str(speed)  # Server expects speed as a string
            }
            _LOGGER.debug("Sending TTS request: URL=%s, Payload=%s, Headers=%s", url, payload, headers)

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload, skip_auto_headers=["User-Agent"]) as response:
                    if response.status != 200:
                        response_text = await response.text()
                        _LOGGER.error("HTTP error %s: %s, Response: %s", response.status, response.reason, response_text)
                        return (None, None)

                    # Verify content type
                    content_type = response.headers.get("Content-Type", "")
                    _LOGGER.debug("Response Content-Type: %s", content_type)
                    if not any(fmt in content_type for fmt in ["audio/mpeg", "audio/mp3"]):
                        _LOGGER.error("Expected audio/mpeg, got %s", content_type)
                        return (None, None)

                    # Read audio data
                    audio_data = await response.read()
                    _LOGGER.debug("Received audio data: %s bytes", len(audio_data))
                    return ("mp3", audio_data)

        except aiohttp.ClientError as err:
            _LOGGER.error("Error generating TTS audio: %s", err)
            return (None, None)