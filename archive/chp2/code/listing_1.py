# Listing 1: Process Orders Based on Status
orders = [
    {
        'order_id': 1,
        'status': 'completed',
        'items': [{'product_id': 101, 'amount': 100}, {'product_id': 102, 'amount': 200}]
    },
    {
        'order_id': 2,
        'status': 'canceled',
        'items': [{'product_id': 103, 'amount': 150}]
    },
    {
        'order_id': 3,
        'status': 'pending',
        'items': [{'product_id': 104, 'amount': 250}, {'product_id': 105, 'amount': 350}]
    }
]

processed_orders = []
for order in orders:
    if order['status'] != 'canceled':
        for item in order['items']:
            if order['status'] == 'completed':
                item['amount'] *= 1.2
            elif order['status'] == 'pending':
                item['amount'] *= 1.1
        processed_orders.append(order)

print(processed_orders)
