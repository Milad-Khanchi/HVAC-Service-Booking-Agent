import os
import sys
import json
from dotenv import load_dotenv

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the HVACAssistant and conversation generator
from agent_model.agent_f import HVACAssistant
from data.sample_creator import generate_hvac_conversations

load_dotenv()

def test_hvac_assistant():
    # Initialize the HVAC assistant
    assistant = HVACAssistant(val=True)

    # Generate synthetic HVAC conversation data
    conversations = generate_hvac_conversations(num_conversations=2)  # Reduced to 2 for quicker testing

    # Iterate over each synthetic conversation scenario
    for i, convo in enumerate(conversations, start=1):
        print(f"\n--- Testing Scenario {i} ---")

        # Iterate through each message in the conversation (user/assistant turns)
        for exchange in convo:
            if exchange["role"] == "user":
                user_input = exchange["message"]
                print(f"User: {user_input}")

                # Get the assistant's response
                response = assistant.get_response(user_input)
                print(f"Assistant: {response}")

                # Check if the response is a valid JSON output (final confirmation)
                if response.startswith("{") and response.endswith("}"):
                    try:
                        parsed_json = json.loads(response)
                        print("✅ JSON output is valid and follows the expected structure.")
                    except json.JSONDecodeError:
                        print("❌ ERROR: JSON output is not formatted correctly.")

if __name__ == "__main__":
    test_hvac_assistant()
