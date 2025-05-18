import pandas as pd
from dateutil import parser  #A

# Create messy dataset from Bob's shop  #B
df = pd.DataFrame({  #C
    'purchase_date': ['12/31/2023', '2023-01-01', '01-15-2023'],  #D
    'sku': ['abc123', 'XYZ789', '123ABC'],  #E
    'product_description': ['red winter jacket - insulated and waterproof', 
                            'bindings - lightweight and durable',
                            'short snowboard - beginner friendly'],  #F
    'first_name': ['Ava', 'Leo', 'Riley'],  #G
    'last_name': ['Smith', 'Nguyen', 'Patel'],  #H
    'product_name': ['winter jacket', 'bindings', 'short snowboard']  #I
})

# Standardize purchase_date format to YYYY-MM-DD  #J
def normalize_date(val):  #K
    try:
        return parser.parse(val).strftime('%Y-%m-%d')  #L
    except Exception:
        return None  #M

df['purchase_date'] = df['purchase_date'].apply(normalize_date)  #N

# Enforce SKU format (3 uppercase letters + 3 digits)  #O
df['sku'] = df['sku'].str.upper().str.extract(r'([A-Z]{3}\d{3})', expand=False)  #P

# Truncate product_description to 20 characters  #Q
df['product_description'] = df['product_description'].str[:20]  #R

# Concatenate first and last names into full_name  #S
df['full_name'] = df['first_name'] + ' ' + df['last_name']  #T

# Map product_name to standardized categories  #U
category_map = {
    'winter jacket': 'outerwear',
    'bindings': 'gear',
    'short snowboard': 'boards'
}
df['product_category'] = df['product_name'].map(category_map)  #V

# Print cleaned DataFrame  #W
display(df)  #X
