import requests
import pandas as pd
import logging

# Set up logging
logging.basicConfig(filename='api_requests.log', level=logging.INFO)

def fetch_number_facts(numbers):
    data = []
    for num in numbers:
        try:
            response = requests.get(f"http://numbersapi.com/{num}?json")
            if response.status_code == 200:
                fact = response.json().get('text', 'No fact available')
                data.append({'Number': num, 'Fact': fact})
                logging.info(f"Successfully retrieved fact for {num}")
            else:
                data.append({'Number': num, 'Fact': f"Error: Status {response.status_code}"})
                logging.error(f"Failed to retrieve fact for {num}, Status: {response.status_code}")
        except Exception as e:
            data.append({'Number': num, 'Fact': f"Error: {str(e)}"})
            logging.error(f"Error fetching fact for {num}: {str(e)}")
    
    return pd.DataFrame(data)

# Example usage
numbers = [42, 7, 100]
df = fetch_number_facts(numbers)
print(df)
