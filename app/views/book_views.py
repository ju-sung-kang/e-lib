from flask import Blueprint, render_template, request, flash, url_for
from werkzeug.utils import redirect
from flask_login import login_required, login_user, current_user, logout_user
from app.models import Book, Rent
from app import db
from datetime import datetime

bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/list', methods=('GET', 'POST'))
def _list():
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
        return redirect(url_for('book._list'))
    else:
        page = request.args.get('page', type=int, default=1)
        book_list = Book.query.order_by(Book.id)
        book_list = book_list.paginate(page, per_page=8)
        return render_template('book_list.html', book_list=book_list)


@bp.route('/detail/<int:book_id>')
def detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)
