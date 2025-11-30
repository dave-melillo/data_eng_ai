import pandas as pd  #A
from pandas.tseries.offsets import BDay  #B
import pytz  #C
from datetime import datetime  #D

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
display(df)