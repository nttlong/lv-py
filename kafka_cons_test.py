from confluent_kafka import Consumer


c = Consumer({
    'bootstrap.servers': '192.168.18.36:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit':False
})

c.subscribe(['mytopic3'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print('Received message: {}'.format(msg.value()))

c.close()