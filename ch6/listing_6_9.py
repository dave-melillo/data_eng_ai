import pandas as pd

# Example 4: Concatenating columns
df_concat = pd.DataFrame({'first_name': ['John', 'Jane'], 'last_name': ['Doe', 'Smith']})  #A
df_concat = chatgpt_transform_column(df_concat, 'first_name', "Concatenate this with 'last_name' into a full name.")  #B

# Output the result
print("\nConcatenated Names:\n", df_concat)  #C

#A Create a sample DataFrame with first and last names.
#B Use the chatgpt_transform_column function to concatenate into a full name.
#C Print the concatenated names DataFrame.
