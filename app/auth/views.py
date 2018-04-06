from flask_login import login_user, login_required, logout_user, current_user
from flask import redirect, render_template, flash, url_for
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
        print('\n\n')
        print(user)
        if user is not None and user.verify_password(password):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.home'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


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
        uni = email.find('@')
        user = User(id=email[:uni],
                    email=email,
                    password=form.password.data,
                    school=form.school.data)
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
