from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc
from datetime import datetime

from .. import db, login_manager
from ..models import Book, Rent

bp = Blueprint('rent', __name__, url_prefix='/rent')


@bp.route('/get-book', methods=('POST',))
@login_required
def get_book():
    book_id = request.form['book_id']
    book = Book.query.filter_by(id=book_id).first()
    if book.stock <= 0:
        flash('책 재고가 없습니다', 'error')
        return redirect(url_for('main.index'))
    else:
        rent = Rent(user_id=current_user.id,
                    book_id=book_id, start_date=datetime.now())
        db.session.add(rent)
        book.stock -= 1
        db.session.commit()
        flash('대여완료!', 'success')
        return redirect(url_for('rent.rent_record'))


@bp.route('/rent-record', methods=('GET',))
@login_required
def rent_record():
    page = request.args.get('page', type=int, default=1)
    records = Rent.query.filter_by(
        user_id=current_user.id).order_by(desc(Rent.start_date))
    records = records.paginate(page, per_page=8)
    return render_template('rent_record.html', records=records)


@bp.route('/return-book', methods=('GET', 'POST'))
@login_required
def return_book():
    if request.method == 'POST':
        rent_id = request.form['rent_id']
        book_id = request.form['book_id']
        rent = Rent.query.filter_by(id=rent_id).first()
        rent.end_date = datetime.now()
        book = Book.query.filter_by(id=book_id).first()
        book.stock += 1
        db.session.commit()
        flash('반납완료', 'success')
        return redirect(url_for('rent.return_book'))
    else:
        page = request.args.get('page', type=int, default=1)
        rent_list = Rent.query.filter(
            Rent.end_date == None, Rent.user_id == current_user.id).order_by(Rent.start_date)
        rent_list = rent_list.paginate(page, per_page=8)
        return render_template('return_book.html', rent_list=rent_list)
