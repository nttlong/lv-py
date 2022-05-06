import lv_mongo_db
def do_update_pdf_content(
        app_name,
        upload_id,
        file_content_path
):
    assert isinstance(app_name,str),'app_name must be str '
    assert isinstance(file_content_path,str) ,'file_content_path must be str'
    try:
        ret = lv_mongo_db.update_content_of_upload_info_by_upload_id(
            db_name=app_name,
            file_name=file_content_path,
            upload_id=upload_id

        )
        # ret= api_call.upload_update_content_file(
        #     access_token_key,
        #     upload_id,
        #     file_content_path,
        #     1024
        # )
        return None, ret
    except Exception as e:
        return e, None
def do_update_add_content(
        app_name,
        upload_id,
        file_content_path
):
    assert isinstance(app_name,str),'app_name must be str'
    try:
        ret = lv_mongo_db.add_ocr_pfd_for_image_upload(
            db_name=app_name,
            upload_id=upload_id,
            file_name= file_content_path
        )
        # ret =api_call.upload_add_pdf_content_file(
        #     access_token_key,
        #     upload_id,
        #     file_content_path,
        #     1024*2
        # )
        return None,ret
    except Exception as e:
        return e, None
