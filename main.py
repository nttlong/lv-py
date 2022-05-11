import sys
import os
import lv_mongo_db
print(sys.argv)
if len(sys.argv) ==0 :

    raise Exception(""
                    "Please call main.exe with path to config folder"
                    "Exanple main.exe c:\\orc\config"
                    "")

working_dir = sys.argv[sys.argv.__len__()-1]
print("Running on '{}'".format(working_dir))
if os.path.isfile(working_dir):
    working_dir = os.path.dirname(os.path.realpath(working_dir))
import settings
settings.load_form_working_dir(working_dir)
lv_mongo_db.set_working_folder(working_dir)
settings.logger.info("Running on '{}'".format(working_dir))
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import os.path

import file_consumer

import file_processing
import _thread
from multiprocessing import Process, Manager
__consumer__ = None



__consumer__ = file_consumer.init_consumer(
        topic_id="pdf-processing",
        group_id="lv",
        bootstrap_servers=settings.kafka_server
    )


def call_handler(

        msg,
        data,
        kafka_record,

):
    global __consumer__
    file_processing.hander(__consumer__, msg, data, kafka_record)
    print(data)
def thead_run(

        msg,
        data,
        kafka_record
):

    p = Process(
        target=call_handler,
        args=(

            msg,
            data,
            kafka_record,
        )
    )
    p.start()
    p.join()

if __name__ == '__main__':
    file_consumer.runner(
        current_consumer=__consumer__,
        logger=settings.logger,
        topic_id="pdf-processing",
        process_handler=file_processing.hander,
        group_id="lv",
        bootstrap_servers=settings.kafka_server,


    )
