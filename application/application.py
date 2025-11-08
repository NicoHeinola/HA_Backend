import logging
from application.web_server import WebServer
from helpers.audio.vosk_speech_to_text_helper import VoskSpeechToTextHelper
from home_assistant_api.text_to_speech.text_to_speech_api import HATextToSpeechAPI


logger = logging.getLogger(__name__)


class Application:
    def __init__(self, ha_url: str, access_token: str, host: str, port: int):
        self._text_to_speech_api = HATextToSpeechAPI(ha_url, access_token)
        self._speech_to_text_helper: VoskSpeechToTextHelper = VoskSpeechToTextHelper("vosk-model-small-en-us-0.15")
        self._web_server: WebServer = WebServer(host=host, port=port)

    def run(self):
        logger.info("Starting Home Assistant")
        self._web_server.start()
