import json
import os.path
import time
from json import dumps
from kafka import KafkaProducer, consumer
from json import loads
from kafka import KafkaConsumer
from concurrent.futures import ThreadPoolExecutor

import file_processing
import settings
import threading

def init_consumer(
        topic_id,
        group_id,
        bootstrap_servers):
    current_consumer = None
    while not current_consumer:
        try:
            current_consumer = KafkaConsumer(
                topic_id,
                bootstrap_servers=bootstrap_servers,
                auto_offset_reset='earliest',
                group_id=group_id,
                enable_auto_commit=False,

                value_deserializer=lambda x: loads(x.decode('utf-8'))
            )
        except Exception as e:
            settings.logger.debug(e)
            settings.logger.info("Will resume at 5 s")
            time.sleep(3)
    return current_consumer
def test():
    import time
    def fx():
        from random import randint
        n = randint(10, 30)
        print("sleep {}".format(n))
        time.sleep(n)
    th=threading.Thread(target=fx)
    time.sleep(1)
    th.start()
    th.join()

def runner(
        current_consumer,
        logger,
        topic_id,
        bootstrap_servers,
        group_id,
        process_handler

         ):

    while True:
        try:
            msg = current_consumer.poll(timeout_ms=1)
            if msg.values().__len__()>0:
                logger.info("recive new topic")


                assert isinstance(msg, dict)
                x= msg.popitem()
                record = x[1][0]
                logger.info(json.dumps(record.value))
                assert isinstance(record, consumer.fetcher.ConsumerRecord)
                if isinstance(record.value,dict):
                    try:
                        print(record.value["UploadInfo"]["UploadId"])
                        th = threading.Thread(
                            target=file_processing.hander,
                            args=(
                                current_consumer,
                                msg,
                                record.value,
                                record
                            )
                        )
                        time.sleep(1)
                        th.start()
                        from datetime import date
                        dir_name = date.today().strftime("%Y-%m-%d")
                        dir_to_day = os.path.join(settings.data_dir, dir_name)
                        if not os.path.isdir(dir_to_day):
                            os.mkdir(dir_to_day)
                        path_to_msg_json = os.path.join(dir_to_day, record.value["UploadInfo"]["UploadId"] + ".json")
                        if not os.path.isfile(path_to_msg_json):
                            str_json = json.dumps(
                                record.value["UploadInfo"],
                                indent = 4,
                                sort_keys = True
                            )
                            with open(path_to_msg_json, "w") as text_file:
                                text_file.write(str_json)
                        #th.join()
                        # with ThreadPoolExecutor(max_workers=10) as executor:
                        #     future = executor.submit(
                        #         test)
                        #     print(future.result())
                        # logger.info(dumps(record.value))
                        # with ThreadPoolExecutor(max_workers=settings.max_workers) as executor:
                        #     future = executor.submit(
                        #         process_handler,
                        #         current_consumer,
                        #         msg,
                        #         record.value,
                        #         record)
                        #     print(future.result())
                        # process_handler(
                        #     msg,
                        #     record.value,
                        #     record
                        # )
                    except Exception as e:
                        print("error")
                        print(e)
                        logger.debug(e)
        except Exception as e:
            print(e)
            print("resume")
    current_consumer.close()