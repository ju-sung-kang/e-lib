from flask import Blueprint, url_for, request, redirect, render_template, flash, url_for
from flask_login import login_required, login_user, current_user, logout_user
from datetime import datetime

from .. import db
from ..models import Book, Rent

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        book_id = request.form['book_id']
        book = Book.query.filter_by(id=book_id).first()
        if book.stock <= 0:
            flash('책 재고가 없습니다')
        else:
            rent = Rent(user_id=current_user.user_id,
                        book_id=book_id, start_date=datetime.now())
            db.session.add(rent)
            book.stock -= 1
            db.session.commit()
            flash('대여완료!')
        return redirect(url_for('/'))
    else:
        page = request.args.get('page', type=int, default=1)
        book_list = Book.query.order_by(Book.id)
        book_list = book_list.paginate(page, per_page=8)
        return render_template('book_list.html', book_list=book_list)
