# from flask_mail import Message
# from emails import mail, app
from flask import render_template
import requests
import os
import sys


def send_simple_message(recipients, **kwargs):
    key = os.environ.get("MAILGUN_KEY")
    print('The key extracted is: ', key)
    with app.app_context():
        template = 'auth/email/confirm.html'
        request = requests.post(
            "https://api.mailgun.net/v3/api.adicu.com/messages",
            auth=("api", key),
            data={
                "from": "Data@CU data@cu.adicu.com",
                "to": recipients,
                "subject": "DATA@CU Email Testing",
                "text": "Testing: Pleaseeeeee tell me this works ",
                "html": render_template(template, **kwargs)})

        print("Status: {0}".format(request.status_code))
        print("Body: {0}".format(request.text))
        return


def send_mail(recipients=None, subject=None, text=None, template=None, **kwargs):

    try:
        key = os.environ.get('MAILGUN_KEY')
        print("In send message")
        request = requests.post(
            "https://api.mailgun.net/v3/api.adicu.com/messages",
            auth=("api", key),
            data={
                "from": "Data@CU data@cu.adicu.com",
                "to": recipients,
                "subject": subject,
                "text": text,
                "html": render_template(template, **kwargs),
            })
        print("Status: {0}".format(request.status_code))
        print("Body: {0}".format(request.text))
        return True
    except Exception:
        print("Status: {0}".format(request.status_code))
        print("Body: {0}".format(request.text))
        print("Got an exception.")
        return False


def main():
    print(sys.argv)
    email = sys.argv[1]
    send_simple_message(email)

main()
