from app import create_app, mail
from flask_mail import Message
from unittest import TestCase


class EmailTest(TestCase):
    def setUp(self):
        self.app = create_app('email_test')
        self.app.config.update(
            TESTING=True,
            MAIL_DEFAULT_SENDER='postmaster@api.adicu.com'
        )
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_single_text_email(self):
        recipients = ['jz2814@columbia.edu']
        msg = Message('TEST', body='testing', recipients=recipients, sender=self.app.config['MAIL_DEFAULT_SENDER'])
        self.assertTrue(self.app.config['TESTING'])

        print(self.app.config)
        # defaults to environment variable $MAILGUN_USERNAME
        self.assertIsNotNone(msg.sender)

        with mail.record_messages() as outbox:
            mail.send(msg)

            self.assertEqual(len(outbox), 1)
            self.assertEqual(outbox[0].subject, 'TEST')
