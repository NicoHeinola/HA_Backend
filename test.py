import logging
import os
from time import sleep
from dotenv import load_dotenv
import json

from helpers.keyboard import keyboard_helper
from home_assistant_api.wiz import wiz_light_api

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

from helpers.audio.vosk_speech_to_text_helper import VoskSpeechToTextHelper
from helpers.models.text_prediction.gguf.gguf_text_prediction_model import GGUFTextPredictionModel
from home_assistant_api.text_to_speech.text_to_speech_api import HATextToSpeechAPI
from home_assistant_api.wiz.wiz_light_api import HAWizLightAPI
from helpers.keyboard.keyboard_helper import KeybboardHelper

# keyboard.press("w")  # Test keyboard import


# Load environment variables
load_dotenv()

# Configuration
HA_URL = os.getenv("HA_URL", "")
HA_TOKEN = os.getenv("HA_TOKEN", "")
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST", "")
WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT", ""))
TEXT_TO_SPEECH_VOICE_ENGINE_ID = os.getenv("TEXT_TO_SPEECH_VOICE_ENGINE_ID", "")

KEYBOARD_SERVER_HOST = os.getenv("KEYBOARD_SERVER_HOST", "")
KEYBOARD_SERVER_PORT = int(os.getenv("KEYBOARD_SERVER_PORT", ""))

model_name: str = "Phi-3-mini-4k-instruct-q4.gguf"

actions: list = [
    {
        "name": "lights.turn_off",
        "description": "Turns all lights off in the house",
        "params": {
            "entity_id": {
                "description": "Optional specific light entity ID to turn off",
                "allowed_values": [
                    "wiz_lamp_kitchen_1",
                    "wiz_lamp_bed_1",
                    "wiz_lamp_mirror_1",
                    "wiz_lamp_workstation_1",
                ],
            }
        },
    },
    {
        "name": "lights.turn_on",
        "description": "Turns all lights on in the house",
        "params": {
            "entity_id": {
                "description": "Optional specific light entity ID to turn on",
                "allowed_values": [
                    "wiz_lamp_kitchen_1",
                    "wiz_lamp_bed_1",
                    "wiz_lamp_mirror_1",
                    "wiz_lamp_workstation_1",
                ],
            }
        },
    },
    {
        "name": "keyboard.hold",
        "description": "Holds down a specific keyboard key on the user's computer. Useful for gaming or productivity tasks. Useful for car games.",
        "params": {
            "key": {
                "description": "The key to press. W for forward, A for left, S for backward, D for right, enter, space, ctrl",
                "allowed_values": ["w", "a", "s", "d", "enter", "space", "ctrl"],
            }
        },
    },
    {
        "name": "keyboard.press",
        "description": "Presses a specific keyboard key on the user's computer. Useful for car games.",
        "params": {
            "key": {
                "description": "The key to press. W for forward, A for left, S for backward, D for right, enter, space, ctrl",
                "allowed_values": ["w", "a", "s", "d", "enter", "space", "ctrl"],
            },
            "duration_seconds": {
                "description": "duration_seconds in seconds to hold the key down",
                "allowed_values": "any positive number",
            },
        },
    },
    {
        "name": "keyboard.release",
        "description": "Releases a specific keyboard key on the user's computer. Useful for car games.",
        "params": {
            "key": {
                "description": "The key to release. W for forward, A for left, S for backward, D for right, enter, space, ctrl",
                "allowed_values": ["w", "a", "s", "d", "enter", "space", "ctrl"],
            }
        },
    },
    {
        "name": "just_chatting",
        "description": "This action is used when the user is just chatting other actions don't fit. Be very friendly and engaging in your response. Don't ask the user for more information, just do as they say.",
        "params": {},
    },
]

