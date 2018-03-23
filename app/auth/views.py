from flask_login import login_user, login_required, logout_user
from flask import redirect, abort, request, Response
from ..models import User
from . import auth


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_secret":
            id = username.split('user')[0]
            user = User(id)
            login_user(user)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')
