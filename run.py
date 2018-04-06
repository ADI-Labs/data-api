from app import create_app, db, mail
from app.models import User
from app.models import Course, Dining, Student
from requests import Session
import json

import os

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(app=app,
                db=db,
                User=User,
                mail=mail,
                Student=Student,
                Course=Course,
                Dining=Dining,
                clear=clear)



@app.cli.command()
def test():
    """Run unit tests from command line"""
    from unittest import TestLoader, TextTestRunner
    suite = TestLoader().discover('tests')
    TextTestRunner(verbosity=2, buffer=False).run(suite)

@app.cli.command()
def populate_courses(url=''):

    db.create_all()

    data=json.load(open('app/courses.json'))
    for i, datum in enumerate(data):
        course = Course(course_id=datum["Course"],
                        call_number=datum["CallNumber"],
                        course_name=datum["CourseTitle"],
                        bulletin_flags=datum["BulletinFlags"],
                        division_code=datum["DivisionCode"],
                        class_notes=datum["ClassNotes"],
                        num_enrolled=datum["NumEnrolled"],
                        max_size=datum["MaxSize"],
                        min_units=datum["MinUnits"],
                        num_fixed_units=datum["NumFixedUnits"],
                        term=datum["Term"],
                        campus_name=datum["CampusName"],
                        campus_code=datum["CampusCode"],
                        school_code=datum["SchoolCode"],
                        school_name=datum["SchoolName"],
                        approval=datum["Approval"],
                        prefix_name=datum["PrefixName"],
                        prefix_long_name=datum["PrefixLongname"],
                        instructor_name=datum["Instructor1Name"],
                        type_name=datum["TypeName"],
                        type_code=datum["TypeCode"]
                        )

        db.session.add(course)
        db.session.commit()
        if i % 10 == 0:
            print(f'\rSuccessfully added {i} courses...')
    print()


def clear():
    os.system('clear')
