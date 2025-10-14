from datetime import datetime
import pandas as pd
import pytz

# Create a sample DataFrame with timestamps in different formats and time zones
df = pd.DataFrame({
    'timestamp': ['2024-03-01 12:00:00 EST', '2024-03-01 17:00:00 GMT', '2024-03-01T09:00:00+05:00']
})

# Function to normalize time zones to UTC
def normalize_to_utc(timestamp):
    try:
        if 'EST' in timestamp:
            local_dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S EST')
            return pytz.timezone('America/New_York').localize(local_dt).astimezone(pytz.utc)
        elif 'GMT' in timestamp:
            local_dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S GMT')
            return pytz.timezone('GMT').localize(local_dt).astimezone(pytz.utc)
        elif '+' in timestamp:
            return pd.to_datetime(timestamp).tz_convert('UTC')
        else:
            raise ValueError("Unsupported format")
    except Exception as e:
        print(f"Error processing timestamp '{timestamp}': {e}")
        return None

# Apply the normalization function to the DataFrame
df['utc_timestamp'] = df['timestamp'].apply(normalize_to_utc)

# Output the standardized DataFrame
print(df)
