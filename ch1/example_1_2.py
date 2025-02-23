import pandas as pd

# Sample data
data = {'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, None, 30]}

df = pd.DataFrame(data)

# AI-assisted transformation: Fill missing values with the median age
df['age'].fillna(df['age'].median(), inplace=True)

# Print the transformed DataFrame
print(df)