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


#RUN pip install pipenv
#RUN echo python3 --version
#RUN pipenv install --system --deploy


CMD python3 src/auto_restocker.py
 
