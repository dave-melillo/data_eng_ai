import pandas as pd

df = pd.DataFrame({'item_description': [
    'Led Zeppelin Vinyl', 
    'The Beatles CD', 
    'Pink Floyd Tour Poster', 
    'Elvis Cassette Tape', 
    'Rolling Stones T-Shirt'
]})  #A

category_mapping = {
    'vinyl': 'Records',
    'cd': 'CDs',
    'tape': 'Tapes',
    'poster': 'Memorabilia',
    'shirt': 'Memorabilia'
}  #B

def map_category(description):
    for keyword, category in category_mapping.items():  #C
        if keyword.lower() in description.lower():  #D
            return category
    return 'Uncategorized'  #E

df['category'] = df['item_description'].apply(map_category)  #F

print(df)  #G
