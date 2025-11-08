import logging
import requests
import subprocess
import tempfile
import os

from home_assistant_api.home_assistant_api import HomeAssistantAPI

logger = logging.getLogger(__name__)


class HATextToSpeechAPI(HomeAssistantAPI):
    """Home Assistant Text-to-Speech integration"""

    def __init__(self, ha_url: str, access_token: str):
        super().__init__(ha_url, access_token)

    def generate_tts_url(self, engine_id: str, message: str) -> requests.Response:
        """Get TTS URL from Home Assistant."""

        payload = {"engine_id": f"tts.{engine_id}", "message": message}
        headers = {
            **self._authorization_header,
            "Content-Type": "application/json",
        }

        response = requests.post(f"{self._ha_url}/api/tts_get_url", json=payload, headers=headers)
        return response

    def speak(self, engine_id: str, message: str) -> None:
        """Make Home Assistant speak a message using TTS."""

        tts_url_response: requests.Response = self.generate_tts_url(engine_id, message)
        tts_url_response.raise_for_status()

        voice_recording_file_url: str = tts_url_response.json().get("url", "")
        suffix: str = "." + voice_recording_file_url.split(".")[-1].split("?")[0]

        # Download the TTS audio file and play it
        audio_response = requests.get(voice_recording_file_url)
        audio_response.raise_for_status()

        # Play the audio using the system's default player
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp_file:
            tmp_file.write(audio_response.content)
            tmp_file_path = tmp_file.name

        try:
            print("Running audio!")
        finally:
            os.unlink(tmp_file_path)
