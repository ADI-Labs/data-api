from app import create_app, db
from unittest import TestCase


class LoginTest(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI=f"sqlite:///data_testing.sqlite"
        )
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_login(self):
        """
        tests the registration process
        :return:
        """
        res = self.client.post('/auth/register', data={
            'email': 'test@apitest.com',
            'username': 'test',
            'password': 'apis',
            'password2': 'apis',
            'school': 'Columbia College'
        })
        self.assertEqual(res.status_code, 200)

        # TODO: CSRF token is broken and unsure why

        # print(res.get_data(as_text=True))
        # # self.assertGreater(len(User.query.all()), 0)
        #
        # # login with the new account
        # res = self.client.post('/auth/login', data={
        #     'email': 'test@apitaest.com',
        #     'password': 'apis'
        # }, follow_redirects=True)
        #
        # self.assertEqual(res.status_code, 200)
        # print(res.get_data(as_text=True))
        # self.assertTrue('test@apitest.com' in res.get_data(as_text=True))
        # # send a confirmation
        # print(User.query.all())
        # user = User.query.filter_by(email='test@apitest.com').first()
        # self.assertIsNotNone(user)
        # self.assertEqual(user.email, 'test@apitest.com')
        #
        # res_logout = self.client.get('/auth/logout')
        # self.assertEqual(res_logout, 200)
