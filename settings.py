#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import logging
import yaml
ocr_temp_directory  = None
ocr_in_directory = None
ocr_out_directory = None
logger = logging.getLogger()
lang_processing = [
    'vie',
    'eng'
]
fs_crawler_path = r'\\172.16.7.81\source\fscrawler-es7-2.9\docs'
poppler_path = ""
kafka_server = None
lv_file_server_host = ""


def load_form_working_dir(working_dir):
    global poppler_path
    global kafka_server
    global lv_file_server_host
    global ocr_temp_directory
    global ocr_in_directory
    global ocr_out_directory
    config = {}
    config_path = os.path.join(working_dir,"settings.yaml")
    print("load ... '{}'".format(config_path))
    with open(config_path,
              mode="r",
              encoding="utf-8"
              ) as stream:
        try:
            config = yaml.safe_load(stream)

        except yaml.YAMLError as exc:
            print("load ... '{}' is fail".format(config_path))
            print(exc)

    os.environ["TMP"] = os.path.join(working_dir, "tmp")
    if not os.path.isdir(os.environ["TMP"]):
        os.mkdir(os.environ["TMP"])
    os.environ["TEMP"] = os.environ["TMP"]
    poppler_path = os.path.join(working_dir, "poppler-0.68.0", "bin")
    """
    Quan tr?ng không có cái này không x? ly image to pdf dc
    """

    ocr_temp_directory = os.path.join(working_dir, "docs")
    """
    Temporary directory for orc processing auto created if not exist
    """
    if not os.path.isdir(ocr_temp_directory):
        print('"{}" is not exist'.format(ocr_temp_directory))
        os.makedirs(ocr_temp_directory)
        print('"{}" has been created'.format(ocr_temp_directory))
    else:
        print('"{}" is already'.format(ocr_temp_directory))
    ocr_in_directory = os.path.join(ocr_temp_directory, "in")
    """
    All file for orc before processing put here. The directory will be created if 
    not exist
    """

    if not os.path.isdir(ocr_in_directory):
        print('"{} is not exist'.format(ocr_in_directory))
        os.mkdir(ocr_in_directory)
        print("'{}' has been created".format(ocr_in_directory))
    else:
        print("'{}' is already".format(ocr_in_directory))

    ocr_out_directory = os.path.join(ocr_temp_directory, "out")
    """
    After ocr successfully process file. The processed-file will be put here
    The directory will be created if not exist
    """

    if not os.path.isdir(ocr_out_directory):
        print('"{} is not exist'.format(ocr_out_directory))
        os.mkdir(ocr_out_directory)
        print("'{}' has been created".format(ocr_out_directory))
    else:
        print("'{}' is already".format(ocr_out_directory))

    log_path = os.path.join(working_dir, "logs")
    if not os.path.isdir(log_path):
        os.mkdir(log_path)

    """
    log directory inside current directory python log will create if not exist
    """
    kafka_server = ["192.168.18.36:9092"]
    """
    Server host kafka including port
    """
    lv_file_server_host = "http://192.168.18.36:5010"
    """
    url of lacviet file service
    """
    __formatter__ = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s',
                                      '%m-%d-%Y %H:%M:%S')

    logger.setLevel(
        logging.DEBUG
        # logging.INFO
        # |
        # logging.ERROR
    )
    __path_to_info_logs__ = os.path.join(log_path, 'info')
    if not os.path.isdir(__path_to_info_logs__):
        os.mkdir(__path_to_info_logs__)
    __logger_info_handler__ = logging.FileHandler(os.path.join(__path_to_info_logs__, 'logs.txt'))
    __logger_info_handler__.setLevel(logging.INFO)
    __logger_info_handler__.setFormatter(__formatter__)

    __path_to_error_logs__ = os.path.join(log_path, 'error')
    if not os.path.isdir(__path_to_error_logs__):
        os.mkdir(__path_to_error_logs__)
    __logger_error_handler__ = logging.FileHandler(os.path.join(__path_to_error_logs__, 'logs.txt'))
    __logger_error_handler__.setLevel(logging.ERROR)
    __logger_error_handler__.setFormatter(__formatter__)

    __path_to_debug_logs__ = os.path.join(log_path, 'debug')
    if not os.path.isdir(__path_to_debug_logs__):
        os.mkdir(__path_to_debug_logs__)
    __logger_debug_handler__ = logging.FileHandler(os.path.join(__path_to_debug_logs__, 'logs.txt'))
    __logger_debug_handler__.setLevel(logging.DEBUG)
    __logger_debug_handler__.setFormatter(__formatter__)

    logger.addHandler(__logger_info_handler__)
    logger.addHandler(__logger_error_handler__)
    logger.addHandler(__logger_debug_handler__)

    lv_file_server_host = config.get('file-server-host', None)
    if not lv_file_server_host:
        print('file-server-host in {} was not found'.format(config_path))
        logger.debug('file-server-host in {} was not found'.format(config_path))
        raise Exception('file-server-host in {} was not found'.format(config_path))

    kafka_server = config.get('kafka-server', None)

    if not kafka_server:
        print('kafka-server in {} was not found'.format(config_path))
        logger.debug('kafka-server in {} was not found'.format(config_path))
        raise Exception('kafka-server in {} was not found'.format(config_path))

    kafka_server = kafka_server.split(',')

    fs_crawler_path = config.get('fs-crawler-path', None)

    if not fs_crawler_path:
        print('fs_crawler_path in {} was not found'.format(config_path))
        logger.debug('fs_crawler_path in {} was not found'.format(config_path))
        raise Exception('fs_crawler_path in {} was not found'.format(config_path))
    if not os.path.isdir(fs_crawler_path):
        logger.error(" Directory '{}' at '{}' in '{}' was not found".format(
            fs_crawler_path,
            "fs-crawler-path",
            config_path
        ))
        print(" Directory '{}' at '{}' in '{}' was not found".format(
            fs_crawler_path,
            "fs-crawler-path",
            config_path
        ))
        raise Exception(" Directory '{}' at '{}' in '{}' was not found".format(
            fs_crawler_path,
            "fs-crawler-path",
            config_path
        ))
    # if everything is ok print all config info

    print("Current working dir '{}'".format(working_dir))
    print("log directory dir '{}'".format(log_path))
    print("kafka server '{}'".format(kafka_server))
    print("file server server '{}'".format(lv_file_server_host))

    logger.info("Current working dir '{}'".format(working_dir))
    logger.info("log directory dir '{}'".format(log_path))
    logger.info("kafka server '{}'".format(kafka_server))
    logger.info("file server server '{}'".format(lv_file_server_host))
