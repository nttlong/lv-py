from json import dumps
from kafka import KafkaProducer, consumer
from json import loads
from kafka import KafkaConsumer
def runner(
        logger,
        topic_id,
        bootstrap_servers,
        group_id,
        process_handler

         ):
    __consumer__ = KafkaConsumer(
        topic_id,
        bootstrap_servers= bootstrap_servers,
        auto_offset_reset='earliest',
        group_id=group_id,
        enable_auto_commit = False,

        value_deserializer=lambda x: loads(x.decode('utf-8'))
     )
    while True:
        try:
            msg = __consumer__.poll(timeout_ms=5)
            if msg.values().__len__()>0:
                logger.info("recive new topic")

                assert isinstance(msg, dict)
                x= msg.popitem()
                record = x[1][0]
                assert isinstance(record, consumer.fetcher.ConsumerRecord)
                if isinstance(record.value,dict):
                    try:
                        logger.info(dumps(record.value))
                        process_handler(
                            __consumer__,
                            msg,
                            record.value,
                            record
                        )
                    except Exception as e:
                        print("error")
                        print(e)
                        logger.debug(e)
        except Exception as e:
            print(e)
            print("resume")
    __consumer__.close()