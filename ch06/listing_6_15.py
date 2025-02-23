import pandas as pd

df_tags = pd.DataFrame({'tags': ['ski shoes', 'running gear', 'snowboard boots', 'unknown tag']})  #A
tag_reference = {  #B
    'ski shoes': 'ski equipment',
    'running gear': 'athletic equipment',
    'snowboard boots': 'snowboard equipment'
}
df_tags = chatgpt_transform_column(df_tags, 'tags', "Map this tag to a standardized category based on the reference list. If the tag does not exist in the reference, return 'Uncategorized'.", reference=tag_reference)  #C

print("\nStandardized Tags:\n", df_tags)  #D

#A Create a sample DataFrame with raw tags.
#B Define a mapping dictionary for standardizing tags into broader categories.
#C Use the chatgpt_transform_column function to map tags to standardized categories based on the reference list.
#D Print the standardized tags DataFrame.
