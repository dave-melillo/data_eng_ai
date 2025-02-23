import pandas as pd

# Sample data
data = {'temperature': [72, 85, 90, 78, 88],
        'humidity': [30, 50, 60, 40, 55]}

df = pd.DataFrame(data)

# AI-generated feature: Heat index (simplified formula)
df['heat_index'] = df['temperature'] * 0.7 + df['humidity'] * 0.3

# Print the updated DataFrame
print(df)
