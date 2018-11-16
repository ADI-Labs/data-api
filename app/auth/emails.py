import os
import requests
from requests.exceptions import RequestException
from flask import Flask
from flask_mail import Mail, Message
from flask import render_template

app = Flask(__name__)


#
# app.config['MAIL_SUBJECT_PREFIX'] = 'Confirmation Email'
# app.config['MAIL_SENDER'] = 'ADICU: data@adicu.com'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get("EMAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("EMAIL_PASSWORD")
app.config["SERVER_NAME"] = "data.adicu.com"

mail = Mail(app)


def send_email(to, subject, template, **kwargs):
    msg = Message(subject=app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


def send_message(recipients=None, subject=None,
                 text=None, template=None, **kwargs):
    try:
        key = os.environ.get('MAILGUN_KEY')
        print("In send message")
        print("The key is: ", key)
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
    except RequestException as e:
        print(e)
        # print("Status: {0}".format(request.status_code))
        # print("Body: {0}".format(request.text))
        return False
