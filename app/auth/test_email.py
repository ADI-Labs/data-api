# from flask_mail import Message
# from emails import mail, app
import requests
import os
from flask import render_template
import sys

app = Flask(__name__)
#
# msg = Message('test subject', sender='bbz2103@columbia.edu',
#               recipients=['brukbekele333@gmail.com',
#                           'ytm2102@columbia.edu',
#                           'km3290@columbia.edu'])
# msg.body = 'text body'
# msg.html = '<b> HTML </b> body'
# print("About to try and send.")
# with app.app_context():
#     print("Inside the app.context")
#     mail.send(msg)


# recipients = ['bbz2103@columbia.edu']


def send_simple_message(recipients, **kwargs):
    with app.app_context():
        print("In send simple_message")
        template = "auth/email/confirm.html"
        request = requests.post(
            "https://api.mailgun.net/v3/api.adicu.com/messages",
            auth=("api", "key-43b2ffe1fe0c4e268748307f4ec70406"),
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

#send_simple_message()
# send_mail(token="asldkfajdsflk"

def main():
    print(sys.argv)
    email = sys.argv[1]
    send_simple_message(email)

main()
