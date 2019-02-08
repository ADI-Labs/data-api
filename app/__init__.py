from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap
import os
import json


login_manager = LoginManager()
login_manager.login_view = "login"
db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()
config = json.load(open("config_keys.json"))

basedir = os.path.abspath(os.path.dirname(__file__))

# UNCOMMENT BELOW LINE FOR DEPLOY
# storedir = '/storage'
storedir = './'


def create_app(name=__name__):
    app = Flask(name)
    database_uri = "sqlite:///" + os.path.join(storedir, 'data.sqlite')
    app.config.update(
        DEBUG=False,
        SQLALCHEMY_DATABASE_URI=database_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_COMMIT_ON_TEARDOWN=True,
        MAIL_SERVER='smtp.mailgun.org',
        MAIL_PORT=587,
        MAIL_USERNAME=os.environ.get('MAILGUN_USERNAME'),
        MAIL_PASSWORD=os.environ.get('MAILGUN_PASSWORD'),
        MAIL_DEFAULT_SENDER=os.environ.get('MAILGUN_USERNAME'),
        SECRET_KEY=config["SECRET_KEY"],
        SECURITY_PASSWORD_SALT=config["SECURITY_PASSWORD_SALT"],
        MAILGUN_KEY=config["MAILGUN_KEY"],
        ERROR_404_HELP=False,
        CORS_HEADERS='Content-Type'
    )

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api_bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    return app
