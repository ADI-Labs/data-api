from flask import Blueprint
from . import views  # noqa: F401
from flask.ext.login import LoginManager

auth = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config.app):
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')
	login_manager.init_app(app)
	return app

