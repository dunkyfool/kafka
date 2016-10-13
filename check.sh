#!/bin/sh

echo 'docker status'
docker ps
echo ''
echo 'docker logs'
docker logs test_kafka
echo ''
#echo 'show current configure'
#python main.py 4
