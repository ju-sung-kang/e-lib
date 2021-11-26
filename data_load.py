import csv

from app import db
from app.models import Book
from main import app_obj

app_obj.app_context().push()

with open('library.csv', 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        book = Book(
            id=int(row['id']),
            isbn=row['isbn'],
            title=row['book_name'],
            author=row['author'],
            publisher=row['publisher'],
            publication_date=row['publication_date'],
            pages=int(row['pages']),
            description=row['description'],
            link=row['link'],
            stock=5,
            star_rate=0,
        )
        db.session.add(book)
    db.session.commit()
