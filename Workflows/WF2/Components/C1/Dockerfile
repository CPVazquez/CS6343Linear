FROM python:alpine3.11

ENV PYTHONBUFFERED 1
ENV PYTHONFAULTHANDLER 1

COPY . /app
WORKDIR /app

RUN pip install pipenv
RUN echo python3 --version
RUN pipenv install --system --deploy

EXPOSE 1000

CMD gunicorn -b 0.0.0.0:1000 src.order-verifier:app
