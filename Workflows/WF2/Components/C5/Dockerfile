FROM python:alpine3.11

ENV PYTHONBUFFERED 1
ENV PYTHONFAULTHANDLER 1

COPY . /app
WORKDIR /app

RUN apk add curl curl-docs

RUN curl --unix-socket /var/run/docker.sock http:/v1.40/services/cass | python  -m json.tool > /src/cassInfo.txt


RUN pip install pipenv
RUN echo python3 --version
RUN pipenv install --system --deploy

EXPOSE 8000

CMD gunicorn -b 0.0.0.0:8000 --log-level debug src.restocker:app