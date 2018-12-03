import requests
from requests.exceptions import RequestException
from flask import render_template
from app import create_app

app = create_app()


def send_message(recipients=None, subject=None,
                 text=None, template=None, **kwargs):
    try:
        key = app.config["MAILGUN_KEY"]
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
