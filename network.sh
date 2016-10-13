#!/bin/sh

docker network ls
docker network create my-kafka-cluster
docker network ls
