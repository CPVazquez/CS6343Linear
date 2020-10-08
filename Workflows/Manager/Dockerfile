FROM python:alpine3.11

ENV PYTHONBUFFERED 1
ENV PYTHONFAULTHANDLER 1

COPY . /app
WORKDIR /app

RUN pip install pipenv
RUN echo python3 --version
RUN pipenv install --system --deploy
#RUN pipenv install --deploy

EXPOSE 8080 

CMD gunicorn -b 0.0.0.0:8080 --timeout=300 --graceful-timeout=300 --log-level debug src.wkf-manager:app
