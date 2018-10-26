from app import create_app, db, mail
from app.models import Course, Dining, Student, User
from app.helpers import get_courses
import os
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()

print("checking courses...")
with app.app_context():
    get_courses()


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

def courses():
    with app.app_context():
        get_courses()


@app.cli.command()
def test():
    """Run unit tests from command line"""
    from unittest import TestLoader, TextTestRunner
    suite = TestLoader().discover('tests')
    TextTestRunner(verbosity=2, buffer=False).run(suite)


def clear():
    os.system('clear')


scheduler = BackgroundScheduler()
scheduler.add_job(func=courses, trigger="interval", seconds=302400)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


