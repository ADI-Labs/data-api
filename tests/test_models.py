from app import create_app, db
from unittest import TestCase
from app.models import Course, Student
import requests


class BasicTest(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(self.app is None)

    def test_app_is_testing(self):
        self.assertTrue(self.app.config['TESTING'])

    def test_student_model(self):
        student = Student(uni= 'test6666',
                          name= 'Test Test Test',
                          department= 'COLUMBIA COLLEGE',
                          email= 'test@test.test',
                          address= 'test test\n 70 Morningside\n \
                          New York NY 10027\nUNITED STATES')

        db.session.add(student)
        db.session.commit()

        self.assertEquals(student,
                         db.session.query(Student)
                          .filter_by(uni='test6666')[0])
        db.session.rollback()

    def test_course_model(self):
        course = Course(
            course_id='test12',
            call_number='56832',
            course_name='projects with eugene wu',
            class_notes='this class is awesome'
        )

        db.session.add(course)
        db.session.commit()
        self.assertEquals(course,
                          db.session.query(Course).filter_by(course_id='')[0])

        db.session.rollback()

    def test_course_ep(self):
        response = requests.get("127.0.0.1:5000/api/course/20181/ACCT5001B200")
        self.assertEquals(response.course_name, "Accounting I: Financial Accoun")
