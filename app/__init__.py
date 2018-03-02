from flask import Flask
from flask_restful import Api
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os


api = Api()
login_manager = LoginManager()
login_manager.login_view = "login"
db = SQLAlchemy()
bootstrap = Bootstrap()

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(name=__name__):
    app = Flask(name)
    app.config.update(
        DEBUG=True,
        SECRET_KEY=os.environ.get('SECRET_KEY', 'secret_xxx'),
        SQLALCHEMY_DATABASE_URI='sqlite:///' +
        os.path.join(basedir, 'data.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    )

    db.init_app(app)
    api.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
