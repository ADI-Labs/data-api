from flask_mail import Message
from emails import mail, app
msg = Message('test subject', sender='bbz2103@columbia.edu',
              recipients=['brukbekele333@gmail.com',
                          'ytm2102@columbia.edu',
                          'km3290@columbia.edu'])
msg.body = 'text body'
msg.html = '<b> HTML </b> body'
print("About to try and send.")
with app.app_context():
    print("Inside the app.context")
    mail.send(msg)
