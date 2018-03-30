from flask import Flask
from flask_login import LoginManager


from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap
import os


login_manager = LoginManager()
login_manager.login_view = "login"
db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()


basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(name=__name__):
    app = Flask(name)
    database_uri = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
    app.config.update(
        DEBUG=True,
        SECRET_KEY=os.environ.get('SECRET_KEY', 'secret_xxx'),
        SQLALCHEMY_DATABASE_URI=database_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_COMMIT_ON_TEARDOWN=True,
        MAIL_SERVER='smtp.mailgun.org',
        MAIL_PORT=587,
        MAIL_USERNAME=os.environ.get('MAILGUN_USERNAME'),
        MAIL_PASSWORD=os.environ.get('MAILGUN_PASSWORD'),
        MAIL_DEFAULT_SENDER=os.environ.get('MAILGUN_USERNAME')
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
