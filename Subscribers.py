from dotenv import load_dotenv
import os
import requests
import json

load_dotenv(dotenv_path="enviroment_variables.env")


API_KEY = os.getenv('KIT_V4_API_KEY')
BASE_URL = "https://api.kit.com/v4"

headers = {
  'Accept': 'application/json',
  'X-Kit-Api-Key': API_KEY
}
next_page_url = f'{BASE_URL}/subscribers'
all_subscribers = []
records_to_fetch = 100000
records_per_page = 500
total = 0

# Pagination loop
while next_page_url and total < records_to_fetch:
    # Make the API request with the updated URL
    r = requests.get(next_page_url, headers=headers)
    
    if r.status_code == 200:
        data = r.json()
        
        # Extract subscribers and add to the list
        subscribers = data.get('subscribers', [])
        all_subscribers.extend(subscribers)
        total += len(subscribers)
        
        # Handle pagination
        pagination = data.get('pagination', {})
        if pagination.get('has_next_page') and total < records_to_fetch:
            end_cursor = pagination.get('end_cursor')
            next_page_url = f'{BASE_URL}/subscribers?after={end_cursor}'
        else:
            next_page_url = None
    else:
        print(f"Failed to retrieve data. Status code: {r.status_code}")
        print(f"Error message: {r.text}")
        break

# Save the results to a JSON file
with open('subscribers.json', 'w') as json_file:
    json.dump(all_subscribers[:records_to_fetch], json_file, indent=4)

print(f"Successfully fetched {len(all_subscribers[:records_to_fetch])} subscribers.")