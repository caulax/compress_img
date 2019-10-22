FROM python:3.7-alpine3.9

WORKDIR /opt/app/

COPY src/ /opt/app/

ENV FLASK_ENV=development
ENV FLASK_APP=run.py

CMD "flask run"
