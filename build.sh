#!/bin/sh

version='dev'
docker build -t spotify/kafka:$version .
