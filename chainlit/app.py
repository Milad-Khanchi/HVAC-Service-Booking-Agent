# app.py
import chainlit as cl
from agent.agent import HVACAssistant
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the HVACAssistant with the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable in your .env file.")

assistant = HVACAssistant(api_key=api_key)

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
    await message.reply(assistant_response)
