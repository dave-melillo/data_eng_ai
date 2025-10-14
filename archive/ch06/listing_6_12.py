import pandas as pd

df_dates = pd.DataFrame({'date': ['12/31/2023', '2023-01-01', '01-15-2023']})  #A
df_dates = chatgpt_transform_column(df_dates, 'date', "Standardize this date to YYYY-MM-DD.")  #B

print("Standardized Dates:\n", df_dates)  #C

#A Create a sample DataFrame with inconsistent date formats.
#B Use the chatgpt_transform_column function to standardize all dates to YYYY-MM-DD.
#C Print the standardized dates DataFrame.
