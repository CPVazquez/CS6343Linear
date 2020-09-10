FROM python:alpine3.11

ENV PYTHONBUFFERED 1
ENV PYTHONFAULTHANDLER 1

COPY . /app
WORKDIR /app

RUN pip install pipenv
RUN echo python3 --version
RUN pipenv install --system --deploy

CMD gunicorn -w 4 -b 0.0.0.0:8080 --log-level debug src.webserver:app