from datetime import datetime

from flask import Blueprint, url_for, request
from werkzeug.utils import redirect

from app import db
from app.models import Book, Review

bp = Blueprint('review', __name__, url_prefix='/review')


@bp.route('/create/<int:book_id>', methods=('POST',))
def create(book_id):
    book = Book.query.get_or_404(book_id)
    content = request.form['content']
    review = Review(content=content, create_date=datetime.now())
    book.review_set.append(review)
    db.session.commit()
    return redirect(url_for('book.detail', book_id=book_id))
