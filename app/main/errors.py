from . import main
from flask import render_template


@main.app_errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def server_error():
    return render_template('500.html'), 500
