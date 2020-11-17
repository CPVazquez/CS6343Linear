FROM python:alpine3.11

LABEL author="Randeep Ahlawat"
LABEL version="1.0.0"
LABEL maintainer="Randeep Ahlawat"
LABEL email="randeep.ahalwat@utdallas.edu"
LABEL status="Development"

ENV PYTHONBUFFERED 1
ENV PYTHONFAULTHANDLER 1

COPY . /app
WORKDIR /app

RUN pip install pipenv
RUN echo python3 --version
RUN pipenv install --system --deploy

EXPOSE 3000

ENV QUART_APP=src.delivery_assigner:app

CMD quart run --port 3000 --host 0.0.0.0
 
