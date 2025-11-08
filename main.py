#!/usr/bin/env python3
"""
Home Assistant Voice Console
Type text to be sent to Jaakko 1 voice assistant via conversation service.
"""

import os
from dotenv import load_dotenv

from home_assistant_api.text_to_speech.text_to_speech import HATextToSpeechAPI

# Load environment variables
load_dotenv()

# Configuration
HA_URL = os.getenv("HA_URL", "")
HA_TOKEN = os.getenv("HA_TOKEN", "")


def main():
    print("Running Home Assistant Voice Console. Type your message and press Enter.")

    text_to_speech_api: HATextToSpeechAPI = HATextToSpeechAPI(HA_URL, HA_TOKEN)
    text_to_speech_api.speak("google_translate_en_com", "Working Text-to-Speech integration.")


if __name__ == "__main__":
    main()
