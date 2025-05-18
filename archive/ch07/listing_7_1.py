import pandas as pd

# Create a sample DataFrame with missing sales data
df = pd.DataFrame({'daily_sales': [100, None, 300, None, 500]})  #A

# Fill missing values with the column's mean
df['daily_sales'].fillna(df['daily_sales'].mean(), inplace=True)  #B

# Output the updated DataFrame
print(df)  #C

#A Create a column representing daily sales, with some missing values (None).
#B Use fillna() to replace missing values with the column's mean.
#C Print the updated DataFrame, which now has no missing values.
