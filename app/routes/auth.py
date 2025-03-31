from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from app import db
from app.models.models import User
from app.forms.auth_forms import LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'cook':
            return redirect(url_for('cook.dashboard'))
        elif current_user.role == 'waiter':
            return redirect(url_for('waiter.dashboard'))
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя пользователя или пароль')
            return redirect(url_for('auth.login'))
        
        if user.status == 'fired':
            flash('Ваша учетная запись деактивирована')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('auth.index')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Вход в систему', form=form)

@auth.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', title='Профиль пользователя')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 