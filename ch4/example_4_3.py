import pandas as pd

# Sample nested JSON data
data = {
    "customer_id": 101,
    "transactions": [
        {
            "transaction_id": 1,
            "amount": 150,
            "items": [
                {"item_id": "A", "price": 50},
                {"item_id": "B", "price": 100}
            ]
        },
        {
            "transaction_id": 2,
            "amount": 200,
            "items": [
                {"item_id": "C", "price": 200}
            ]
        }
    ]
}

# Unnest JSON data into a flat structure
rows = []
for transaction in data['transactions']:
    for item in transaction['items']:
        rows.append({
            'customer_id': data['customer_id'],
            'transaction_id': transaction['transaction_id'],
            'item_id': item['item_id'],
            'price': item['price']
        })

# Convert the flattened data into a pandas DataFrame
df = pd.DataFrame(rows)
print(df)
