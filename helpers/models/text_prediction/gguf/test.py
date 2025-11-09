import json
from llama_cpp import CreateCompletionResponse, Llama
import re


# Load your local .gguf model with GPU acceleration
llm = Llama(
    model_path="models/llm/gguf/Phi-3-mini-4k-instruct-q4.gguf",
    n_ctx=2048,
    n_gpu_layers=-1,  # offload all layers
    n_threads=1,  # only used for tokenization
    offload_kv=True,  # move KV cache to GPU
    use_mlock=False,
    verbose=False,
)

print(f"Model loaded successfully!")
print(f"Model meta: {llm.metadata}")

system_prompt = """Pick the best fitting action
ACTIONS:
- turn off the lights
- turn on the lights

Respond strictly in JSON:
{
  "action": "<ACTION>",
  "params": {}
}
"""

user_input = "Hey! Turn off the lights!"

prompt = f"{system_prompt}\nUser: {user_input}\nAssistant:"

output = llm(prompt, max_tokens=128, temperature=0.0)

# Print the model's full raw text
if isinstance(output, dict):
    choices: list = output.get("choices", [])
    raw_text = choices[0].get("text")
    print("RAW:", raw_text)

    # Extract JSON from the response
    try:
        # Try multiple patterns to find JSON
        json_match: re.Match[str] | None = re.search(r"```json\s*(.*?)\s*```", raw_text, re.DOTALL)

        if not json_match:
            # Try to find JSON object directly
            json_match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", raw_text, re.DOTALL)

        print("JSON MATCH:", json_match)

        if json_match:
            json_str = json_match.group(0).strip()
            parsed_json = json.loads(json_str)
            print("PARSED JSON:", json.dumps(parsed_json, indent=2))
        else:
            print("No JSON found in response")
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON - {e}")
