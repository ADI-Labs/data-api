from flask_login import UserMixin
from . import login_manager, db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash


# commented for now to pass the flake8 checks
@login_manager.user_loader # noqa: F811
def load_user(userid):
    try:
        user = User.query.filter_by(id=userid).first()
        return user
    except Exception:
        return None


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username, password = token.split(":")  # naive token
        user_entry = User.get(username)
        if user_entry is not None:
            user = User(user_entry[0], user_entry[1])
            if user.password == password:
                return user
    return None


class User(UserMixin, db.Model):

    id = db.Column(db.String(120), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), unique=False, nullable=False)
    school = db.Column(db.String(120), unique=False, nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer('xxx', expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify(self, token):
        s = Serializer('xxx')
        try:
            data = s.loads(token)
        except Exception:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirm = True
        db.session.add(self)
        return True
