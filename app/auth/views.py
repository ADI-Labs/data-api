from flask_login import login_user, login_required, logout_user, current_user
from flask import redirect, render_template, flash, url_for, request
from .. import db
from ..models import User
from . import auth
from .forms import LoginForm, RegistrationForm


@auth.route("/")
def home():
    return redirect(url_for('index'))


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        print(user)
        if user is not None and user.verify_password(password):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or next.startswith('/'):
                next = url_for('main.home')
            return redirect(next)
        flash('Invalid username or password.')
        print('flashed')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.home'))


@auth.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        uni_ind = email.find('@')
        user = User(uni=email[:uni_ind],
                    email=email,
                    password=form.password.data,
                    school=form.school.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/token', methods=["GET"])
@login_required
def token():
    token = current_user.generate_confirmation_token()
    return render_template('auth/token.html', api_key=str(token))
