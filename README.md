# MeloTTS Home Assistant Integration

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2023.6%2B-blue.svg)

The `melotts` integration for Home Assistant provides a Text-to-Speech (TTS) platform that interfaces with a [MeloTTS Docker API Server](https://github.com/timhagel/MeloTTS-Docker-API-Server) to generate high-quality speech in multiple languages. It supports MP3 audio output and allows customization of speech speed and speaker selection.

## Features

- Supports multiple languages: English (`en`), French (`fr`), Spanish (`es`), Chinese (`zh`), Japanese (`jp`), and Korean (`kr`).
- Customizable speech speed and speaker selection via service options.
- Configurable server host, port, and default speed through `configuration.yaml`.
- Returns MP3 audio compatible with Home Assistant's media players.
- Robust error handling with detailed logging for debugging.

## Requirements

- Home Assistant 2023.6 or later.
- A running instance of the [MeloTTS Docker API Server](https://github.com/timhagel/MeloTTS-Docker-API-Server) accessible via HTTP (default: `http://192.168.50.40:8888`).
- The `aiohttp` Python library (automatically installed by Home Assistant).

## Installation

1. **Download the Integration**:
   - Clone or download this repository to your Home Assistant configuration directory:
     ```bash
     git clone https://github.com/Sigfrodr/melotts-home-assistant.git
     ```
   - Copy the `custom_components/melotts` folder to your Home Assistant configuration directory (typically `/config/custom_components/`):
     ```bash
     cp -r melotts-home-assistant/custom_components/melotts /config/custom_components/
     ```

2. **Restart Home Assistant**:
   - Restart Home Assistant to load the integration:
     ```bash
     ha core restart
     ```
   - Alternatively, restart via the Home Assistant UI: **Settings > System > Restart**.

## Configuration

Add the `melotts` platform to your `configuration.yaml` file under the `tts` section. Below is an example configuration:

```yaml
tts:
  - platform: melotts
    host: 192.168.50.40
    port: 8888
    speed: 1.0
```

### Configuration Options

| Key       | Type   | Default          | Description                                      |
|-----------|--------|------------------|--------------------------------------------------|
| `host`    | String | `192.168.50.40`  | Hostname or IP address of the MeloTTS server.    |
| `port`    | Integer| `8888`           | Port of the MeloTTS server.                      |
| `speed`   | Float  | `1.0`            | Default speech speed (e.g., `0.5` for slower, `1.2` for faster). |

### Enabling Debug Logging

To troubleshoot issues, enable debug logging in `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    homeassistant.components.tts: debug
    custom_components.melotts: debug
```

## Usage

The `melotts` integration is used via the `tts.speak` service in Home Assistant. Below are example service calls.

### Example 1: French TTS
Generate French speech with the default speaker and speed:

```yaml
service: tts.speak
data:
  entity_id: tts.melotts
  message: "Bonjour, ceci est un test"
  language: "fr"
  media_player_entity_id: media_player.your_speaker
  options:
    speaker_id: "FR"
    speed: 1.0
```

### Example 2: English TTS
Generate English speech with a specific speaker and slower speed:

```yaml
service: tts.speak
data:
  entity_id: tts.melotts
  message: "Hello, this is a test"
  language: "en"
  media_player_entity_id: media_player.your_speaker
  options:
    speaker_id: "EN-BR"
    speed: 0.5
```

### Supported Languages and Speakers

| Language | Code | Default Speaker | Other Speakers          |
|----------|------|-----------------|-------------------------|
| English  | `en` | `EN-Default`    | `EN-US`, `EN-BR`, `EN_INDIA`, `EN-AU` |
| French   | `fr` | `FR`            | None                    |
| Spanish  | `es` | `ES`            | None                    |
| Chinese  | `zh` | `ZH`            | None                    |
| Japanese | `jp` | `JP`            | None                    |
| Korean   | `kr` | `KR`            | None                    |

### Service Options

| Option       | Type   | Default            | Description                                      |
|--------------|--------|--------------------|--------------------------------------------------|
| `speaker_id` | String | Language-dependent | Speaker ID (e.g., `FR`, `EN-Default`, `EN-BR`).  |
| `speed`      | Float  | Configured speed   | Speech speed (e.g., `0.5` for slower, `1.2` for faster). |

## Troubleshooting

- **HTTP 500 Errors**:
  - Ensure the MeloTTS server is running and accessible at the configured `host` and `port`.
  - Check the server logs (`docker logs <container_name>`) for errors.
  - Verify that the payload includes `text`, `language`, `speaker_id`, and `speed`.

- **No Audio Played**:
  - Confirm that your media player supports MP3 audio.
  - Check Home Assistant logs for errors related to `tts.melotts`.
  - Test the server directly with `curl`:
    ```bash
    curl -H "Content-Type: application/json" -d '{"text": "bonjour", "language": "FR", "speaker_id": "FR", "speed": "1.0"}' http://192.168.50.40:8888/convert/tts --output "example.mp3"
    ```

- **Invalid Language**:
  - Ensure the `language` specified is one of `en`, `fr`, `es`, `zh`, `jp`, or `kr`.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Please include tests and update documentation as needed.

## License

This integration is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Built with inspiration from the [MeloTTS Docker API Server](https://github.com/timhagel/MeloTTS-Docker-API-Server) and [myshell-ai/MeloTTS](https://github.com/myshell-ai/MeloTTS).
- Thanks to the Home Assistant community for their support and documentation.
