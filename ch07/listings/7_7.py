import pandas as pd  #A
from pandas.tseries.offsets import BDay  #B
import pytz  #C
from datetime import datetime  #D

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

# Load transaction data into a DataFrame  #E
df = pd.DataFrame(transactions)  #F
df["transaction_date"] = pd.to_datetime(df["transaction_date"], utc=True)  #G

# A: Plain date without time  #H
df["date_only"] = df["transaction_date"].dt.date  #I

# B–D: Timestamps converted to PST, EST, and GST respectively  #J
df["timestamp_pst"] = df["transaction_date"].dt.tz_convert("US/Pacific")  #K
df["timestamp_est"] = df["transaction_date"].dt.tz_convert("US/Eastern")  #L
df["timestamp_gst"] = df["transaction_date"].dt.tz_convert("Asia/Dubai")  #M

# E: Extracted month and year for reporting breakdowns  #N
df["month"] = df["transaction_date"].dt.month  #O
df["year"] = df["transaction_date"].dt.year  #P

# F: Custom fiscal quarter based on internal calendar (Q1 = Feb–Apr)  #Q
def get_fiscal_quarter(date):  #R
    fiscal_month = (date.month - 1) % 12 + 1  #S
    if fiscal_month in [2, 3, 4]: return "Q1"  #T
    elif fiscal_month in [5, 6, 7]: return "Q2"  #U
    elif fiscal_month in [8, 9, 10]: return "Q3"  #V
    else: return "Q4"  #W

df["fiscal_quarter"] = df["transaction_date"].apply(get_fiscal_quarter)  #X

# 2: Due date calculation using business days only  #Y
def get_due_date(row):  #Z
    term_days = int(row["terms"].replace("NET", ""))  #AA
    return row["transaction_date"] + BDay(term_days)  #AB

df["due_date"] = df.apply(get_due_date, axis=1)  #AC

# 3: Percent contribution of each transaction to its account's total balance  #AD
account_totals = df.groupby("account")["amount_due"].transform("sum")  #AE
df["contribution_pct"] = (df["amount_due"] / account_totals * 100).round(2)  #AF

# Display key columns for verification  #AG
print(df)  #AH

#A–#G: Import libraries, load data, and prepare datetime objects.
#H–#P: Extract a clean date, timezones (PST/EST/GST), and reporting breakdowns.
#Q–#X: Apply a custom fiscal quarter based on a 1-month offset.
#Y–#AC: Calculate business-day due dates based on NET terms.
#AD–#AF: Determine each transaction's share of the account's total balance.
#AG–#AH: Output essential transformation results for verification. 