import os
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


mail = Mail(app)


def send_email(to, subject, template, **kwargs):
    msg = Message(subject=app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
