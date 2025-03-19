from faker import Faker
import random
import json

def generate_hvac_conversations(num_conversations=15, filename='conversations.txt', json_filename='conversations.json'):
    """
    Generate structured HVAC service booking conversations for chatbot testing.

    Parameters:
    - num_conversations (int): Number of conversations to generate.
    - filename (str): Name of the text file for conversations.
    - json_filename (str): Name of the JSON file for structured conversations.

    Returns:
    - List of structured conversation scenarios.
    """
    fake = Faker()

    # Define HVAC service types
    services = [
        "AC Repair", "Furnace Maintenance", "HVAC Installation",
        "Duct Cleaning", "Thermostat Installation", "Air Quality Assessment"
    ]

    # Define property types
    properties = [
        "Residential - Apartment", "Residential - House", "Commercial - Office",
        "Commercial - Retail Store", "Industrial - Warehouse"
    ]

    # Define common issues
    issues = [
        "AC unit not cooling", "Furnace making unusual noises",
        "Installation of a new HVAC system", "Routine maintenance check",
        "Ducts need cleaning due to dust buildup", "Thermostat malfunctioning",
        "Interested in improving indoor air quality"
    ]

    # List to store conversation scenarios
    conversations = []

    for _ in range(num_conversations):
        customer_name = fake.name()
        phone = fake.phone_number()
        email = fake.email()
        property_type = random.choice(properties)
        service_needed = random.choice(services)
        issue_description = random.choice(issues)
        appointment_date = fake.date_this_month()
        appointment_time = fake.time()
        property_address = fake.address()
        additional_notes = "I dont have additional notes."

        # Generate a structured conversation simulating a full booking process
        conversation = [
            {"role": "user", "content": f"Hello, my name is {customer_name}. I need help with {service_needed} for my {property_type}."},
            {"role": "assistant", "content": f"Sure! Could you describe the issue you're experiencing?"},
            {"role": "user", "content": f"{issue_description}"},
            {"role": "assistant", "content": f"Thank you. I'll need your contact details. Please provide your phone number and email."},
            {"role": "user", "content": f"Phone: {phone}, Email: {email}"},
            {"role": "assistant", "content": f"Got it! Now, can you please provide your property address?"},
            {"role": "user", "content": f"My address is: {property_address}"},
            {"role": "assistant", "content": f"Thanks! What would be your preferred date and time for the appointment?"},
            {"role": "user", "content": f"Date: {appointment_date}, Time: {appointment_time}"},
            {"role": "assistant", "content": f"Do you have any additional notes or special requests?"},
            {"role": "user", "content": f"{additional_notes}"},
            {"role": "assistant", "content": f"Great! Here is a summary of your request:\n\n"
                                              f"1. **Customer's Full Name:** {customer_name}\n"
                                              f"2. **Contact Information:**\n"
                                              f"   - Phone Number: {phone}\n"
                                              f"   - Email Address: {email}\n"
                                              f"3. **Property Details:**\n"
                                              f"   - Type of Property: {property_type}\n"
                                              f"   - Property Address: {property_address}\n"
                                              f"4. **Service Required:** {service_needed}\n"
                                              f"5. **Issue Description:** {issue_description}\n"
                                              f"6. **Preferred Appointment:**\n"
                                              f"   - Date: {appointment_date}\n"
                                              f"   - Time: {appointment_time}\n"
                                              f"7. **Additional Notes:** {additional_notes}\n\n"
                                              f"Does this look correct?"},
            {"role": "user", "content": "Yes, that looks good."},
        ]

        conversations.append(conversation)

    # Write conversations to a text file
    with open(filename, 'w') as file:
        for i, convo in enumerate(conversations, start=1):
            file.write(f"Conversation Scenario {i}:\n")
            for exchange in convo:
                file.write(f"{exchange['role'].capitalize()}: {exchange['content']}\n")
            file.write("-" * 50 + "\n")

    # Write conversations to a JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(conversations, json_file, indent=4)

    print(f"{num_conversations} conversation scenarios have been written to '{filename}' and '{json_filename}'.")

    return conversations

# Example usage:
conversations = generate_hvac_conversations()
