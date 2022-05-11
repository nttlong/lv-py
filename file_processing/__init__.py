import os
#from lv_files_client import api, download
from kafka.consumer.group import KafkaConsumer
from .file_ocr import run_ocrmypdf
from .convert_image_to_pdf import convert_image_to_pdf
from .file_update_content import do_update_add_content, do_update_pdf_content
import settings
from .fs_crawler_transfer import dispatcher
from kafka import TopicPartition
import PyPDF2
import lv_mongo_db
#api_call = api(settings.lv_file_server_host)

def hander(
        consumer,
        msg,
        data,
        kafka_record
):
    """
    Hàm thực hiện 1 message nhận được từ kafka
    """

    assert isinstance(consumer, KafkaConsumer), "consumer must be kafka.consumer.group.KafkaConsumer"
    assert isinstance(msg, dict), "msg must be kafka.consumer.group.KafkaConsumer"
    assert isinstance(data, dict), "data must be kafka.consumer.group.KafkaConsumer"
    """

    """

    upload_info = data["UploadInfo"]  # lấy toàn bộ thông tin upload
    upload_id = upload_info["UploadId"]  # thông tin upload id
    server_file_name = upload_info["ServerFilename"]
    app = data["Application"]  # thông tin app đang sử dụng
    app_name = app["Name"]  # lấy app name
    file_ext = upload_info["FileExt"]

    assert isinstance(upload_info, dict), 'Argument of wrong type!'

    mime_type = upload_info["MimeType"]

    if 'audio/' in mime_type:  # file âm thanh bỏ qua
        return
    if 'video/' in mime_type:  # file video bỏ qua
        return
    access_token_key = data["AccessTokenKey"]  # thẻ truy cập
    request_download_key = data[
        "RequestDownloadKey"]  # request kay name exampel www.example.com?<request_download_key>=<AccessTokenKey>
    url_of_file = upload_info["UrlOfFile"]  # url để download file
    url_download = "{}?{}={}".format(url_of_file, request_download_key, access_token_key)
    settings.logger.info(url_download)
    download_to = os.path.join(settings.ocr_in_directory,
                               "{}.{}".format(upload_id, file_ext))  # đường dẫn đến file sau khi download
    process_to = os.path.join(settings.ocr_out_directory,
                              "{}.{}".format(upload_id, file_ext))  # đường dẫn đến file sau khi xử lý
    settings.logger.info(download_to)
    if not os.path.isfile(download_to):
        try:
            lv_mongo_db.save_mongodb_file_fs_with_file_name_to(
                db_name=app_name,
                file_name=server_file_name,
                path_to_save=download_to
            )
        except Exception as e:
            settings.logger.info("{} is not exist".format(download_to))
            consumer.commit()


            return
        #download(url_download, download_to, 1024 * 1024 * 5)  # tải nội dung
    if file_ext == 'pdf':  # Nếu là file pdf
        if not os.path.isfile(process_to):  # nếu chưa xử lý
            error, ret = run_ocrmypdf(  # xử lý orc
                in_put=download_to,
                out_put=process_to
            )
            if error:  # Quá trình xử lý bị lỗi
                print("OCR is Error")
                settings.logger.debug("OCR is Error")
                print(error)
                settings.logger.debug(error)
                dispatcher(download_to, app_name)  # chuyển sang quá trình đọc text trong file pdf

            else:
                print("ocr file '{}' is ok".format(download_to))
                settings.logger.info("ocr file to '{} is ok'".format(process_to))
                print("update '{}' to '{}'".format(process_to, upload_id))
                settings.logger.info("update '{}' to '{}'".format(process_to, upload_id))

                error, ret = do_update_pdf_content(
                    app_name=app_name,
                    upload_id=upload_id,
                    file_content_path=process_to
                )
                if error:
                    print("update '{}' to '{}' is error".format(process_to, upload_id))
                    settings.logger.debug(error)
                else:
                    print("Transfer '{}' to Elasticsearch content".format(process_to))
                    settings.logger.info("Transfer '{}' to Elasticsearch content".format(process_to))
                    error, ret = dispatcher(process_to, app_name)
                    if error:
                        print("Transfer '{}' to Elasticsearch content is error".format(process_to))
                        print(error)
                        settings.logger.debug("Transfer '{}' to Elasticsearch content is error".format(process_to))
                        settings.logger.debug(error)
                    else:

                        consumer.commit()
                        print("Process {} is total complete".format(upload_id))
                        settings.logger.info("Process {} is total complete".format(upload_id))
        else:
            print("ocr file '{}' is ok".format(download_to))
            settings.logger.info("ocr file to '{} is ok'".format(process_to))
            print("update '{}' to '{}'".format(process_to, upload_id))
            settings.logger.info("update '{}' to '{}'".format(process_to, upload_id))

            error, ret = do_update_pdf_content(
                upload_id=upload_id,
                app_name= app_name,
                file_content_path=process_to
            )
            if error:
                print("update '{}' to '{}' is error".format(process_to, upload_id))
                settings.logger.debug(error)
            else:
                print("Transfer '{}' to Elasticsearch content".format(process_to))
                settings.logger.info("Transfer '{}' to Elasticsearch content".format(process_to))
                error, ret = dispatcher(process_to, app_name)
                if error:
                    print("Transfer '{}' to Elasticsearch content is error".format(process_to))
                    print(error)
                    settings.logger.debug("Transfer '{}' to Elasticsearch content is error".format(process_to))
                    settings.logger.debug(error)
                else:

                    consumer.commit()
                    print("Process {} is total complete".format(upload_id))
                    settings.logger.info("Process {} is total complete".format(upload_id))

    elif 'image/' in mime_type:
        pdf_file_path_convert = os.path.join(settings.ocr_in_directory, "{}.pdf".format(upload_id))
        if not os.path.isfile(pdf_file_path_convert):
            error, ret = convert_image_to_pdf(download_to, pdf_file_path_convert)
            if error:
                settings.logger.debug(error)
                print(error)
        else:
            process_to = os.path.join(settings.ocr_out_directory, "{}.pdf".format(upload_id))
            print("OCR file {}".format(pdf_file_path_convert))
            settings.logger.info("OCR file {}".format(pdf_file_path_convert))
            error, ret = run_ocrmypdf(
                in_put=pdf_file_path_convert,
                out_put=process_to
            )
            if error:
                print("OCR file {} is error".format(pdf_file_path_convert))
                settings.logger.debug("OCR file {} is error".format(pdf_file_path_convert))
                settings.logger.debug(error)
            else:
                print("OCR file {} is ok".format(process_to))
                settings.logger.info("OCR file {} is ok".format(process_to))
                print("Update content to {} by {}".format(upload_id, process_to))
                settings.logger.info("Update content to {} by {}".format(upload_id, process_to))
                error, ret = do_update_add_content(

                    app_name= app_name,
                    upload_id=upload_id,
                    file_content_path=process_to
                )
                if error:
                    print("Update content is Error")
                    settings.logger.debug("Update content is Error")
                    settings.logger.debug(error)
                else:
                    print("Transfer to Elasticsearch content")
                    error, ret = dispatcher(pdf_file_path_convert, app_name)
                    if error:
                        print("Transfer to Elasticsearch content is error")
                        print(error)
                        settings.logger.debug("Transfer to Elasticsearch content is error")
                        settings.logger.debug(error)
                    else:

                        consumer.commit()
                        print("Process {} is total complete".format(upload_id))
                        settings.logger.info("Process {} is total complete".format(upload_id))
        if not os.path.isfile(process_to):
            error, ret = run_ocrmypdf(
                in_put=pdf_file_path_convert,
                out_put=process_to
            )
            if error:
                print("error")
                settings.logger.debug("OCR is Error")
                settings.logger.debug(error)
            else:
                process_to = os.path.join(settings.ocr_out_directory, "{}.pdf".format(upload_id))
                print("ocr file '{}' is ok".format(pdf_file_path_convert))
                settings.logger.info("ocr file '{}' is ok".format(pdf_file_path_convert))
                print("ocr file to '{}'".format(process_to))

                settings.logger.info("ocr file to '{}'".format(process_to))

                error, ret = do_update_add_content(
                    app_name=app_name,
                    upload_id=upload_id,
                    file_content_path=process_to
                )
                if error:
                    print("Update content is Error")
                    settings.logger.debug("Update content is Error")
                    settings.logger.debug(error)
                else:
                    print("Transfer to Elasticsearch content")
                    error, ret = dispatcher(process_to, app_name)
                    if error:
                        print("Transfer to Elasticsearch content is error")
                        print(error)
                        settings.logger.debug("Transfer to Elasticsearch content is error")
                        settings.logger.debug(error)
                    else:
                        consumer.commit()
                        print("Process {} is total complete".format(upload_id))
                        settings.logger.info("Process {} is total complete".format(upload_id))
    else:
        error, ret = dispatcher(download_to, app_name)
        if error:
            print("Transfer to Elasticsearch content is error")
            print(error)
            settings.logger.debug("Transfer to Elasticsearch content is error")
            settings.logger.debug(error)
        else:
            consumer.commit()
            print("Process {} is total complete".format(upload_id))
            settings.logger.info("Process {} is total complete".format(upload_id))
