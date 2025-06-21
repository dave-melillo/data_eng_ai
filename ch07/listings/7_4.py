import openai  #A
import os  #B
from dotenv import load_dotenv  #C
from pydantic import BaseModel  #D
import pandas as pd  #E

load_dotenv()  #F
openai.api_key = os.getenv("OPENAI_API_KEY")  #G

# Sample JSON data structure
json_data = {
    "library": {
        "name": "Central Library",
        "location": "Downtown",
        "books": [
            {
                "title": "Python Programming",
                "author": {
                    "first_name": "John",
                    "last_name": "Smith"
                },
                "genres": ["Programming", "Technology"],
                "published_year": 2023
            },
            {
                "title": "Data Science Handbook",
                "author": {
                    "first_name": "Jane",
                    "last_name": "Doe"
                },
                "genres": ["Data Science", "Analytics"],
                "published_year": 2022
            }
        ]
    }
}

class LibraryBook(BaseModel):  #H
    library_name: str  #I
    location: str  #J
    title: str  #K
    author: str  #L
    genres: str  #M
    published_year: int  #N

system_prompt = f"Extract data to match this class:\n{LibraryBook.schema_json(indent=2)}"  #O

structured_data = []  #P

for book in json_data["library"]["books"]:  #Q
    payload = {  #R
        "library_name": json_data["library"]["name"],  #S
        "location": json_data["library"]["location"],  #T
        **book  #U
    }

    try:  #V
        completion = openai.beta.chat.completions.parse(  #W
            model="gpt-4o",  #X
            messages=[  #Y
                {"role": "system", "content": system_prompt},  #Z
                {"role": "user", "content": f"{payload}"}  #AA
            ],
            response_format=LibraryBook  #AB
        )
        if completion.choices[0].message.parsed:  #AC
            structured_data.append(completion.choices[0].message.parsed.dict())  #AC
    except Exception as e:  #AD
        print(f"Error: {e}")  #AE

df = pd.DataFrame(structured_data)  #AF
print(df)  #AG

#A–#E Import required libraries for OpenAI access, environment loading, data modeling, and tabular display.
#F–#G Load the OpenAI API key from a local .env file to securely authenticate the request.
#H–#N Define the target data structure (LibraryBook) using Pydantic, which will serve as the AI response format.
#O Create a dynamic prompt by extracting the class schema using Pydantic's built-in JSON formatter.
#P Initialize an empty list to hold the structured outputs returned by the AI.
#Q–#U Loop through each book entry and dynamically attach the shared context (`library_name`, `location`) without hardcoding.
#V–#W Use OpenAI's structured output API to generate a response from the AI based on the prompt and combined payload.
#X–#Y Set up the conversation using system and user messages, defining intent and data input.
#Z–#AA Pass the schema definition and single enriched book entry as the full input.
#AB Specify the expected response format using the LibraryBook class.
#AC–#AE Parse and append the AI's structured response, handling any errors that occur during the process.
#AF–#AG Convert the list of structured dictionaries into a DataFrame and display the result. 