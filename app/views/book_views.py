from flask import Blueprint, render_template

from app.models import Book

bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/list')
def _list():
    book_list = Book.query.all()
    return render_template('book_list.html', book_list=book_list)


@bp.route('/detail/<int:book_id>')
def detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)
