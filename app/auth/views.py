from flask_login import login_user, login_required, logout_user, current_user
from flask import redirect, render_template, flash, url_for, request
from .. import db
from ..models import User
from . import auth
from .forms import LoginForm, RegistrationForm, ResetPasswordForm, ChangePasswordForm
from .emails import send_message
from sqlalchemy.exc import IntegrityError
from ..decorators import check_confirmed
from .token import generate_confirmation_token, confirm_token


@auth.route("/")
def home():
    return redirect(url_for('main.home'))


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
        if user is not None and user.verify_password(password):
            login_user(user, form.remember_me.data)
            return redirect(url_for('auth.unconfirmed'))

        flash('Invalid username or password.')
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
        try:
            uni = form.uni.data
            email = form.email.data
            user = User(uni=uni,
                        email=email,
                        password=form.password.data,
                        school=form.school.data)
            db.session.add(user)
            db.session.commit()
            token = generate_confirmation_token(user.email)
            send_message(recipients=[user.email],
                     subject="DATA@CU Email Testing",
                     text="This is your user confirmation link",
                     template='auth/email/confirm.html',
                     token=token,
                     user=user
                         )
            login_user(user)
            flash("A confirmation email has been sent to your email address.")
            return redirect(url_for('auth.unconfirmed'))
        except IntegrityError:
            db.session.rollback()
            flash("Sorry. That UNI already exists.")
        except Exception as e:
            print(e)
            flash("An error occurred during registering.")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
def confirm(token):
    try:
        email = confirm_token(token)
    except:
        flash("The confirmation link is invalid or has expired.",'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash("Account already confirmed. Please login. ", 'success')

    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account.", 'success')

    return redirect(url_for('main.home'))


@auth.route('/token', methods=["GET"])
@login_required
@check_confirmed
def token():
    token = current_user.generate_confirmation_token()
    return render_template('auth/token.html', api_key=token.decode('UTF-8'))


@auth.route('/reset_request', methods=["GET", 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        token = generate_confirmation_token(user.email)
        send_message(recipients=[user.email],
                     subject="Reset Password Link",
                     text="This is your user password reset link.",
                     template='auth/forgot_password.html',
                     token=token,
                     user=user
                     )
        flash('A password reset link has been sent to your email address.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))

    try:
        email = confirm_token(token)
    except:
        flash("The password reset link is invalid or has expired.","danger")
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first_or_404()

    form = ChangePasswordForm()
    if form.validate_on_submit():
        new_password = form.password.data
        user.password = new_password
        db.session.add(user)
        db.session.commit()
        flash("Your password has been reset successfully.")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.confirmed:
        return redirect('main.home')
    flash("Please confirm your account!", "warning")
    return render_template('auth/unconfirmed.html')


@auth.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    send_message(recipients=[current_user.email],
                 subject="DATA@CU Email Testing",
                 text="This is your user confirmation link",
                 template='auth/email/confirm.html',
                 token=token,
                 user=current_user
                 )
    flash("A new confirmation email has been sent.", 'success')
    return redirect(url_for('auth.unconfirmed'))
