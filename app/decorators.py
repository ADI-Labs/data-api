from functools import wraps
from flask_login import current_user
from flask import redirect, flash, url_for


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash("Please confirm your account!")
            return redirect(url_for('auth.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function
