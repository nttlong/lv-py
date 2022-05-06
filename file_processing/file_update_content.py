
def do_update_pdf_content(
        api_call,
        access_token_key,
        upload_id,
        file_content_path
):
    try:
        ret= api_call.upload_update_content_file(
            access_token_key,
            upload_id,
            file_content_path,
            1024
        )
        return None, ret
    except Exception as e:
        return e, None
def do_update_add_content(
        api_call,
        access_token_key,
        upload_id,
        file_content_path
):
    try:
        ret =api_call.upload_add_pdf_content_file(
            access_token_key,
            upload_id,
            file_content_path,
            1024*2
        )
        return None,ret
    except Exception as e:
        return e, None
