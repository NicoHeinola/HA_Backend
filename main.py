#!/usr/bin/env python3
"""
Home Assistant Voice Console
Type text to be sent to Jaakko 1 voice assistant via conversation service.
"""

import logging
import os
from dotenv import load_dotenv

from home_assistant_api.text_to_speech.text_to_speech import HATextToSpeechAPI

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

    text_to_speech_api: HATextToSpeechAPI = HATextToSpeechAPI(HA_URL, HA_TOKEN)
    text_to_speech_api.speak(TEXT_TO_SPEECH_VOICE_ENGINE_ID, "Working Text-to-Speech integration.")


if __name__ == "__main__":
    main()
