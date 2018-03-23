from flask import render_template
from . import main


@main.route('/')
def base():
    return render_template('base.html')


@main.route('/courses')
def courses():
    return render_template('main/courses.html')


@main.route('/housing')
def housing():
    return render_template('main/housing.html')


@main.route('/dining')
def dining():
    return render_template('main/dining.html')


@main.route('/auth')
def auth():
    return render_template('main/authentication.html')


@main.route('/docs')
def docs():
    return render_template('main/docs.html')
