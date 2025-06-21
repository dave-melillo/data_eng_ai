import openai  #A
import os  #B
from dotenv import load_dotenv  #C
from pydantic import BaseModel  #D

load_dotenv()  #E
openai.api_key = os.getenv("OPENAI_API_KEY")  #F

# Sample data
customers = [
    {"name": "John Smith", "email": "john.smith@acmeco.com"},
    {"name": "Jane Smythe", "email": "jane@alpha.io"},
    {"name": "Johnny S.", "email": "johnny@acmeco.com"},
    {"name": "Bob Wilson", "email": "bob@beta.com"}
]

# Define a structured output model for entity resolution  #G
class EmailMatch(BaseModel):  #H
    name: str  #I
    email: str  #J
    confidence: float  #K
    reasoning: str  #L

# Define the system prompt with resolution instruction  #M
system_prompt = """
You are an entity resolution assistant. A new customer email has arrived: 'jonny_smith@acmeco.com'.
Compare it to the list of known customers. Identify the best match based on email similarity and name inference.
Provide the closest match with a confidence score (0 to 1) and explain your reasoning.
""".strip()  #N

# Format the full input payload  #O
user_message = {
    "incoming_email": "jonny_smith@acmeco.com",
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
if completion.choices[0].message.parsed:  #Y
    match = completion.choices[0].message.parsed.dict()  #Y

    # Format and Print  #Z
    print(f"Best match: {match['name']} ({match['email']})")
    print(f"Confidence: {match['confidence']:.2f}")
    print("Reasoning:")
    print(match['reasoning'])

#A–#C Import libraries for environment setup and OpenAI access.
#D–#L Define the structured response format using EmailMatch, a Pydantic model.
#M–#N Compose a system prompt that explains the matching task to the AI.
#O–#P Provide the incoming email and previously defined customer_data as the input.
#Q–#W Send the request to the OpenAI API with a defined response structure.
#X–#Z Parse and display the AI's output, including confidence and reasoning. 