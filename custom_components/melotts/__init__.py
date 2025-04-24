"""The MeloTTS integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MeloTTS from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    return True