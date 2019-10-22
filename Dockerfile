FROM python:3.7-alpine3.9

WORKDIR /opt/app/

COPY src/ ./
COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt && rm requirements.txt

ENV FLASK_ENV=development
ENV FLASK_APP=run.py

CMD "flask run"
