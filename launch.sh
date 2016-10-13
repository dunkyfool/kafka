#!/bin/sh


docker run \
-p 2181:2181 \
-p 9092:9092 \
--env ADVERTISED_HOST=172.19.0.2 \
--env ADVERTISED_PORT=9092 \
--net my-kafka-cluster \
-v /home/dunkyfool/kafka:/mnt \
--name test_kafka \
-d spotify/kafka:dev


#sudo sysctl vm.overcommit_memory=1

#docker run \
#-v /home/dunkyfool/redis:/data \
#-p 30001:6379 \
#--net my-redis-cluster \
#--name test_redis \
#-d redis:backup #redis-server /etc/redis/conf/redis.conf #\
#--logfile /etc/redis/log/redis.log

#docker exec test_redis /etc/redis/backup.sh &
