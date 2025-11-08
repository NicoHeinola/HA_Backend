#!/usr/bin/env python3
"""
Home Assistant Voice Console
Type text to be sent to Jaakko 1 voice assistant via conversation service.
"""

import logging
import os
from dotenv import load_dotenv

from application.application import Application
from home_assistant_api.text_to_speech.text_to_speech_api import HATextToSpeechAPI
from home_assistant_api.wiz.wiz_lights_api import HAWizLightsAPI

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

# Configuration
HA_URL = os.getenv("HA_URL", "")
HA_TOKEN = os.getenv("HA_TOKEN", "")
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST", "")
WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT", ""))

TEXT_TO_SPEECH_VOICE_ENGINE_ID = os.getenv("TEXT_TO_SPEECH_VOICE_ENGINE_ID", "")


def main():
    application: Application = Application(HA_URL, HA_TOKEN, WEB_SERVER_HOST, WEB_SERVER_PORT)
    application.run()


if __name__ == "__main__":
    main()