system_prompt: str = (
    """
You are a helpful home assistant AI. Your job is to interpret user requests and map them to the best fitting action from the following list of available actions:

{actions_list}

For each user request, respond with a JSON object containing keys:
- "action": The name of the best matching action from the list above (or null if no match).
- "ai_answer": A creative, helpful, and friendly response confirming or explaining the action, e.g., "Sure thing! Turning off the lights now." or "Got it, all lights are off!"
- "params": An object containing any required parameters for the action (or empty object if none).
- "allowed_values" Sometimes user mistypes the entity_id, so please choose the closest matching entity_id from the allowed values.
- just_chatting action does not require any parameters. Put all your friendly responses in the "ai_answer" field.


Wrap the entire JSON response in a code block like ```json
{{
  "action": "lights.turn_off",
  "ai_answer": "Yes, I'll turn off the lights for you!",
  "params": {{
        "entity_id": "wiz_lamp_bed_1"
    }}
}}
```

When you think you are done. Remember to end code blocks with "```" and start code blocks with "```json". Remember to add "," after each key-value pair in the JSON object and ensure proper JSON formatting.
""".format(
        actions_list=json.dumps(actions, indent=2)
    )
)

tts_api: HATextToSpeechAPI = HATextToSpeechAPI(ha_url=HA_URL, access_token=HA_TOKEN)
ha_wiz_light_api: HAWizLightAPI = HAWizLightAPI(ha_url=HA_URL, access_token=HA_TOKEN)
keyboard_helper_api: KeybboardHelper = KeybboardHelper(host=KEYBOARD_SERVER_HOST, port=KEYBOARD_SERVER_PORT)

stt_api: VoskSpeechToTextHelper = VoskSpeechToTextHelper("vosk-model-small-en-us-0.15")

start_keyword: str = ""

while True:

    # Listen to microphone and get user input
    user_input: str = stt_api.listen_and_transcribe()
    if not user_input.lower().startswith(start_keyword.lower()):
        logger.info("Start keyword not detected in user input. Ignoring input. Input: " + user_input)
        continue

    # user_input: str = input("Enter your prompt: ")
    # user_input: str = "could you write me a very short poem"
    logger.info(f"User Input: {user_input}")

    model = GGUFTextPredictionModel(model_name=model_name, system_prompt=system_prompt, max_tokens=128 * 2)
    prediction = model.predict(user_input)

    # logger.info("Prediction:")
    # logger.info("-------")

    prediction = prediction.split("<!DONE!>")[0].split("!<DONE>")[0].strip().lower()

    # Remove everything before ```json
    if "```json" in prediction:
        prediction = prediction.split("```json", 1)[1].strip()

    # Remove everything after the closing ```
    if "```" in prediction:
        prediction = prediction.split("```", 1)[0].strip()

    logger.info(f"Prediction:\n------\n{prediction}\n------")

    # Try to convert prediction to JSON
    try:
        prediction_json = json.loads(prediction)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse prediction as JSON: {e}")
        prediction_json = {}

    action = prediction_json.get("action", None)
    answer = prediction_json.get("ai_answer", "Sorry, I don't quite understand.")
    params = prediction_json.get("params", {})

    print("Action:", action)

    all_lamps = ["wiz_lamp_kitchen_1", "wiz_lamp_bed_1", "wiz_lamp_mirror_1", "wiz_lamp_workstation_1"]

    if action == "lights.turn_off":
        entity_id = params.get("entity_id", None)
        print("Entity ID:", entity_id)
        if entity_id:
            logger.info(f"Turning off light: {entity_id}")
            ha_wiz_light_api.turn_off(entity_id=entity_id)
        else:
            logger.info("Turning off all lights")
            for lamp in all_lamps:
                ha_wiz_light_api.turn_off(entity_id=lamp)
    elif action == "lights.turn_on":
        entity_id = params.get("entity_id", None)
        if entity_id:
            logger.info(f"Turning on light: {entity_id}")
            ha_wiz_light_api.turn_on(entity_id=entity_id)
        else:
            logger.info("Turning on all lights")
            for lamp in all_lamps:
                ha_wiz_light_api.turn_on(entity_id=lamp)
    elif action == "keyboard.hold":
        key = params.get("key", None)
        if key:
            keyboard_helper_api.hold_key(key=key)
    elif action == "keyboard.press":
        key = params.get("key", None)
        if key:
            duration_seconds = params.get("duration_seconds", 0)
            keyboard_helper_api.press_key(key=key, duration_seconds=duration_seconds)
    elif action == "keyboard.release":
        key = params.get("key", None)
        if key:
            keyboard_helper_api.release_key(key=key)

    # tts_api.speak(engine_id=TEXT_TO_SPEECH_VOICE_ENGINE_ID, message=answer, speed=1.1)

    model = None  # Free up resources
    # break
