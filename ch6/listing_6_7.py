df_skus = pd.DataFrame({'sku': ['abc123', 'XYZ789', '123ABC', 'a12bc3']})  #A
df_skus = chatgpt_transform_column(df_skus, 'sku', "Ensure SKU follows format: three uppercase letters + three digits.")  #B

print("\nStandardized SKUs:\n", df_skus)  #C
