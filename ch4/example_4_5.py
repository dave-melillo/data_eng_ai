import re

text = """
Call me at (123) 456-7890 or 123-456-7890. You can also reach me at 123.456.7890 or +44 20 7946 0958. 
And my US number is +1 (123) 456-7890.
"""

# Regex pattern to match various phone number formats
phone_numbers = re.findall(r'\+?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{4}', text)

# Function to normalize phone numbers to a consistent format
def normalize_phone_number(number):
    cleaned_number = re.sub(r'[().\s]', '', number)
    
    if cleaned_number.startswith('+'):
        return re.sub(r'(\+\d{1,3})(\d{1,4})(\d{3,4})(\d{4})', r'\1-\2-\3-\4', cleaned_number)
    else:
        return re.sub(r'(\d{3})(\d{3})(\d{4})', r'+1-\1-\2-\3', cleaned_number)

# Normalize all phone numbers
normalized_numbers = [normalize_phone_number(num) for num in phone_numbers]
print(normalized_numbers)
