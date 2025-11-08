#!/usr/bin/env python3
"""
Home Assistant Voice Console
Type text to be sent to Jaakko 1 voice assistant via conversation service.
"""

import logging
import os
from dotenv import load_dotenv

from application.application import Application

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
