FROM python:3.6
MAINTAINER ADI <labs@adicu.com>
WORKDIR /data
EXPOSE 6003

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# add the rest of the application
COPY ./ ./

CMD /bin/bash -c "FLASK_APP=run.py flask run"
