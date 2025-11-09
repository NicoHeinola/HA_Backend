#!/usr/bin/env python3
"""
Local Speech-to-Text Helper using Vosk
Provides offline speech recognition without internet connection
"""

import logging
import os
import sys
import pyaudio
from vosk import Model, KaldiRecognizer

logger = logging.getLogger(__name__)


class VoskSpeechToTextHelper:
    """
    Local speech-to-text recognition using Vosk
    - Fully offline (no internet required)
    - Low latency
    - Supports multiple languages
    """

    def __init__(self, model_path: str):
        """
        Initialize the speech-to-text helper

        Args:
            model_path: Path to Vosk model directory. Can also be a name of a pre-downloaded model in the "models/audio/vosk/" directory
        """
        if not os.path.exists(model_path):
            model_path = os.path.join(os.path.dirname(__file__), "..", "..", "models", "audio", "vosk", model_path)

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Vosk model not found at {model_path}\n"
                f"Download models from: https://alphacephei.com/vosk/models\n"
                f"Extract to: models/audio/vosk/"
            )

        self._model = Model(model_path)
        self._recognizer = KaldiRecognizer(self._model, 16000)

    def listen_and_transcribe(self, duration_seconds: int = 0) -> str:
        """
        Listen to microphone input and transcribe speech to text

        Args:
            duration_seconds: Duration to listen in seconds. 0 means listen until something is detected.
        """

        mic: pyaudio.PyAudio = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream()

        elapsed_time = 0
        start_time = os.times()[4]

        logger.debug("Listening for speech...")
        result = ""
        while (elapsed_time < duration_seconds and duration_seconds > 0) or (duration_seconds == 0 and result == ""):
            data = stream.read(4096, exception_on_overflow=False)

            if len(data) == 0:
                break

            if self._recognizer.AcceptWaveform(data):
                result = self._recognizer.Result()

            elapsed_time = os.times()[4] - start_time

        return result


def main():
    """Example usage"""

    try:
        stt = VoskSpeechToTextHelper("vosk-model-small-en-us-0.15")
        text = stt.listen_and_transcribe(duration_seconds=0)
        logger.debug(f"Transcribed Text: {text}")
    except FileNotFoundError as e:
        logger.error(e)


if __name__ == "__main__":
    main()
