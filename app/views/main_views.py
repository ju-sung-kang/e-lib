from flask import Blueprint, url_for, request, redirect, render_template, flash, url_for
from flask_login import login_required, login_user, current_user, logout_user
from datetime import datetime

from .. import db
from ..models import Book, Rent

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/', methods=('GET', 'POST'))
def index():
    page = request.args.get('page', type=int, default=1)
    book_list = Book.query.order_by(Book.id)
    book_list = book_list.paginate(page, per_page=8)
    return render_template('book_list.html', book_list=book_list)
