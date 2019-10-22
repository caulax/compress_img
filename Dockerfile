FROM python:3.7-alpine3.9

WORKDIR /opt/app/

COPY src/ ./
COPY requirements.txt ./requirements.txt

RUN apk update && apk add build-base python-dev py-pip jpeg-dev zlib-dev

RUN pip install -r requirements.txt && rm requirements.txt

ENV FLASK_ENV=development
ENV FLASK_APP=run.py

EXPOSE 5000

CMD "flask run"
