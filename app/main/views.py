from flask import render_template
from . import main


@main.route('/')
def home():
    return render_template('main/home.html')
