import sys
import os
import json
import time
from dotenv import load_dotenv

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agent_model.ReAct_agent import HVACAssistant

load_dotenv()

def test_conversation(messages):
    assistant = HVACAssistant()
    chat_history = []

    for message in messages:
        time.sleep(2)
        role = message["role"]
        content = message["content"]

        chat_history.append({"role": role, "content": content})

        if role == "user":
            assistant_response = assistant.get_response(chat_history)
            chat_history.append({"role": "assistant", "content": assistant_response})
            print(f"{role}: {content}")
            print(f"assistant: {assistant_response}\n")

    return chat_history

def run_tests_from_json(json_file_path=os.getenv("CONVERSATION_PATH", "conversations.json")):
    with open(json_file_path, 'r') as file:
        conversations = json.load(file)

    for i, conversation in enumerate(conversations):
        print(f"--- Running Test Scenario {i + 1} ---")
        test_conversation(conversation)
        print("--- End of Test Scenario --- \n")
        time.sleep(2)

# Run tests from the JSON file
run_tests_from_json()
print("Done!")