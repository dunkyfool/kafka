import sys
import time

###################
# Global Variable #
###################
msg_count = 1000000
msg_size = 100
msg_payload = ('kafkatest' * 20).encode()[:msg_size]
#print(msg_payload)
#print(len(msg_payload))

bootstrap_servers = 'localhost:9092'

producer_timings = {}
consumer_timings = {}

def calculate_thoughput(timing, n_messages=1000000, msg_size=100):
    print("Processed {0} messsages in {1:.2f} seconds".format(n_messages,
                                                              timing))
    print("{0:.2f} MB/s".format((msg_size * n_messages)/timing/(1024*1024)))
    print("{0:.2f} Msgs/s".format(n_messages/timing))

# pykafka
def pykafka_test_p(use_rdkafka=False):
    from pykafka import KafkaClient

    client = KafkaClient(hosts=bootstrap_servers)
    topic = client.topics[b'pykafka-test-topic']
    producer = topic.get_producer(use_rdkafka=use_rdkafka)

    produce_start = time.time()
    for i in range(msg_count):
        producer.produce(msg_payload)

    producer.stop()
    return time.time() - produce_start

def pykafka_check_p():
    from pykafka import KafkaClient

    client = KafkaClient(hosts=bootstrap_servers)
    #topic = client.topics[b'pykafka-test-topic']
    topic = client.topics[b'confluent-kafka-topic']
    print(topic.earliest_available_offsets())
    print(topic.latest_available_offsets())

def pykafka_test_c(use_rdkafka=False):
    from pykafka import KafkaClient

    client = KafkaClient(hosts=bootstrap_servers)
    topic = client.topics[b'pykafka-test-topic']
    consumer = topic.get_simple_consumer(use_rdkafka=use_rdkafka)

    msg_consumed_count = 0

    consumer_start = time.time()
    while True:
        msg = consumer.consume()
        if msg: msg_consumed_count += 1
        if msg_consumed_count >= msg_count: break

    consumer.stop()
    return time.time() - consumer_start

# confluent-kafka-python
def ckafka_test_p():
    import confluent_kafka

    topic = 'confluent-kafka-topic'
    conf = {'bootstrap.servers': bootstrap_servers}
    producer = confluent_kafka.Producer(**conf)
    messages_to_retry = 0

    producer_start = time.time()
    for i in range(msg_count):
        try:
            producer.produce(topic, value=msg_payload)
        except BufferError as e:
            messages_to_retry += 1

    for i in range(messages_to_retry):
        producer.poll(0)
        try:
            producer.produce(topic, value=msg_payload)
        except BufferError as e:
            producer.poll(0)
            producer.produce(topic, value=msg_payload)

    producer.flush()
    return time.time() - producer_start

def ckafka_test_c():
    import confluent_kafka
    import uuid

    topic = 'confluent-kafka-topic'
    msg_consumed_count = 0
    conf = {'bootstrap.servers': bootstrap_servers,
            'group.id': uuid.uuid1(),
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': 'earliest'}}
    consumer = confluent_kafka.Consumer(**conf)

    consumer_start = time.time()
    consumer.subscribe([topic])
    raw_input('PAUSE')

    while True:
        msg = consumer.poll(1)
        if msg: msg_consumed_count += 1
        if msg_consumed_count >= msg_count: break

    consumer_timing = time.time() - consumer_start
    consumer.close()
    return consumer_timing

if __name__=='__main__':
    arg_list = sys.argv
    if len(arg_list)==1:
            print 'python main.py MODE'
            print 'MODE:1 [Producer] pykafka test'
            print 'MODE:2 [Producer] pykafka check'
            print 'MODE:3 [Producer] pykafka test w/ C'
            print 'MODE:4 [Consumer] pykafka test'
            print 'MODE:5 [Producer] ckafka test'
            print 'MODE:6 [Consumer] ckafka test'
            #print 'MODE:5 [Consumer] pykafka test w/ C'
    else:
        # Producer pykafka
        if   arg_list[1]=='1':
            producer_timings['pykafka_producer']=pykafka_test_p()
            calculate_thoughput(producer_timings['pykafka_producer'])
        elif arg_list[1]=='2':
            pykafka_check_p()
        elif arg_list[1]=='3':
            producer_timings['pykafka_producer_rd']=pykafka_test_p(True)
            calculate_thoughput(producer_timings['pykafka_producer_rd'])
        elif arg_list[1]=='4':
            consumer_timings['pykafka_consumer']=pykafka_test_c()
            calculate_thoughput(consumer_timings['pykafka_consumer'])
        elif arg_list[1]=='5':
            producer_timings['ckafka_producer']=ckafka_test_p()
            calculate_thoughput(producer_timings['ckafka_producer'])
        elif arg_list[1]=='6':
            consumer_timings['ckafka_consumer']=ckafka_test_c()
            calculate_thoughput(consumer_timings['ckafka_consumer'])
            consumer_timings['ckafka_consumer']=ckafka_test_c()
            calculate_thoughput(consumer_timings['ckafka_consumer'])
