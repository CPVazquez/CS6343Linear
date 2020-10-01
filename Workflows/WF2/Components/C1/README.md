# Pizza Order Webserver
  Workflow 2, Component 1

## Description
  

## Commands
  * To build the docker image, use the following command in the folder containing the Dockerfile:

    `docker build --rm -t trishaire/webserver path_to_c1_dockerfile`
   
  * To update Dockerhub repository:
  
    ```
    sudo docker login
    docker push trishaire/webserver:tag
    ```

  * To create the image as a service run the following command:

    `docker service create --name webserver --network myNet --publish 8080:8080 --env CASS_DB=VIP_of_Cass_Service trishaire/webserver`

