from helpers.audio.vosk_speech_to_text_helper import VoskSpeechToTextHelper
from helpers.models.text_prediction.gguf.gguf_text_prediction_model import GGUFTextPredictionModel
from home_assistant_api.text_to_speech.text_to_speech_api import HATextToSpeechAPI
import logging
import os
from dotenv import load_dotenv

from application.application import Application

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

# Load environment variables
load_dotenv()

# Configuration
HA_URL = os.getenv("HA_URL", "")
HA_TOKEN = os.getenv("HA_TOKEN", "")
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST", "")
WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT", ""))
TEXT_TO_SPEECH_VOICE_ENGINE_ID = os.getenv("TEXT_TO_SPEECH_VOICE_ENGINE_ID", "")

model_name: str = "Phi-3-mini-4k-instruct-q4.gguf"
system_prompt: str = (
    "Be a helpful assistant. Everytime you answer, just answer, don't put weird | marks or <assistant>."
)
tts_api: HATextToSpeechAPI = HATextToSpeechAPI(ha_url=HA_URL, access_token=HA_TOKEN)
stt_api: VoskSpeechToTextHelper = VoskSpeechToTextHelper("vosk-model-small-en-us-0.15")


while True:
    user_input: str = input("Enter your prompt: ")

    # Listen to microphone and get user input
    logger.info("Listening for user input...")
    # user_input: str = stt_api.listen_and_transcribe()
    logger.info(f"User Input: {user_input}")

    model = GGUFTextPredictionModel(model_name=model_name, system_prompt=system_prompt)
    prediction = model.predict(user_input)

    logger.info("Prediction:")
    logger.info("-------")

    # Find the line with "Assistant:"
    for line in prediction.split("\n"):
        logger.info(line)
        tts_api.speak(engine_id=TEXT_TO_SPEECH_VOICE_ENGINE_ID, message=line, speed=1.1)
        break
    else:
        logger.warning("No assistant response found.")
    logger.info("-------")

    model = None  # Free up resources
