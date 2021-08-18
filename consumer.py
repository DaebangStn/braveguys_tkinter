from kafka import KafkaConsumer

consumer = KafkaConsumer('test',bootstrap_servers=['localhost:9092'])
for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                message.offset, message.key,
                message.value))
    break
