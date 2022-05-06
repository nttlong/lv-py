import sys
import os
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
settings.logger.info("Running on '{}'".format(working_dir))
# sys.path.append(working_dir)
# sys.path.append(os.path.join(working_dir,"evnv"))
# sys.path.append(os.path.join(working_dir,"evnv","Scripts"))
import os.path

import file_consumer

import file_processing
import _thread




def thead_run(
        consumer,
        msg,
        data,
        kafka_record
):
    _thread.start_new_thread(file_processing.hander, (
        consumer,
        msg,
        data,
        kafka_record,
    ))
file_consumer.runner(
    logger=settings.logger,
    topic_id="pdf-processing",
    process_handler=thead_run,
    group_id="lv",
    bootstrap_servers=settings.kafka_server,


)
