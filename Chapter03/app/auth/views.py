from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user

from app.auth import auth
from app.auth.forms import  LoginForm, SignupForm
from app.auth.models import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_by_email = User.query.filter_by(email=form.email.data).first()
        if user_by_email is not None and user_by_email.verify_password(form.password.data):
            login_user(user_by_email)
            return redirect(url_for('todo.list'))
    return render_template('auth/login.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if not User.query.filter_by(email=form.email.data).scalar():
            User(
                email = form.email.data,
                password = form.password.data
            ).save()
            return redirect(url_for('auth.login'))
        else:
            form.errors['email'] = 'User already exists.'
            return render_template('auth/signup.html', form=form)
    return render_template('auth/signup.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
