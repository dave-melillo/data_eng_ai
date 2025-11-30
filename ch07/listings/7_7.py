import re  #A
from rapidfuzz import fuzz  #B

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

# Create a fingerprint by combining and normalizing key fields  #C
def build_fingerprint(record):  #D
    combined = f"{record['name']} {record['email']} {record['device_id']} {record['ip_address']} {record['top_coding_language']}"  #E
    normalized = re.sub(r'\W+', '', combined.lower())  #F
    return normalized  #G

# Build normalized fingerprints for the incoming activity and all customers  #H
incoming_fingerprint = build_fingerprint(incoming_activity)  #I
customer_candidates = [  #J
    {
        "original": customer,  #K
        "fingerprint": build_fingerprint(customer)  #L
    }
    for customer in customers  #M
]

# Score each candidate against the incoming fingerprint  #N
matches = [  #O
    {
        "name": c["original"]["name"],  #P
        "email": c["original"]["email"],  #Q
        "score": fuzz.token_sort_ratio(incoming_fingerprint, c["fingerprint"])  #R
    }
    for c in customer_candidates  #S
]

# Sort matches by score and print the best one  #T
top_match = sorted(matches, key=lambda m: m["score"], reverse=True)[0]  #U

print(f"Best match: {top_match['name']} ({top_match['email']}) - Score: {top_match['score']}")  #V
