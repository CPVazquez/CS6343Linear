FROM python:alpine3.11

ENV PYTHONBUFFERED 1
ENV PYTHONFAULTHANDLER 1

COPY . /app
WORKDIR /app

RUN apk add curl curl-doc

RUN pip install pipenv
RUN echo python3 --version
RUN pipenv install --system --deploy

EXPOSE 8080 

ENV QUART_APP=src.wkf-manager:app

CMD quart run --port 8080 --host 0.0.0.0
