from app import create_app, db
from app.models import User
from app.models import Course
from app.models import Dining, Student

import os

app = create_app()

def clear():
    os.system('clear')

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Student=Student, Course=Course, Dining=Dining, clear=clear)

@app.cli.command()
def test():
    """Run unit tests from command line"""
    from unittest import TestLoader, TextTestRunner
    suite = TestLoader().discover('tests')
    TextTestRunner(verbosity=2).run(suite)
