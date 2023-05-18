import connect
import json
from models import Author, Quote


def load_quotes():
    with open('quotes.json') as file:
        quotes_data = json.load(file)

    for quote_data in quotes_data:
        author_name = quote_data['author']
        author = Author.objects(fullname=author_name).first()
        if author:
            quote = Quote(
                tags=quote_data['tags'],
                author=author,
                quote=quote_data['quote']
            )
            quote.save()


load_quotes()
