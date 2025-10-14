import pandas as pd  #A

# Sample JSON data structure (would be loaded from file in practice)
json_data = {
    "library": {
        "name": "Central Library",
        "location": "Downtown",
        "books": [
            {
                "title": "Python Programming",
                "author": {
                    "first_name": "John",
                    "last_name": "Smith"
                },
                "genres": ["Programming", "Technology"],
                "published_year": 2023
            },
            {
                "title": "Data Science Handbook",
                "author": {
                    "first_name": "Jane",
                    "last_name": "Doe"
                },
                "genres": ["Data Science", "Analytics"],
                "published_year": 2022
            }
        ]
    }
}

# Function to convert nested JSON to a DataFrame  #B
def json_to_dataframe(json_data):  #C
    """Convert nested JSON to a pandas DataFrame."""  #D
    records = []  #E
    for book in json_data['library']['books']:  #F
        record = {  #G
            'Library Name': json_data['library']['name'],  #H
            'Location': json_data['library']['location'],  #I
            'Title': book['title'],  #J
            'Author': f"{book['author']['first_name']} {book['author']['last_name']}",  #K
            'Genres': ', '.join(book['genres']),  #L
            'Published Year': book['published_year']  #M
        }
        records.append(record)  #N
    return pd.DataFrame(records)  #O

df = json_to_dataframe(json_data)  #P
print(df)  #Q

#A Import the pandas library for data manipulation and analysis.
#B–#D Define a function to transform nested JSON into a flat pandas DataFrame.
#E–#F Initialize a list to collect records and loop through each book entry in the nested JSON.
#G–#M Extract relevant fields from both the top-level and nested structures and format them into a flat dictionary.
#N Append each structured record to the list of records.
#O Convert the list of dictionaries into a pandas DataFrame and return it.
#P–#Q Call the transformation function and display the resulting DataFrame. 