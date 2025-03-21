import chainlit as cl
import sys
import os
from dotenv import load_dotenv

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agent_model.ReAct_agent import HVACAssistant

load_dotenv()
assistant = HVACAssistant()

@cl.on_chat_start
async def on_chat_start():
    # Initialize chat history in the user session
    cl.user_session.set('chat_history', [])
    await cl.Message(content="Hello! How can I assist you with HVAC services today?").send()

@cl.on_message
async def on_message(message: cl.Message):
    # Retrieve chat history from the user session
    chat_history = cl.user_session.get('chat_history', [])

    # Add the new user message to the chat history
    chat_history.append({"role": "user", "content": message.content})

    # Get the assistant's response
    assistant_response = assistant.get_response(chat_history)

    # Add the assistant's response to the chat history
    chat_history.append({"role": "assistant", "content": assistant_response})

    # Update the chat history in the user session
    cl.user_session.set('chat_history', chat_history)

    # Send the assistant's response to the user
    await cl.Message(content=assistant_response).send()
