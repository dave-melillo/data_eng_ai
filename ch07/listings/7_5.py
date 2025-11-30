import openai  #A
import os  #B
from dotenv import load_dotenv  #C
from pydantic import BaseModel  #D
import pandas as pd  #E

load_dotenv()  #F
openai.api_key = os.getenv("OPENAI_API_KEY")  #G

json_data = {
  "library": {
    "name": "City Library",
    "location": "Downtown",
    "books": [
      {
        "title": "Python Programming",
        "author": {
          "first_name": "John",
          "last_name": "Doe"
        },
        "genres": ["Programming", "Technology"],
        "published_year": 2020
      },
      {
        "title": "Data Science 101",
        "author": {
          "first_name": "Jane",
          "last_name": "Smith"
        },
        "genres": ["Data Science", "AI"],
        "published_year": 2019
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
        structured_data.append(completion.choices[0].message.parsed.dict())  #AC
    except Exception as e:  #AD
        print(f"Error: {e}")  #AE

df = pd.DataFrame(structured_data)  #AF
display(df)  #AG
