import connect
import redis
from models import Author, Quote

redis_client = redis.Redis(host='localhost', port=6379, password=None)

while True:
    command = input("Enter a command: ")
    if command.startswith('name:'):
        author_name = command.split(':')[1].strip()
        if redis_client.exists(author_name):
            quotes = redis_client.get(author_name)
            print(quotes.decode('utf-8'))
        else:
            author = Author.objects(fullname__iregex=author_name)
            if author:
                quotes = Quote.objects(author=author[0].id)
                for quote in quotes:
                    print(quote.quote)
                redis_client.set(author_name, '\n'.join(quote.quote for quote in quotes if quote.quote))
            else:
                print("Author not found.")

    if command.startswith('tag:'):
        tag = command.split(':')[1].strip()
        if redis_client.exists(tag):
            quotes = redis_client.get(tag)
            print(quotes.decode('utf-8'))
        else:
            quotes = Quote.objects(tags__iregex=tag)
            for quote in quotes:
                print(quote.quote)
            redis_client.set(tag, '\n'.join(quote.quote for quote in quotes))
    if command.startswith('tags:'):
        tags = command.split(':')[1].strip().split(',')
        tags_key = ','.join(tags)
        if redis_client.exists(tags_key):
            quotes = redis_client.get(tags_key)
            print(quotes.decode('utf-8'))
        else:
            quotes = Quote.objects(tags__in=tags)
            for quote in quotes:
                print(quote.quote)
            redis_client.set(tags_key, '\n'.join(quote.quote for quote in quotes))
    if command == 'exit':
        break
