from flask_login import login_user, login_required, logout_user, current_user
from flask import redirect, render_template, flash, url_for, request
from .. import db
from ..models import User
from . import auth
from .forms import LoginForm, RegistrationForm, ResetPasswordForm
from .emails import send_email, send_message
from sqlalchemy.exc import IntegrityError
import os


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
        if user is not None and user.verify_password(password) \
                and user.confirmed:
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
    print("Inside register;")
    form = RegistrationForm()
    print("Form was just made")
    if form.validate_on_submit():
        try:
            uni = form.uni.data
            email = form.email.data
            user = User(uni=uni,
                        email=email,
                        password=form.password.data,
                        school=form.school.data)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            print("Token:",token)
            print("Email:",user.email)
            cmd_str = "python app/auth/test_email.py "+user.email
            os.system(cmd_str)
            print("Right before send_message")
            send_message(recipients=[user.email],
                     subject="DATA@CU Email Testing",
                     text="This is your user confirmation link",
                     template='auth/email/confirm.html',
                     ##token=token
                     )
            print("send message passed")
            flash("A confirmation email has been sent to your email address.")
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash("Sorry. That UNI already exists.")
        except Exception as e:
            ##db.session.delete(user)
            print(e)
            flash("An error occured during registering.")
        print("WHy are you here?")
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


@auth.route('/forgot_password', methods=["GET", 'POST'])
def forgot_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user and user.confirmed:

            flash('A password reset link has been sent to your email address.')

            return render_template('auth/forgot_password.html')
            # Just for trial

        elif not user.confirmed:
            flash("User account has been registered but not been confirmed yet.")
            print(user)
        elif not user:
            flash("There is no account registered with this email address.")
    return render_template('auth/forgot_password.html', form=form)
    # Just for trial
