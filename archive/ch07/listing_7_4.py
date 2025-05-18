import pandas as pd
from ai_handle_missing_values import handle_missing_values

df_static = pd.DataFrame({'value': [10, None, 30, None, 50]})  #A
df_static = handle_missing_values(df_static, 'value', method="static")  #B

print("\nStatic Value Imputation:\n", df_static)  #C
