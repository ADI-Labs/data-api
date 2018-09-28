from app import create_app, db, mail
from app.models import Course, Dining, Student, User
from app.helpers import get_courses

import os


app = create_app()
print("creating database...")
get_courses()
print("database created!")

@app.shell_context_processor
def make_shell_context():
    return dict(app=app,
                db=db,
                User=User,
                mail=mail,
                Student=Student,
                Course=Course,
                Dining=Dining,
                )


@app.cli.command()
def courses():
    get_courses()


@app.cli.command()
def test():
    """Run unit tests from command line"""
    from unittest import TestLoader, TextTestRunner
    suite = TestLoader().discover('tests')
    TextTestRunner(verbosity=2, buffer=False).run(suite)


def clear():
    os.system('clear')



