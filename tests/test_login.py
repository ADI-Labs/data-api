import re
from app import create_app, db
from unittest import TestCase
from app.models import User


class LoginTest(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_login(self):
        #register a new account
        res = self.client.post('/auth/register', data={
            'email':'test@apitest.com',
            'username': 'test',
            'password': 'apis',
            'password2': 'apis',
            'school': 'Columbia College'
        })
        self.assertEqual(res.status_code, 200)

        #login with the new account
        res = self.client.post('/auth/login', data={
            'email': 'test@apitest.com',
            'password': 'apis'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        print("USER ")

        #send a confirmation
        user = User.query.filter_by(email='test@apitest.com').first()
        print(user)

        #logout
