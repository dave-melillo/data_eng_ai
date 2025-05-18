import pandas as pd
import re

orders =  [{ "order_id": 1, "status": "completed", "products": [ {"description": "Nike Air Max - Red", "price": 120.00, "quantity": 1}, {"description": "Adidas Ultraboost - Black", "price": 150.00, "quantity": 2} ] }, { "order_id": 2, "status": "pending", "products": [ {"description": "Puma Speedcat - White", "price": 90.00, "quantity": 3} ] }, { "order_id": 3, "status": "canceled", "products": [ {"description": "Reebok Classic - Blue", "price": 100.00, "quantity": 1} ] } ]

# Process JSON
rows = []
for order in orders:
    if order['status'] != 'canceled':
        for product in order['products']:
            description = product['description']
            brand_match = re.search(r'^\w+', description)
            product_name_match = re.search(r'(?<=\s)\w[\w\s]+(?=\s-)', description)
            color_match = re.search(r'(?<=-\s)\w+$', description)

            tax_rate = 1.2 if order['status'] == 'completed' else 1.1
            rows.append({
                "order_id": order['order_id'],
                "status": order['status'],
                "product_name": product_name_match.group(0) if product_name_match else None,
                "brand": brand_match.group(0) if brand_match else None,
                "color": color_match.group(0) if color_match else None,
                "price": product['price'],
                "quantity": product['quantity'],
                "price_with_tax": round(product['price'] * tax_rate, 2)
            })

df = pd.DataFrame(rows)
print(df)
