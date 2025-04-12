import pandas as pd
import re

# Process JSON with total order value filter
rows = []
for order in orders:
    if order['status'] != 'canceled':
        total_order_value = sum(
            product['price'] for product in order['products'] if 'price' in product and product['price'] is not None
        )
        if total_order_value < 100:  # Skip low-value orders
            continue
        
        for product in order['products']:
            if 'price' not in product or product['price'] is None:
                continue

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
