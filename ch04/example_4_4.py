import pandas as pd

# Function to unnest JSON with handling for missing data
def unnest_json(data):
    rows = []
    for transaction in data['transactions']:
        for item in transaction['items']:
            if 'item_id' not in item:  # Skip items without an item_id
                continue
            price = item.get('price', 0)  # Default price to 0 if missing
            rows.append({
                'customer_id': data['customer_id'],
                'transaction_id': transaction['transaction_id'],
                'item_id': item['item_id'],
                'price': price
            })
    return pd.DataFrame(rows)

# Example usage
data = {
    "customer_id": 101,
    "transactions": [
        {
            "transaction_id": 1,
            "amount": 150,
            "items": [
                {"item_id": "A", "price": 50},
                {"item_id": "B"}  # Missing price
            ]
        },
        {
            "transaction_id": 2,
            "amount": 200,
            "items": [
                {"price": 200}  # Missing item_id
            ]
        }
    ]
}

# Generate the DataFrame
df = unnest_json(data)
print(df)
