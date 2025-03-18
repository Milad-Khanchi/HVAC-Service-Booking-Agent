# import os
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
# from langchain.chains import LLMChain
#
# # Set your OpenAI API key
# openai_api_key = os.getenv("OPENAI_API_KEY")
# if not openai_api_key:
#     raise ValueError("Please set the OPENAI_API_KEY environment variable.")
#
# def main():
#     # Define the prompt template
#     template = """You are an AI assistant specialized in HVAC services. Answer the following question:
#
#     {question}
#     """
#     prompt = ChatPromptTemplate.from_template(template)
#
#     # Initialize the OpenAI chat model
#     chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
#
#     # Create the LLMChain with the prompt
#     chain = LLMChain(llm=chat_model, prompt=prompt)
#
#     print("Welcome to the HVAC Service Assistant. Type 'exit' to quit.")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ['exit', 'quit']:
#             print("Goodbye!")
#             break
#         # Generate the response
#         response = chain.run({"question": user_input})
#         print(f"Assistant: {response.strip()}")
#
# if __name__ == "__main__":
#     main()
# model.py
import openai
import os

class HVACAssistant:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.model = "gpt-3.5-turbo"

    def get_response(self, messages):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            return f"An error occurred: {e}"
