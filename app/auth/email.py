from flask import Flask
from flask.ext.mail import Mail, Message
from flask import render_template

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SUBJECT_PREFIX'] = 'Confirmation Email'
app.config['MAIL_SENDER'] = 'ADICU: data@adicu.com'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "brukbekele333@gmail.com"  # os.environ.get("EMAIL_USERNAME")
app.config['MAIL_PASSWORD'] = ""  # os.environ.get('EMAIL_PASSWORD")


def send_email(to, subject, template, **kwargs):
    msg = Message(subject=app.config['MAIL_SUBJECT_PREFIX']+ subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)