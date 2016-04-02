# Docker
https://hub.docker.com/_/mongo/

## Start Mongo

This will start the latest mongo with the following features:

* network in host mode allowing me to easily connect to it
* storing the data in a place of my choosing on the host

```
docker run --net=host --name bench-mongo -v /home/tory/mongo_data/:/data/db -d mongo:latest
```

## Attach running container
```
docker exec -it  8ce9e22a3ed7  /bin/bash
```

# Git
## Set editor
```
git config --global core.editor "vim"
```
