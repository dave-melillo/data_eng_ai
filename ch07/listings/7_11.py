import openai  #A
import os  #B
from dotenv import load_dotenv  #C
from pydantic import BaseModel  #D
from datetime import datetime  #E
import pandas as pd  #F

load_dotenv()  #G
openai.api_key = os.getenv("OPENAI_API_KEY")  #H

transactions = [
    {"account": "A001", "transaction_date": "2025-01-31T16:00:00Z", "terms": "NET30", "amount_due": 1200},
    {"account": "A001", "transaction_date": "2025-02-28T12:45:00Z", "terms": "NET60", "amount_due": 800},
    {"account": "A001", "transaction_date": "2025-03-15T09:30:00Z", "terms": "NET30", "amount_due": 1500},
    {"account": "A001", "transaction_date": "2025-06-01T11:00:00Z", "terms": "NET15", "amount_due": 950},
    {"account": "A001", "transaction_date": "2025-07-04T10:00:00Z", "terms": "NET30", "amount_due": 700},

    {"account": "A002", "transaction_date": "2025-01-10T14:00:00Z", "terms": "NET45", "amount_due": 300},
    {"account": "A002", "transaction_date": "2025-02-12T08:30:00Z", "terms": "NET30", "amount_due": 600},
    {"account": "A002", "transaction_date": "2025-03-29T17:15:00Z", "terms": "NET60", "amount_due": 1100},
    {"account": "A002", "transaction_date": "2025-04-20T13:00:00Z", "terms": "NET30", "amount_due": 950},
    {"account": "A002", "transaction_date": "2025-06-15T07:00:00Z", "terms": "NET30", "amount_due": 800},

    {"account": "A003", "transaction_date": "2025-03-01T18:30:00Z", "terms": "NET30", "amount_due": 400},
    {"account": "A003", "transaction_date": "2025-04-01T09:00:00Z", "terms": "NET90", "amount_due": 2500},
    {"account": "A003", "transaction_date": "2025-05-15T11:30:00Z", "terms": "NET30", "amount_due": 600},
    {"account": "A003", "transaction_date": "2025-07-01T08:00:00Z", "terms": "NET60", "amount_due": 1000},
    {"account": "A003", "transaction_date": "2025-08-05T16:45:00Z", "terms": "NET30", "amount_due": 750},

    {"account": "A004", "transaction_date": "2025-02-20T15:00:00Z", "terms": "NET15", "amount_due": 900},
    {"account": "A004", "transaction_date": "2025-03-15T10:45:00Z", "terms": "NET30", "amount_due": 850},
    {"account": "A004", "transaction_date": "2025-04-10T14:15:00Z", "terms": "NET45", "amount_due": 1200},
    {"account": "A004", "transaction_date": "2025-06-30T09:00:00Z", "terms": "NET30", "amount_due": 1000},
    {"account": "A004", "transaction_date": "2025-09-01T13:20:00Z", "terms": "NET60", "amount_due": 1300}
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
        results.append(completion.choices[0].message.parsed.dict())  #AN
    except Exception as e:  #AO
        print(f"Error: {e}")  #AP

# Final result as DataFrame  #AQ
final_df = pd.DataFrame(results)  #AR
display(final_df)  #AS
