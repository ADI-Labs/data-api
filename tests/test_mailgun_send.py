# from app import create_app
# from unittest import TestCase
#
#
# class EmailTest(TestCase):
#     '''
#     This does nothing for now since secret environment variables do not work
#     well with travis CI.
#     '''
#     def setUp(self):
#         self.app = create_app('email_test')
#         self.app.config.update(
#             TESTING=True,
#             MAIL_DEFAULT_SENDER='postmaster@api.adicu.com'
#         )
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#
#     def tearDown(self):
#         self.app_context.pop()
