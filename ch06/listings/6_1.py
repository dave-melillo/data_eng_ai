import pandas as pd

# Create a sample DataFrame with inconsistent data
df = pd.DataFrame({
    'email': ['user1@example.com', 'user2@.com', '555-1234', 'user4@example.com'],  #A
    'age': [25, None, 30, 40],  #B
    'purchase_amount': [100.5, -50.0, None, 200.0]  #C
})

# Detect missing values in each column
missing_values = df.isnull().sum()  #D

# Detect negative values in the 'purchase_amount' column
negative_values = df[df['purchase_amount'] < 0]  #E

# Output the results
print("Missing Values:\n", missing_values)  #F
print("\nNegative Values:\n", negative_values)  #G
