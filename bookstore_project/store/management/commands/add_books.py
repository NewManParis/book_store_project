import os
import logging as lg

import yaml
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from store.models import Book, Author


lg.basicConfig(level=lg.DEBUG)


class Command(BaseCommand):
    help = 'Add books to the database from a yml file located in data/'

    def handle(self, *args, **options):
        # open file with data
        directory = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(directory, 'data', 'books.yml')
        with open(path, 'r') as file:
            data = yaml.load(file)
            books = data['books']
            for book in books:
                # Create author
                authors = []
                for author in book['authors']:
                    try:
                        stored_author = Author.objects.get(name=author)
                        lg.info('Author found: %s'%stored_author)
                    except ObjectDoesNotExist:
                        stored_author = Author.objects.create(name=author)
                        lg.info('Author created: %s'%stored_author)
                    authors.append(stored_author)
                # Find or create book
                try:
                    stored_book = Book.objects.get(title=book['title'])
                    lg.info('Book found: %s'%stored_book.title)
                except ObjectDoesNotExist:
                    book = Book.objects.create(
                        title=book['title'],
                        picture=book['picture'],
                        category=book['category']
                    )
                    #book.authors = authors
                    book.authors.set(authors)
                    #lg.info('New book: %s'%stored_book)
