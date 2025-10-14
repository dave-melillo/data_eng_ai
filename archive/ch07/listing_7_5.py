import pandas as pd
from ai_handle_missing_values import handle_missing_values

df_increment = pd.DataFrame({'value': [10, None, 30, None, 50]})  #A
df_increment = handle_missing_values(df_increment, 'value', method="increment")  #B

print("\nIncremental Imputation:\n", df_increment)  #C
