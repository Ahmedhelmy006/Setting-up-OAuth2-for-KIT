import json
import csv

# Load the JSON data from the file
with open('subscribers.json', 'r') as json_file:
    data = json.load(json_file)  # `data` is a list of dictionaries

# Open a CSV file for writing
with open('subscribers.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Define the header fields
    header = [
        "id", "first_name", "email_address", "state", "created_at",
        "fields_ai_finance_club", "fields_career_path", "fields_chatgpt",
        "fields_chatgpt_marketing_opt_out", "fields_chatgpt_pdf",
        "fields_city", "fields_company", "fields_country_long",
        "fields_current_position", "fields_full_name"
    ]
    csv_writer.writerow(header)

    # Write rows for each subscriber
    for subscriber in data:
        row = [
            subscriber.get("id"),
            subscriber.get("first_name"),
            subscriber.get("email_address"),
            subscriber.get("state"),
            subscriber.get("created_at"),
            # Flatten fields
            subscriber.get("fields", {}).get("ai_finance_club"),
            subscriber.get("fields", {}).get("career_path"),
            subscriber.get("fields", {}).get("chatgpt"),
            subscriber.get("fields", {}).get("chatgpt_marketing_opt_out"),
            subscriber.get("fields", {}).get("chatgpt_pdf"),
            subscriber.get("fields", {}).get("city"),
            subscriber.get("fields", {}).get("company"),
            subscriber.get("fields", {}).get("country_long"),
            subscriber.get("fields", {}).get("current_position"),
            subscriber.get("fields", {}).get("full_name"),
        ]
        csv_writer.writerow(row)

print("Data has been successfully written to 'subscribers.csv'.")
