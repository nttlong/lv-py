import kafka
import re_faster
import re_faster.re_kafka_producer
import re_faster.re_kafka_consumer
from re_faster.re_kafka_producer import Bootstrap

consumer = re_faster.re_kafka_consumer.Consumer(["192.168.18.36:9092"])
file_processing = consumer.file_processing
file_processing_topic = file_processing.topic
file_processing_topic_watcher = file_processing.topic.thumb_creator

# bootstrap = Bootstrap(["192.168.18.36:9092"])
# file_system = bootstrap.producers.file_processing.topic.thumb_creator
# assert isinstance(file_system, re_faster.re_kafka_producer.Topic_sender)
# file_system.send(value={
#     "msg":"hello"
# })
# ret = file_system.send({
#         "code":1
#     })
#
print(file_processing_topic_watcher)