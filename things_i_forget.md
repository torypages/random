# AWS

## remove prefix / path
```
aws s3 rm s3://something/more/ --recursive
```


# Docker
https://hub.docker.com/_/mongo/

https://github.com/jupyter/docker-stacks/tree/master/all-spark-notebook

## Start Mongo

### latest
This will start the latest mongo with the following features:

* network in host mode allowing me to easily connect to it
* storing the data in a place of my choosing on the host

```
docker run --net=host --name bench-mongo -v /home/tory/mongo_data/:/data/db -d mongo:latest
```

### older

```
docker run --net=host --name testmongo -v /home/tory/Code/mongo_mmapv1/mongo/:/data/db -d mongo:2.2.7
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

# Mongo

##Find null values

```
db.somecollection.find({'some_field': {$type: 10}})
```

## Mongodump with timestamp

```
mongodump --db somedb -c actions  --query "{\"timestamp\":{\"\$gt\":{\"\$date\":`date -d 2016-02-01 +%s`000}}, someField: \"someValue\"}"
```


# Java

## Maven skip tests

```
mvn install -DskipTests
```

# SBT Scala Build Tool

## Generate project files for Eclipse

```
sbt eclipse
```

I required a `~/.sbt/0.13/plugins/plugins.sbt` containing the following for this to work

```
addSbtPlugin("com.typesafe.sbteclipse" % "sbteclipse-plugin" % "4.0.0")
```


# Mesos
## Minimesos

For some reason the front page instructions don't tell you to use `--exposedHostPorts` but this part was super important for me.
```
# curl -sSL https://minimesos.org/install | sh
export PATH=$PATH:/root/.minimesos/bin
minimesos up --exposedHostPorts
```

Also, though blunt, restarting docker service `service docker restart` will fix
```
Unable to find image 'inet6:latest' locally
Pulling repository inet6
FATA[0001] Error: image library/inet6:latest not found
```
