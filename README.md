### data and setting up the hail enviornment

1. Hail enviornment was created in a [docker container](Dockerfile)

2. To start the container: `docker run -it --rm -p 8889:8889 -v $PWD:/hail hail-jupyter` 

3. To connect from local:`ssh -N -f -L localhost:8889:localhost:8889 ifpan` then `localhost:8889` in browser
 


