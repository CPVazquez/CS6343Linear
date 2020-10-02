# Pizza Order Verifier
  Workflow 2, Component 1

## Description
  This component receives pizza orders routed from the workflow manager (WFM). Orders are compliant with the pizza-order.schema.json format. Upon receiving an order, C1 validates the order, checks if sufficient stock exists, and if the stock exists, then it creates the order. If sufficient stock is not available, C1 creates a restock order and provides it as a response to the WFM.

## Commands
  * To build the docker image, use the following command in the folder containing the Dockerfile:

    `docker build --rm -t trishaire/order-verifier path_to_c1_dockerfile`
   
  * To update Dockerhub repository:
  
    ```
    sudo docker login
    docker push trishaire/order-verifier:tag
    ```

  * To create the image as a service run the following command:

    ```docker service create --name order-verifier --network myNet --publish port:port --env CASS_DB=cass_service_vip trishaire/order-verifier```

    * Where `port` is `8080` for order-verifier and `cass_service_vip` is the VIP of `myNet` overlay network.