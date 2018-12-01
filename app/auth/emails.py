import requests
from requests.exceptions import RequestException
from flask_mail import Mail, Message
from flask import render_template
from app import create_app

app = create_app()


def send_email(to, subject, template, **kwargs):
    msg = Message(subject=app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


def send_message(recipients=None, subject=None,
                 text=None, template=None, **kwargs):
    try:
        key = app.config["MAILGUN_KEY"]
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
