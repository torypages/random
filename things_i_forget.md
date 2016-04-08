# Docker
https://hub.docker.com/_/mongo/

https://github.com/jupyter/docker-stacks/tree/master/all-spark-notebook

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

## Starting Jupyter notebooks

`-p` port mapping

`--user` I have read allow the `NB_UID` to work

`--net=host` to allow me to connect notebooks using my web browser

`-e NB_UUID=1001` without this I would get permission issues when I would mount my host working directory to one of the docker directories

`-v /home/freyja/Code:/home/jovyan/work` Save my work in my normal working directory

```
docker run -d -p 8888:8888 --user root --net=host -e NB_UID=1001 -v /home/freyja/Code:/home/jovyan/work   jupyter/all-spark-notebook start-notebook.sh
```

# Git
## Set editor
```
git config --global core.editor "vim"
```
# Eclipse
`ctrl + F9` to run individual unit tests, when selecting hold shift for debug mode.
