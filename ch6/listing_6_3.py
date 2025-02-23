import pandas as pd

# Create a sample DataFrame
df = pd.DataFrame({
    'customer_id': [1, 2, 2, 3, 3],  #A
    'preferred_store_location': ['NY', 'CA', 'CA', 'TX', None],  #B
    'purchase_amount': [200, 300, 300, 400, 400],  #C
    'optional_note': [None, None, None, None, None]  #D
})

# Remove duplicate rows
df = df.drop_duplicates()  #E

# Remove columns that are mostly null
threshold = 0.5 * len(df)  #F
df = df.loc[:, df.isnull().sum() <= threshold]  #G

# Output the cleaned DataFrame
print(df)  #H
