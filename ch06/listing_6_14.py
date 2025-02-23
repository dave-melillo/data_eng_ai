import pandas as pd

df_truncate = pd.DataFrame({'description': ['This is a long description', 'Short text', 'Another example']})  #A
df_truncate = chatgpt_transform_column(df_truncate, 'description', "Truncate this text to the first 10 characters.")  #B

print("\nTruncated Descriptions:\n", df_truncate)  #C

#A Create a sample DataFrame with long text descriptions.
#B Use the chatgpt_transform_column function to truncate text to the first 10 characters.
#C Print the truncated descriptions DataFrame.
