Webserver

requirements:
- install pipenv python package to test locally

  This folder uses pipenv to install the dependencies for the project.
  pipenv is a python virtual enviornment. It allows you to install necessary
  dependencies without making changes to your machine. 

  to enter the virtual enviornment enter the following command:

  pipenv shell

  To run the tests:
  - python -m unittest discover -p test_webserver.py

  To launch locally:
  - gunicorn -w 4 -b 0.0.0.0:8080 --log-level debug webserver:app



To build the docker image run the following command: 

- docker build -t webserver:1.0 .

To run the docker container run the following command:

- docker run -dp 8080:8080 webserver:1.0  

  This runs the container in detached mode, which means it won't hang
  and binds the container's port 8080 to the machine's port 8080.
  that means that you can reach the port from your local machine.
