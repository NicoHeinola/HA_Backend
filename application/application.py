import logging
from application.web_server import WebServer
from helpers.audio.vosk_speech_to_text_helper import VoskSpeechToTextHelper
from home_assistant_api.text_to_speech.text_to_speech_api import HATextToSpeechAPI
from home_assistant_api.wiz.wiz_light_api import HAWizLightAPI


logger = logging.getLogger(__name__)


class Action:
    # Light Actions
    TURN_LIGHT_OFF = "light.turn_off"
    TURN_LIGHT_ON = "light.turn_on"
    TOGGLE_LIGHT = "light.toggle"


class Application:
    def __init__(self, ha_url: str, access_token: str, host: str, port: int, *args, **kwargs):
        self._wiz_light_api = HAWizLightAPI(ha_url, access_token)
        self._text_to_speech_api = HATextToSpeechAPI(ha_url, access_token)
        self._speech_to_text_helper: VoskSpeechToTextHelper = VoskSpeechToTextHelper("vosk-model-small-en-us-0.15")

        self._web_server: WebServer = WebServer(host=host, port=port)
        self._web_server.register_event("action_triggered", self.on_action_triggered)

    def on_action_triggered(self, run_action: str, *args, **kwargs) -> None:
        logger.info(f"Action triggered: {run_action}")

        if run_action == Action.TURN_LIGHT_OFF:
            entity_id = kwargs.get("entity_id", "")
            self._wiz_light_api.turn_off(entity_id)
        elif run_action == Action.TURN_LIGHT_ON:
            entity_id = kwargs.get("entity_id", "")
            self._wiz_light_api.turn_on(entity_id)
        elif run_action == Action.TOGGLE_LIGHT:
            entity_id = kwargs.get("entity_id", "")
            self._wiz_light_api.toggle(entity_id)

    def run(self):
        logger.info("Starting Home Assistant")
        self._web_server.start()
