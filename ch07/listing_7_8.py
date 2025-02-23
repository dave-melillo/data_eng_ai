import pandas as pd

# Example 1: Normalizing ZIP codes
df_zip = pd.DataFrame({'zip_code': [1001, 40004, 502]})
df_zip['zip_code'] = df_zip['zip_code'].apply(lambda x: f"{x:05d}")
print("Normalized ZIP Codes:\n", df_zip)

# Example 2: Standardizing decimal places
df_prices = pd.DataFrame({'price': [12, 5.5, 7.89]})
df_prices['price'] = df_prices['price'].apply(lambda x: f"{x:.2f}")
print("\nNormalized Prices:\n", df_prices)

# Example 3: Converting units
df_units = pd.DataFrame({'height_in_inches': [65, 70, 72]})
df_units['height_in_cm'] = df_units['height_in_inches'] * 2.54
print("\nHeight in Centimeters:\n", df_units)
