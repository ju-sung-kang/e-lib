from email_validator import validate_email, EmailNotValidError
from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db, login_manager
from ..models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email=email).first()


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        input_email = request.form['input_email']
        input_name = request.form['input_name']
        input_password1 = request.form['input_password1']
        input_password2 = request.form['input_password2']

        # 이메일 검증
        if not input_email:
            flash('Email을 입력해주세요.', 'error')
            return render_template('sign_up.html')
        else:
            try:
                validate_email(input_email)
            except EmailNotValidError as e:
                flash('올바른 Email 형식이 아닙니다.', 'error')
                return render_template('sign_up.html')

        # 이름 미입력 방지
        if not input_name:
            flash('이름을 입력해주세요.', 'error')
            return render_template('sign_up.html')

        # 비밀번호 미입력, 혹은 불일치 방지
        if not input_password1 and not input_password2:
            flash('비밀번호를 입력해주세요.', 'error')
            return render_template('sign_up.html')
        elif input_password1 != input_password2:
            flash('비밀번호가 일치하지 않습니다.', 'error')
            return render_template('sign_up.html')

        # 비밀번호 개인정보 보호기준 검증
        alphabet_cnt = 0
        digit_cnt = 0
        special_cnt = 0
        for char in input_password1:
            if char.isalpha():
                alphabet_cnt += 1
            elif char.isdigit():
                digit_cnt += 1
            else:
                special_cnt += 1

        if alphabet_cnt > 0 and digit_cnt > 0 and special_cnt > 0 and len(input_password1) >= 8:
            pass
        else:
            zero_cnt = 0
            for cnt in (alphabet_cnt, digit_cnt, special_cnt):
                if cnt == 0:
                    zero_cnt += 1

            if zero_cnt == 1 and len(input_password1) >= 10:
                pass
            else:
                flash('비밀번호 생성규칙을 확인해주세요!', 'error')
                return render_template('sign_up.html')

        user = User.query.filter_by(email=input_email).first()
        if user:
            flash('이미 가입된 email입니다.', 'error')
            return render_template('sign_up.html')

        new_user = User(username=input_name, password=generate_password_hash(
            input_password1, method='sha256'), email=input_email)
        db.session.add(new_user)
        db.session.commit()
        flash('회원가입 성공! 환영합니다~', 'success')
        return redirect(url_for('auth.signin'))

    else:  # GET
        return render_template('sign_up.html')


@bp.route('/signin', methods=('GET', 'POST'))
def signin():
    if request.method == 'POST':
        input_email = request.form['input_email']
        input_password = request.form['input_password']

        if not input_email:
            flash('아이디를 입력해주세요.', 'error')
            return render_template('sign_in.html')

        if not input_password:
            flash('비밀번호를 입력해주세요.', 'error')
            return render_template('sign_in.html')

        user = User.query.filter_by(email=input_email).first()
        if not user or not check_password_hash(user.password, input_password):
            flash('로그인 실패ㅠㅠ.', 'error')
            return render_template('sign_in.html')
        else:
            login_user(user)
            return redirect(url_for('main.index'))

    else:  # GET
        return render_template('sign_in.html')


@bp.route('/logout', methods=('GET',))
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
