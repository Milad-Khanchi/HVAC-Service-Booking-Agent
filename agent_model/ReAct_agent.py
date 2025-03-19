import os
from langchain_google_genai import ChatGoogleGenerativeAI
import json
from langchain.agents import AgentType, initialize_agent
from tools.tools import JsonTool, CalendarTool, AvailableSlotsTool



class HVACAssistant:
    def __init__(self, val=False):
        self.val = val
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")

        self.model = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    temperature=0.1,
                    max_tokens=None,
                    timeout=None,
                    max_retries=2,
                )

        self.prompt =   """
            You are an AI AGENT specialized in HVAC services. Your role is to assist customers in scheduling HVAC services by collecting essential information to ensure a seamless booking experience. 
            DO NOT PROVIDE JSON FORMAT BEFORE USER CONFIRMATION. AFTER CONFIRMATION, PROVIDE JUST JSON FORMAT. YOU MUST ONLY HAVE OUTPUT FORMAT OF TEXT OR JSON. 
	        DO NOT ANSWER TO ANY IRRELEVANT QUESTIONS.
	        At the beginning show the available slots to the user and ask for the preferred date and time.
            
            You always follow this exact format for each step when you need to use a tool:
            Thought: [Your reasoning about which tool to use.]
            Action: Should be one of the given tools.
            Action Input: You pass it to the selected tool.
            Observation: [Your observation based on the tool output.] 
            Final Answer: [This is where user can see and answer based on. You need to provide a clear and concise list of the required information.]
            
            For example These are not a good Final Answer:
            "Final Answer: I have requested the remaining information from the user."
            "Final Answer: I have initiated the HVAC booking process for an air filter change and am awaiting the user's information."
            "Final Answer: Is all the information correct? (yes/no) (WITHOUT PROVIDING INFORMATION THAT YOU ARE ASKING FOR)" 
            
            YOU MUST PROVIDE WHAT INFORMATION DO YOU NEED ALWAYS.

            Good Final Answer:
            "Final Answer: I need your full name, contact information, property details, service required, issue description, preferred appointment date and time, and any additional notes or special requests."

		
            These are the information you need to gather and once pass to tools, key should be exactly these:

            1. **Customer's Full Name:**  
            2. **Contact Information:**  
               - Phone Number:  
               - Email Address:  
            3. **Property Details:**  
               - Type of Property (e.g., Residential - Apartment, Residential - House, Commercial - Office, Commercial - Retail Store, Industrial - Warehouse):  
               - Property Address:  
            4. **Service Required:**  
               - Specific HVAC Service Needed (e.g., AC Repair, Furnace Maintenance, HVAC Installation, Duct Cleaning, Thermostat Installation, Air Quality Assessment):  
            5. **Issue Description:**  
               - Detailed Description of the Problem or Service Request:  
            6. **Preferred Appointment:**  
               - Date:  
               - Time:  
            7. **Additional Notes or Special Requests:**  
            
            Once you have collected all the necessary information, confirm the appointment details with the user as follows:  
            "Please confirm the following details:  
            - Full Name: [Customer's Full Name]  
            - Phone Number: [Phone Number]  
            - Email Address: [Email Address]  
            - Property Type: [Type of Property]  
            - Property Address: [Property Address]  
            - Service Required: [Service Required]  
            - Issue Description: [Issue Description]  
            - Preferred Appointment Date: [Date]  
            - Preferred Appointment Time: [Time]  
            - Additional Notes: [Additional Notes or Special Requests] 
            Is all the information correct? (yes/no)" 
            
            DO NOT CONFIRM ANYTHING BEFORE GETTING USER CONFIRMATION.
            AFTER USER CONFIRMATION, GENERATE JSON FORMAT AND USE CORRECT TOOL TO SAVE BOOKING INFORMATION.
            ALSO CALL CALENDER TOOL TO SCHEDULE APPOINTMENT.
            """

        self.tools = [CalendarTool(), JsonTool(), AvailableSlotsTool()]
        self.agent = initialize_agent(
            self.tools,
            self.model,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            agent_kwargs={"prefix": self.prompt},  # Set the prefix here
        )

    def get_response(self, user_input):
        try:
            response = self.agent.run(user_input)
            response_content = response.strip()
            try:
                return response_content
            except json.JSONDecodeError as e:
                return f"Failed to parse JSON content: {e}"


        except Exception as e:
            return f"An error occurred: {e}"



if __name__ == "__main__":
    assistant = HVACAssistant()
    user_question = "I need to schedule an AC repair for tomorrow at 2 PM."
    response = assistant.get_response(user_question)
    print(response)