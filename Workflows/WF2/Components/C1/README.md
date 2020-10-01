Webserver

Requirements:
  Install pipenv python package to test locally

  This folder uses pipenv to install the dependencies for the project.
  pipenv is a python virtual environment. It allows you to install necessary
  dependencies without making changes to your machine.

  To enter the virtual environment enter the following command:
    pipenv shell

  To run the tests:
    python -m unittest discover -p test_webserver.py

  To launch locally:
    gunicorn -w 4 -b 0.0.0.0:8080 --log-level debug src.webserver:app



To build the docker image run the following command in the folder containing the Dockerfile:

  docker build -t trishaire/webserver .

To create the image as a service run the following command:

  docker service create --name webserver --network myNet --publish 8080:8080 trishaire/webserver

To run the docker container run the following command:

  docker run -dp 8080:8080 webserver:1.0

  This runs the container in detached mode, which means it won't hang
  and binds the container's port 8080 to the machine's port 8080.
  that means that you can reach the port from your local machine.
