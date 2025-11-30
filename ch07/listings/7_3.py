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

print(json_data)