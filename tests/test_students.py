from app import create_app
from app.models import User
from app.models import Course
from app.models import Dining, Student
import json
import os

app = create_app()

def parse_and_store():
	db.create_all()
	data = json.load(open('app/compileUnis.json'))
	for datum in data:
		student = Student(uni = datum["uni"],
						  name = datum["name"],
						  title = datum["title"],
						  department = datum["dept"])
		db.session.add(student)
		db.session.commit()

def clear():
	os.system()

@app.shell_context_processor
def make_shell_context():
	return dict(app=app, db=db, User=User)
	return dict(app=app,
				db=db,
				User=User,
				Student=Student,
				Course=Course,
				Dining=Dining,
				clear=clear,
				sqlIt=parse_and_store)

@app.cli.command()
def test():
    """Run unit tests from command line"""
    from unittest import TestLoader, TextTestRunner
    suite = TestLoader().discover('tests')
    TextTestRunner(verbosity=2).run(suite)

    print(Student.get("amz2136"));
