FROM python:3.8.6-slim

ENV PYTHONBUFFERED 1
ENV PYTHONFAULTHANDLER 1

COPY . /app
WORKDIR /app

RUN apt-get -y update 
RUN apt-get install -y \
	build-essential \
	python3-dev \
	python-dev 


RUN pip install -r requirements.txt
RUN pip install fbprophet
RUN pip install cassandra-driver
RUN pip install gunicorn
RUN pip install flask

CMD gunicorn -w 4 -b 0.0.0.0:4000 --log-level info src.auto_restocker:app
