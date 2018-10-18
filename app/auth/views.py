from flask_login import login_user, login_required, logout_user, current_user
from flask import redirect, render_template, flash, url_for, request
from .. import db
from ..models import User
from . import auth
from .forms import LoginForm, RegistrationForm, RegeneratePasswordForm
# from .email import send_email


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
        if user is not None and user.verify_password(password) and user.is_confirmed:
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
        uni = form.uni.data
        email = form.email.data
        user = User(uni=uni,
                    email=email,
                    password=form.password.data,
                    school=form.school.data)
        db.session.add(user)
        db.session.commit()
        token = current_user.generate_confirmation_token()
        send_email(user.email, "Confirm your Account", 'auth/email/confirm',
                   user=user, token=token)
        flash('A confirmation email has been sent to your email address.'
              'You have to confirm your email address before you can login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
def confirm(token):
    if current_user.confirm(token):
        flash('You have confirmed your account. Thank you.')

    else:
       flash("The confirmation link is invalid or has expired.")
    return redirect(url_for('main.index'))


@auth.route('/token', methods=["GET"])
@login_required
def token():
    token = current_user.generate_confirmation_token()
    return render_template('auth/token.html', api_key=token.decode('UTF-8'))


@auth.route('/forgot_password', methods=["GET"])
def forgot_password():
    form = RegeneratePasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.is_confirmed:
            pass


