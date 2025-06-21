import openai  #A
import os  #B
from dotenv import load_dotenv  #C
from pydantic import BaseModel  #D
from typing import Optional  #E

# Load API key from .env file  #F
load_dotenv()  #G
openai.api_key = os.getenv("OPENAI_API_KEY")  #H

# Define the data model for extracted output  #I
class LogExtraction(BaseModel):  #J
    log_type: Optional[str]  #J.1
    date: Optional[str]  #K
    time: Optional[str]  #L

# Example log entries  #M
logs = [  #N
    "ERROR 2025-06-09 12:34:56 Server failed to respond",  #O
    "INFO 2025-06-09 12:35:56 User logged in",  #P
    "WARNING 2025-06-09 12:36:56 Disk space low"  #Q
]

# Prompt for AI to extract log_type, date, and time  #R
row_prompts = [  #S
    "You are a data extraction assistant. Extract the following from the log entry:\n"
    "- log_type: The type of log message (e.g., ERROR, INFO, WARNING)\n"
    "- date: Extract the date in YYYY-MM-DD format\n"
    "- time: Extract the time in HH:MM:SS format\n"
    "Return the result as a JSON object matching the LogExtraction structure."
    for log in logs  #T
]

# Process each log entry  #U
for log, prompt in zip(logs, row_prompts):  #V
    try:  #W
        # Make the API call  #X
        completion = openai.beta.chat.completions.parse(  #Y
            model="gpt-4o",  #Z
            messages=[  #AA
                {"role": "system", "content": prompt},  #AB
                {"role": "user", "content": log}  #AC
            ],  #AD
            response_format=LogExtraction  #AE
        )

        if completion.choices[0].message.parsed:  #AF
            extracted = completion.choices[0].message.parsed.dict()  #AG
            print(extracted)  #AH

    except Exception as e:  #AI
        print(f"Error processing log entry: {e}")  #AJ

#A–#E Import required libraries for environment loading, API access, and data modeling.
#F–#H Load the OpenAI API key securely using environment variables.
#I–#L Define a Pydantic model to structure the extracted fields: log type, date, and time.
#M–#Q Provide example log entries simulating different log levels and timestamps.
#R–#T Create individual prompts for each log entry instructing the AI to extract structured data.
#U–#AJ Iterate through each log and prompt pair, send them to the OpenAI API, and print the extracted results or handle errors gracefully. 