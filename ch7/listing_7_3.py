import pandas as pd
from ai_handle_missing_values import handle_missing_values

df_avg = pd.DataFrame({'value': [10, None, 30, None, 50]})  #A
df_avg = handle_missing_values(df_avg, 'value', method="average")  #B

print("Average Imputation:\n", df_avg)  #C
