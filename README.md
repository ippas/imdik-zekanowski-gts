### data and setting up the hail enviornment

1. Hail enviornment was created in a [docker container](Dockerfile)

2. To start the container: `docker run -it --rm -p 8889:8889 hail-jupyter` + add mounting volumes

3. To connect from local:`ssh -N -f -L -p localhost:8889:localhost:8889 remoteuser@remotehost` then `localhost:8889` in browser



