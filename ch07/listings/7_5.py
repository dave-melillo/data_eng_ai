import re  #A
from rapidfuzz import fuzz, process  #B

# Sample data
incoming_email = "jonny_smith@acmeco.com"
customers = [
    {"name": "John Smith", "email": "john.smith@acmeco.com"},
    {"name": "Jane Smythe", "email": "jane@alpha.io"},
    {"name": "Johnny S.", "email": "johnny@acmeco.com"},
    {"name": "Bob Wilson", "email": "bob@beta.com"}
]

# Normalize the email by removing special characters and lowercasing  #C
def normalize_email(email):  #D
    prefix = email.split('@')[0]  #E
    normalized = re.sub(r'\W+', '', prefix.lower())  #F
    return normalized  #G

# Normalize the incoming email and customer emails  #H
normalized_incoming = normalize_email(incoming_email)  #I
customer_candidates = [  #J
    {
        "original": customer,  #K
        "normalized": normalize_email(customer["email"])  #L
    }
    for customer in customers  #M
]

# Score similarity using fuzzy matching  #N
matches = [  #O
    {
        "name": c["original"]["name"],  #P
        "email": c["original"]["email"],  #Q
        "score": fuzz.ratio(normalized_incoming, c["normalized"])  #R
    }
    for c in customer_candidates  #S
]

# Sort and print top match  #T
top_match = sorted(matches, key=lambda m: m["score"], reverse=True)[0]  #U
print(f"Best match: {top_match['name']} ({top_match['email']}) - Score: {top_match['score']}")  #V

#A–#B Import libraries for regex and fuzzy string matching.
#C–#G Define a function to normalize email prefixes by removing special characters and lowercasing.
#H–#M Normalize the incoming email and all CRM customer email prefixes.
#N–#S Score each record's similarity to the incoming email using fuzzy string matching.
#T–#V Sort the matches by similarity score and print the top result. 