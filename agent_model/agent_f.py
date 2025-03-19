import os
from langchain_google_genai import ChatGoogleGenerativeAI
import json

class HVACAssistant:
    def __init__(self, val=False):
        self.val = val
        # Retrieve the Google API key from environment variables
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")

        # Initialize the Gemini client
        self.model = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    temperature=0.1,
                    max_tokens=None,
                    timeout=None,
                    max_retries=2,
                )

        # Define the system prompt for the assistant
        self.prompt =   """
You are an AI assistant specialized in HVAC services. Your role is to assist customers in scheduling HVAC services by collecting essential information to ensure a seamless booking experience. 
DO NOT PROVIDE JSON FORMAT BEFORE USER CONFIRMATION. AFTER CONFIRMATION, PROVIDE JUST JSON FORMAT. YOU MUST ONLY HAVE OUTPUT FORMAT OF TEXT OR JSON. DO NOT ANSWER TO ANY IRRELEVANT QUESTIONS.

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

If the user confirms, provide the output **ONLY** in JSON format as follows:  

```json
{
    "Customer's Full Name": "",
    "Contact Information": {
        "Phone Number": "",
        "Email Address": ""
    },
    "Property Details": {
        "Type of Property": "",
        "Property Address": ""
    },
    "Service Required": "",
    "Issue Description": "",
    "Preferred Appointment": {
        "Date": "",
        "Time": ""
    },
    "Additional Notes or Special Requests": ""
} ```
"""

    def get_response(self, user_input):
        try:
            # Format the prompt with the user's input
            messages = [
                ("system", self.prompt),
                ("human", user_input),
            ]

            # Get the assistant's response from the model
            response = self.model.invoke(messages)
            response_content = response.content.strip()

            # Check if the response contains JSON content enclosed within triple backticks
            if "```json" in response_content and "```" in response_content:
                # Extract the JSON content between the triple backticks
                start_index = response_content.find("```json") + len("```json")
                end_index = response_content.rfind("```")
                json_content = response_content[start_index:end_index].strip()

                try:
                    # Parse the JSON content
                    booking_data = json.loads(json_content)
                    # Define the path to save the JSON file
                    json_file_path = '/home/m_khanch/Milad/Code/Agent/booked/hvac_booking.json'
                    # Save the parsed JSON data to a file
                    with open(json_file_path, 'w') as json_file:
                        json.dump(booking_data, json_file, indent=4)
                    return f"Booking is Completed." if not self.val else json_content
                except json.JSONDecodeError as e:
                    return f"Failed to parse JSON content: {e}"
            else:
                return response_content

        except Exception as e:
            return f"An error occurred: {e}"


# Example usage:
if __name__ == "__main__":
    assistant = HVACAssistant()
    user_question = "What do you like?"
    response = assistant.get_response(user_question)
    print(response)
