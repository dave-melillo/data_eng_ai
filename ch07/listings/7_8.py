import openai  #A
import os  #B
from dotenv import load_dotenv  #C
from pydantic import BaseModel  #D
from datetime import datetime  #E
import pandas as pd  #F

load_dotenv()  #G
openai.api_key = os.getenv("OPENAI_API_KEY")  #H

# Sample transaction data
transactions = [
    {
        "account": "ACME Corp",
        "transaction_date": "2024-03-15T10:30:00Z",
        "amount_due": 5000.00,
        "terms": "NET30"
    },
    {
        "account": "ACME Corp", 
        "transaction_date": "2024-04-22T14:15:00Z",
        "amount_due": 3500.00,
        "terms": "NET60"
    },
    {
        "account": "Beta Inc",
        "transaction_date": "2024-05-10T09:45:00Z", 
        "amount_due": 2000.00,
        "terms": "NET30"
    }
]

# Define response schema using Pydantic  #I
class TransformedTransaction(BaseModel):  #J
    account: str  #K
    transaction_date: str  #L
    date_only: str  #M
    timestamp_pst: str  #N
    timestamp_est: str  #O
    timestamp_gst: str  #P
    month: int  #Q
    year: int  #R
    fiscal_quarter: str  #S
    due_date: str  #T
    contribution_pct: float  #U

# Compute account totals for contribution_pct  #W
df = pd.DataFrame(transactions)  #X
account_totals = df.groupby("account")["amount_due"].sum().to_dict()  #Y

# Define system prompt template  #Z
system_prompt = f"""
You are a data transformation assistant. You will receive one transaction at a time and must return a single object matching this schema:
{TransformedTransaction.schema_json(indent=2)}

The transaction will contain:
- 'transaction_date': an ISO-8601 timestamp in UTC
- 'terms': in format like 'NET30', meaning due in 30 **business days**
- 'account': account name
- 'amount_due': numeric value in USD
- 'account_total': total balance due for the account (used for calculating percentage contribution)

For each transaction:
- Extract the date without time
- Convert the timestamp to PST, EST, and GST
- Extract the month and year
- Determine fiscal quarter using a custom calendar: Q1 = Feb-Apr, Q2 = May-Jul, Q3 = Aug-Oct, Q4 = Nov-Jan
- Calculate due date by adding the NET days as business days to the transaction date
- Calculate contribution percentage = (amount_due / account_total) * 100

Return a JSON object that matches the schema exactly.
""".strip()  #AA

# Collect results  #AB
results = []  #AC

for tx in transactions:  #AD
    payload = tx.copy()  #AE
    payload["account_total"] = account_totals[tx["account"]]  #AF

    try:  #AG
        completion = openai.beta.chat.completions.parse(  #AH
            model="gpt-4o",  #AI
            messages=[  #AJ
                {"role": "system", "content": system_prompt},  #AK
                {"role": "user", "content": f"{payload}"}  #AL
            ],
            response_format=TransformedTransaction  #AM
        )
        if completion.choices[0].message.parsed:  #AN
            results.append(completion.choices[0].message.parsed.dict())  #AN
    except Exception as e:  #AO
        print(f"Error: {e}")  #AP

# Final result as DataFrame  #AQ
final_df = pd.DataFrame(results)  #AR
print(final_df)  #AS

#A–#H: Import libs, load env, and set up OpenAI.
#I–#U: Define the response schema with Pydantic.
#W–#Y: Load data and compute account totals.
#Z–#AA: Craft system prompt with transformation rules.
#AB–#AC: Init result list.
#AD–#AF: Loop over transactions and attach totals.
#AG–#AP: Call API, parse response, handle errors.
#AQ–#AS: Convert results to DataFrame and display. 