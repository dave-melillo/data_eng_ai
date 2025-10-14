import requests
import pandas as pd
import logging
import time

# Set up logging
logging.basicConfig(filename='api_requests.log', level=logging.INFO)

def fetch_number_facts(numbers):
    data = []
    for num in numbers:
        attempts = 0
        success = False
        while attempts < 3 and not success:
            try:
                response = requests.get(f"http://numbersapi.com/{num}?json", timeout=10)
                if response.status_code == 200:
                    fact = response.json().get('text', 'No fact available')
                    data.append({'Number': num, 'Fact': fact})
                    logging.info(f"Successfully retrieved fact for {num}")
                    success = True
                else:
                    logging.error(f"Failed to retrieve fact for {num}, Status: {response.status_code}")
                    attempts += 1
                    time.sleep(5)
            except requests.exceptions.Timeout:
                attempts += 1
                logging.warning(f"Timeout error while fetching fact for {num}, attempt {attempts}")
                time.sleep(5)
            except Exception as e:
                logging.error(f"Error fetching fact for {num}: {str(e)}")
                break
    
    return pd.DataFrame(data)

# Example usage
numbers = [42, 7, 100]
df = fetch_number_facts(numbers)
print(df)
