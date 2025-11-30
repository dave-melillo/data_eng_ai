import openai  #A
import os  #B
from dotenv import load_dotenv  #C
from pydantic import BaseModel  #D

load_dotenv()  #E
openai.api_key = os.getenv("OPENAI_API_KEY")  #F

customers = [
    {
        "name": "John Smith",
        "email": "john.smith@acme.com",
        "device_id": "ACME-JS-001",
        "ip_address": "192.168.10.10",
        "top_coding_language": "Python"
    },
    {
        "name": "Jonathan Smith",
        "email": "jon.smith@acmeco.com",
        "device_id": "ACME-JS-002",
        "ip_address": "192.168.10.11",
        "top_coding_language": "R"
    },
    {
        "name": "Jane Smyth",
        "email": "jane.smyth@acmeco.com",
        "device_id": "ACME-JANE-001",
        "ip_address": "192.168.10.12",
        "top_coding_language": "Python"
    }
]

incoming_activity = {
    "name": "Johnny Smith",
    "email": "js.dev123@gmail.com",
    "device_id": "HOME-XYZ-999",  
    "ip_address": "10.0.0.55",     
    "top_coding_language": "Python"
}

# Define a structured output model for entity resolution  #G
class EmailMatch(BaseModel):  #H
    name: str  #I
    email: str  #J
    confidence: float  #K
    reasoning: str  #L

# Define the system prompt with resolution instruction  #M
system_prompt = """
You are an entity resolution assistant for a developer productivity platform.
A new activity record has arrived, and you must determine which known customer it most likely belongs to.
Use all available information: name, email, device_id, IP address, and top coding language.
Compare this incoming activity to the list of known customers. Identify the best match, and return:
- The matched customer's name and email
- A confidence score from 0 to 1
- A short explanation of your reasoning, including which features contributed most to the match
""".strip()  #N

# Format the full input payload  #O
user_message = {
    "incoming_activity": incoming_activity,
    "customers": customers
}  #P

# Call the OpenAI API with schema enforcement  #Q
completion = openai.beta.chat.completions.parse(  #R
    model="gpt-4o",  #S
    messages=[  #T
        {"role": "system", "content": system_prompt},  #U
        {"role": "user", "content": f"{user_message}"}  #V
    ],
    response_format=EmailMatch  #W
)

# Extract and display the structured response  #X
match = completion.choices[0].message.parsed.dict()  #Y

# Format and Print  #Z
print(f"Best match: {match['name']} ({match['email']})")
print(f"Confidence: {match['confidence']:.2f}")
print("Reasoning:")
print(match['reasoning']) 