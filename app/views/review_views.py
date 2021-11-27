from datetime import datetime

from flask import Blueprint, url_for, request, flash, redirect
from flask.templating import render_template
from flask_login import login_required, current_user
from sqlalchemy import func

from .. import db
from ..models import Book, Review

bp = Blueprint('review', __name__, url_prefix='/review')


@bp.route('/create/<int:book_id>', methods=('POST',))
@login_required
def create(book_id):
    book = Book.query.get_or_404(book_id)
    content = request.form['content']
    star_rate = request.form['rating']
    if not content:
        flash('리뷰 내용을 작성해주셔야 해요!')
        return render_template('book.detail')
    if not star_rate:
        flash('평점을 매겨주셔야 해요!')
        return render_template('book.detail')

    sofar_reviews = len(book.review_set)
    sofar_star_rate = book.star_rate

    new_star_rate = (sofar_star_rate * sofar_reviews +
                     int(star_rate)) / (sofar_reviews + 1)
    new_star_rate = round(new_star_rate, 2)

    review = Review(user_id=current_user.id, book_id=book_id, content=content,
                    star_rate=int(star_rate), create_date=datetime.now())
    book.review_set.append(review)
    book.star_rate = new_star_rate
    db.session.commit()
    return redirect(url_for('book.detail', book_id=book_id))
