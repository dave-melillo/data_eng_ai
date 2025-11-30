import pandas as pd  #A

json_data = {
  "library": {
    "name": "City Library",
    "location": "Downtown",
    "books": [
      {
        "title": "Python Programming",
        "author": {
          "first_name": "John",
          "last_name": "Doe"
        },
        "genres": ["Programming", "Technology"],
        "published_year": 2020
      },
      {
        "title": "Data Science 101",
        "author": {
          "first_name": "Jane",
          "last_name": "Smith"
        },
        "genres": ["Data Science", "AI"],
        "published_year": 2019
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

df = json_to_dataframe(json_data) #P
display(df) #Q