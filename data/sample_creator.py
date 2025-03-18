from faker import Faker
import random

def generate_hvac_conversations(num_conversations=15, filename='conversations.txt'):
    """
    Generate a specified number of HVAC service booking conversation scenarios
    and write them to a text file.

    Parameters:
    - num_conversations (int): Number of conversation scenarios to generate.
    - filename (str): Name of the file to write the conversations to.

    Returns:
    - List of dictionaries containing the generated conversation scenarios.
    """
    fake = Faker()

    # Define HVAC service types
    services = [
        "AC Repair",
        "Furnace Maintenance",
        "HVAC Installation",
        "Duct Cleaning",
        "Thermostat Installation",
        "Air Quality Assessment"
    ]

    # Define property types
    properties = [
        "Residential - Apartment",
        "Residential - House",
        "Commercial - Office",
        "Commercial - Retail Store",
        "Industrial - Warehouse"
    ]

    # Define common issues or requests
    issues = [
        "AC unit not cooling",
        "Furnace making unusual noises",
        "Installation of a new HVAC system",
        "Routine maintenance check",
        "Ducts need cleaning due to dust buildup",
        "Thermostat malfunctioning",
        "Interested in improving indoor air quality"
    ]

    # List to store conversation scenarios
    conversations = []

    # Generate conversation scenarios
    for _ in range(num_conversations):
        conversation = {
            "Customer Name": fake.name(),
            "Contact Information": {
                "Phone": fake.phone_number(),
                "Email": fake.email()
            },
            "Property Type": random.choice(properties),
            "Service Needed": random.choice(services),
            "Issue Description": random.choice(issues),
            "Preferred Appointment": {
                "Date": fake.date_this_month(),
                "Time": fake.time()
            }
        }
        conversations.append(conversation)

    # Write conversations to a text file
    with open(filename, 'w') as file:
        for i, convo in enumerate(conversations, start=1):
            file.write(f"Conversation Scenario {i}:\n")
            file.write(f"Customer Name: {convo['Customer Name']}\n")
            file.write("Contact Information:\n")
            file.write(f"    Phone: {convo['Contact Information']['Phone']}\n")
            file.write(f"    Email: {convo['Contact Information']['Email']}\n")
            file.write(f"Property Type: {convo['Property Type']}\n")
            file.write(f"Service Needed: {convo['Service Needed']}\n")
            file.write(f"Issue Description: {convo['Issue Description']}\n")
            file.write("Preferred Appointment:\n")
            file.write(f"    Date: {convo['Preferred Appointment']['Date']}\n")
            file.write(f"    Time: {convo['Preferred Appointment']['Time']}\n")
            file.write("-" * 50 + "\n")

    print(f"{num_conversations} conversation scenarios have been written to '{filename}'.")

    return conversations

# Example usage:
conversations = generate_hvac_conversations()
print(conversations)