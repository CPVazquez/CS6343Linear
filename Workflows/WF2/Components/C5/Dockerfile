# https://github.com/docker-library/cassandra/issues/94
FROM python:alpine3.11

ENV PYTHONBUFFERED 1
ENV PYTHONFAULTHANDLER 1
ENV FLASK_ENV prodcution

COPY . /app
WORKDIR /app

RUN pip install pipenv
RUN echo python3 --version
RUN pipenv install --system --deploy

EXPOSE 5000

CMD gunicorn -b 0.0.0.0:5000 src.restocker:app
