#!/bin/sh

echo 'Enter an option as following.'
echo '1) Create Topic:test & List current tops '
#echo '*) Delete Topic:test'
echo '2) Send Message (type few messages)'
echo '3) Start a consumer (receive few messages)'

read NUM

case $NUM in
		1) docker exec test_kafka \
		/opt/kafka_2.11-0.8.2.1/bin/kafka-topics.sh \
		--create \
		--zookeeper 172.19.0.2:2181 \
		--replication-factor 1 \
		--partitions 1 \
		--topic test

		docker exec test_kafka \
		/opt/kafka_2.11-0.8.2.1/bin/kafka-topics.sh \
		--list \
		--zookeeper 172.19.0.2:2181 

		docker exec test_kafka \
		/opt/kafka_2.11-0.8.2.1/bin/kafka-topics.sh \
		--describe \
		--zookeeper 172.19.0.2:2181 \
		--topic test
		;;
#		3) docker exec test_kafka \
#		/opt/kafka_2.11-0.8.2.1/bin/kafka-topics.sh --delete --zookeeper 172.19.0.2:2181 --topic test
#		;;
		2) docker exec -it test_kafka \
		/opt/kafka_2.11-0.8.2.1/bin/kafka-console-producer.sh --broker-list 172.19.0.2:9092 --topic test
		;;
		3) docker exec test_kafka \
		/opt/kafka_2.11-0.8.2.1/bin/kafka-console-consumer.sh --zookeeper 172.19.0.2:2181 --topic test --from-beginning
		;;
esac
