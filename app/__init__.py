from flask import Flask
from flask_restful import Api
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

import os

api = Api()

login_manager = LoginManager()
login_manager.login_view = "login"


def create_app(name=__name__):
    app = Flask(name)
    bootstrap = Bootstrap(app) # noqa: F841
    app.config.update(
        DEBUG=True,
        SECRET_KEY=os.environ.get('SECRET_KEY', 'secret_xxx')
    )

    api.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
