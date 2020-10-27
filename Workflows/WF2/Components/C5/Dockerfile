FROM python:alpine3.11

LABEL author="Carla Patricia Vazquez"
LABEL version="1.0.0"
LABEL maintainer="Carla Patricia Vazquez"
LABEL emai="cpv150030@utdallas.edu"
LABEL status="Development"

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
