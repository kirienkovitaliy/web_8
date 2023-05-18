import connect
import json
from datetime import datetime
from models import Author



def load_authors():
    with open('authors.json') as file:
        authors_data = json.load(file)

    for author_data in authors_data:
        born_date_str = author_data['born_date']
        born_date = datetime.strptime(born_date_str, "%B %d, %Y")

        author = Author(
            fullname=author_data['fullname'],
            born_date=born_date,
            born_location=author_data['born_location'],
            description=author_data['description']
        )
        author.save()


load_authors()
