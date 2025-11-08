#!/usr/bin/env python3
"""
Home Assistant Voice Console
Type text to be sent to Jaakko 1 voice assistant via conversation service.
"""

import logging
import os
from dotenv import load_dotenv

from home_assistant_api.text_to_speech.text_to_speech_api import HATextToSpeechAPI
from home_assistant_api.wiz.wiz_lights_api import HAWizLightsAPI

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

# Configuration
HA_URL = os.getenv("HA_URL", "")
HA_TOKEN = os.getenv("HA_TOKEN", "")
TEXT_TO_SPEECH_VOICE_ENGINE_ID = os.getenv("TEXT_TO_SPEECH_VOICE_ENGINE_ID", "")


def main():
    logging.info("Starting Home Assistant")

    # text_to_speech_api: HATextToSpeechAPI = HATextToSpeechAPI(HA_URL, HA_TOKEN)
    # text_to_speech_api.speak(TEXT_TO_SPEECH_VOICE_ENGINE_ID, "Working Text-to-Speech integration.")

    wiz_lights_api: HAWizLightsAPI = HAWizLightsAPI(HA_URL, HA_TOKEN)
    success = wiz_lights_api.turn_on("wiz_lamp_workstation_1")
    logging.info(f"Wiz light turn off successful: {success}")

    # Get light state
    state = wiz_lights_api.get_light_state("wiz_lamp_workstation_1")
    logging.info(f"Wiz light state: {state}")


if __name__ == "__main__":
    main()
