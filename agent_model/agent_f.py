import openai
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from dotenv import load_dotenv
import os

load_dotenv()

class HVACAssistant:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key
        self.model = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=self.api_key)
        self.prompt = """You are an AI assistant specialized in HVAC services. Answer the following question:
                      """
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", f"{self.prompt}"),
            ("user", "{question}")
        ])
        self.memory = ConversationSummaryMemory(llm=self.model, return_messages=True)

    def get_response(self, user_input):
        try:
            # Save the user input to memory
            self.memory.save_context({"input": user_input}, {})
            # Retrieve the current summary of the conversation
            summary = self.memory.load_memory_variables({})["history"]
            # Format the prompt with the current summary and user input
            messages = self.prompt_template.format_messages(question=user_input)
            # Add the summary to the system message
            messages.insert(0, {"role": "system", "content": f"Conversation summary:\n{summary}"})
            response = self.model(messages)
            # Save the assistant's response to memory
            self.memory.save_context({}, {"output": response.content.strip()})
            return response.content.strip()
        except Exception as e:
            return f"An error occurred: {e}"