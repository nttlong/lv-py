import confluent_kafka
import re_faster
import re_faster.re_kafka_producer
import re_faster.re_kafka_consumer
from re_faster.re_kafka_producer import Bootstrap

consumer = re_faster.re_kafka_consumer.Consumer(["192.168.18.36:9092"])
hello_consumer = consumer.hello
hello_consumer_topic = hello_consumer.topic
hello_consumer_watcher = hello_consumer_topic.hello

bootstrap = Bootstrap(["192.168.18.36:9092"])
hello_producer = bootstrap.producers.hello
topic_hello= hello_producer.topic.hello
topic_hello.send(dict(
    msg="Hello"
))
# print(topic_thumb_creator)
    #.file_processing.topic.thumb_creator
# assert isinstance(file_system, re_faster.re_kafka_producer.Topic_sender)
# for i in range(1,100):
#
#     import time
#     ret =topic_thumb_creator.send(value={
#         "msg":"hello7878878"
#     })
#
#
#     time.sleep(0.02)
#     print(i)


# # print(file_processing_topic_watcher)
# #
count =0
with hello_consumer_watcher.group("ok") as runner:
    def test(con,msg,data):
        global count

        print("-----------------------------------------")
        print("number :{}".format(count))
        print(data)
        print(msg.value())
        print("-----------------------------------------")
        con.commit()
        count +=1
    runner.handler = test
    runner.start_watch()

