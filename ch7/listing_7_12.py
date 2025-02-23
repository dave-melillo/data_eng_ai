import pandas as pd

# Example 1: Removing currency symbols
df_prices = pd.DataFrame({'price': ['$27.50', '$45.00', '$67.25']})
df_prices['price'] = df_prices['price'].str.replace('[\$,]', '', regex=True).astype(float)
print("Cleaned Prices:\n", df_prices)

# Example 2: Standardizing phone numbers
df_phones = pd.DataFrame({'phone': ['(123) 456-7890', '987-654-3210', '555 333 2222']})
df_phones['phone'] = df_phones['phone'].str.replace('[\(\)\-\s]', '', regex=True)
print("\nStandardized Phone Numbers:\n", df_phones)
