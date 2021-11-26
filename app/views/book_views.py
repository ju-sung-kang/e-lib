from flask import Blueprint, render_template, request, flash, url_for
from flask_login import current_user
from datetime import datetime

from .. import db
from ..models import Book, Rent

bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/list', methods=('GET',))
def _list():
    page = request.args.get('page', type=int, default=1)
    book_list = Book.query.order_by(Book.id)
    book_list = book_list.paginate(page, per_page=8)
    return render_template('book_list.html', book_list=book_list)


@bp.route('/detail/<int:book_id>')
def detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)
