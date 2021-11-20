from sqlalchemy.orm import backref
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.Date(), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    link = db.Column(db.Text(), nullable=False)
    star_rate = db.Column(db.String)


class Rent(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id',
        ondelete='CASCADE'
    ),
        nullable=False)
    user = db.relationship('User', backref=db.backref(
        'rent_set',
        cascade='all, delete-orphan'))

    book_id = db.Column(db.Integer, db.ForeignKey(
        'book.id',
        ondelete='CASCADE'
    ),
        nullable=False)

    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date())


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id',
        ondelete='CASCADE'
    ),
        nullable=False)
    user = db.relationship('User', backref=db.backref(
        'review_set',
        cascade='all, delete-orphan'))

    book_id = db.Column(db.Integer, db.ForeignKey(
        'book.id',
        ondelete='CASCADE'))
    book = db.relationship('Book', backref=db.backref(
        'review_set',
        cascade='all, delete-orphan'))

    content = db.Column(db.Text(), nullable=False)
    star_rate = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.Date(), nullable=False)
