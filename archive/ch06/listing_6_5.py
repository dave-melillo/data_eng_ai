import pandas as pd

df_dates = pd.DataFrame({'date': ['12/31/2023', '2023-01-01', '01-15-2023']})  #A
df_dates['date'] = pd.to_datetime(df_dates['date'], errors='coerce')  #B

df_skus = pd.DataFrame({'sku': ['abc123', 'XYZ789', '123ABC', 'a12bc3']})  #C
df_skus['sku'] = df_skus['sku'].str.upper().str.extract(r'([A-Z]{3}\d{3})', expand=False)  #D

df_truncate = pd.DataFrame({'description': ['This is a long description', 'Short text', 'Another example']})  #E
df_truncate['description'] = df_truncate['description'].str[:10]  #F

df_concat = pd.DataFrame({'first_name': ['John', 'Jane'], 'last_name': ['Doe', 'Smith']})  #G
df_concat['full_name'] = df_concat['first_name'] + ' ' + df_concat['last_name']  #H

df_tags = pd.DataFrame({'tags': ['ski shoes', 'running gear', 'snowboard boots']})  #I
tag_mapping = {'ski shoes': 'ski equipment', 'running gear': 'athletic equipment', 'snowboard boots': 'snowboard equipment'}  #J
df_tags['standardized_tags'] = df_tags['tags'].map(tag_mapping)  #K

print("Standardized Dates:\n", df_dates)
print("\nStandardized SKUs:\n", df_skus)
print("\nTruncated Descriptions:\n", df_truncate)
print("\nConcatenated Names:\n", df_concat)
print("\nStandardized Tags:\n", df_tags)
