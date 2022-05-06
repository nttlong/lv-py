"""
this source code describe a class callback to file server
Client api g?i v? d?ch v? file
"""
import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import io
import shutil
import datetime
from array import array
class api:
    """
    class to invoke file server
    """
    def __init__(self, host_url):
        """
        init a new api caller
        :param host_url:host of lacviet files client
        """
        assert isinstance(host_url,str),"host_url must be str"
        if host_url.__len__() == 0:
            raise Exception("host_url is empty")
        self.__host_url__ = host_url

    def post(self, rel_api_path, data):
        """
        Tri?u h?i request post,

        :param rel_api_path: the relative path to api looks like /api/default/LV-Accounts/Users/GetCurrentUserInfo (?u?ng d?n tuong d?i d?n Api)
        :param data: dictionary data to post
        :return:
        """
        assert isinstance(data, dict),'Data must be a dictionary type (sai ki?u d? li?u)'
        assert isinstance(rel_api_path,str), 'rel_api_path must be a text'
        if rel_api_path[0] != '/':
            raise Exception('rel_api_path must start with /')
        request_url = self.__host_url__ + rel_api_path
        response = requests.post(request_url,json = data)
        assert isinstance(response, requests.models.Response), 'requests.post return wrontype'
        try:
            return response.json()
        except:
            return str(response.content).split("'")[1]

    def post_binary(self, rel_api_path, data,data_key,file_part, file_part_key):
        assert isinstance(file_part,bytes)
        request_url = self.__host_url__ + rel_api_path
        mp_encoder = MultipartEncoder(
            fields={
                data_key: json.dumps(data),
                # plain file object, no filename or mime type produces a
                # Content-Disposition header with just the part name
                file_part_key: (file_part_key+".txt", file_part, 'text/plain'),
            }
        )
        r = requests.post(
            request_url,
            data=mp_encoder,  # The MultipartEncoder is posted as data, don't use files=...!
            # The MultipartEncoder provides the content-type header with the boundary:
            headers={'Content-Type': mp_encoder.content_type}
        )
        assert isinstance(r,requests.models.Response),'requests.post return wrontype'
        return  r.json()

    def get_access_token(self,app_id,secret_key):
        """
        get access token by app id and secret key
        :param app_id:
        :param secret_key:
        :return:
        """
        assert isinstance(app_id,str),'api_id must be str'
        assert isinstance(secret_key, str), 'api_id must be str'
        ret = self.post("/api/default/LV-Accounts/Users/GetAccessToken",{
            "AppId" : app_id,
            "SecretKey" : secret_key
        })
        return ret

    def register_upload(self, access_token, register_info):
        """
        Register a new upload
        :param access_token: access token
        :param register_info:
        :return:
        """
        assert isinstance(access_token,str),'access_token must be a text'
        assert isinstance(register_info, dict), 'access_token must be a dict'
        assert isinstance(register_info["FileName"],str),'register_info["FileName"] must be text '
        assert isinstance(register_info["SizeInBytes"],int),'register_info["SizeInBytes"] must be int '
        assert isinstance(register_info["ChunkSizeInKB"],int),'register_info["ChunkSizeInKB"] must be int '
        assert isinstance(register_info["IsPublic"], bool), 'register_info["IsPublic"] must be bool '
        assert isinstance(register_info["ThumbSize"],dict),'register_info["ThumbSize"] must be dict '
        assert isinstance(register_info["ThumbSize"]["Width"], int), 'register_info["ThumbSize"]["Width"] must be int '
        assert isinstance(register_info["ThumbSize"]["Height"], int), 'register_info["ThumbSize"]["Height"] must be int '
        ret = self.post('/api/default/LV-Media/content/Register',{
            "AccessToken":access_token,
            "RegisterInfo":register_info
        })
        return ret

    def upload_chunk(self, access_token, upload_id, index, file_part_content):
        """
        Upload chunk
        """

        assert isinstance(access_token, str), 'access_token mus be str'
        assert isinstance(index, int), 'index mus be int'
        assert isinstance(file_part_content, bytes), 'access_token mus be bytes'
        rs = self.post_binary("/api/default/LV-Media/content/UploadChunk", {
            "AccessToken": access_token,
            "Data": {
                "UploadId": upload_id,
                "Index": index
            }
        }, "Data", file_part_content, "FilePart")
        return rs

    def upload_update_chunk(self, access_token, upload_id,size_in_byte, index, file_part_content):
        """
        Upload chunk for Update new content
        """
        assert isinstance(access_token, str), 'access_token mus be str'
        assert isinstance(index, int), 'index mus be int'
        assert  isinstance(size_in_byte,int), 'chunk_size_in_byte must be int'
        assert isinstance(file_part_content, bytes), 'access_token mus be bytes'
        rs = self.post_binary("/api/default/LV-Media/content/UpdateContentChunk", {
            "AccessToken": access_token,
            "UploadId":upload_id,
            "Index": index,
            "FileSizeInBytes":size_in_byte
        }, "Data", file_part_content, "FilePart")
        return rs

    def upload_add_pdf_content_chunk(self, access_token, upload_id,size_in_byte, index, file_part_content):
        """
        D?ng d? th?m n?i dung pdf file sau thi th?c hi?n OCR tr?n file ?nh
        """
        assert isinstance(access_token, str), 'access_token mus be str'
        assert isinstance(index, int), 'index mus be int'
        assert  isinstance(size_in_byte,int), 'chunk_size_in_byte must be int'
        assert isinstance(file_part_content, bytes), 'access_token mus be bytes'
        rs = self.post_binary("/api/default/LV-Media/content/PdfConvert_ChunkUpdate", {
            "AccessToken": access_token,
            "UploadId":upload_id,
            "Index": index,
            "FileSizeInBytes":size_in_byte
        }, "Data", file_part_content, "FilePart")
        return rs

    def upload_file(self,access_token, file_path,chunk_size_in_kbyte,is_pblic):
        """
        Upload file
        :param access_token:
        :param file_path:
        :param chunk_size_in_kbyte:
        :return:
        """
        assert isinstance(access_token,str),'acccess_token must be str'
        assert isinstance(file_path, str), 'file_path must be str'
        assert isinstance(chunk_size_in_kbyte,int) , 'chunk_size_in_kbyte must be int'
        assert chunk_size_in_kbyte> 0 ,'chunk_size_in_kbyte must greater than zero'
        assert chunk_size_in_kbyte <=2*1024, 'chunk_size_in_kbyte must less than or equal  2MB'

        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        r = self.register_upload(access_token, {

            "FileName": file_name,
            "SizeInBytes": file_size,
            "ChunkSizeInKB": chunk_size_in_kbyte,
            "IsPublic": is_pblic,
            "ThumbSize": {
                "Width": 300,
                "Height": 300
            }

        })
        assert isinstance(r,dict),'api.register_upload return wrong type, it mus return dict'
        error = r.get("error",None)
        if error is not None and isinstance(error, dict):
            raise Exception(error["message"])
        upload_id = r["data"]["id"]
        size = chunk_size_in_kbyte * 1024
        bff = io.open(
            file_path, "rb")
        try:

            data = bff.read(size)
            index = 0
            while data.__len__() > 0:

                res = self.upload_chunk(access_token, upload_id, index, data)
                index = index + 1
                assert isinstance(res, dict), 'api.upload_chunk return wrong type, it mus return dict'
                error = res.get("error",None)
                if error != None and isinstance(error,dict):
                    raise Exception(error["message"])
                data = bff.read(size)
            return r.get("data",None)
        finally:
            bff.close()

        bff.close()



    def upload_update_content_file(self, access_token,upload_id, file_path, chunk_size_in_kbyte):
        """
        C?p nh?t n? dung kh?c cho m?t upload da t?n t?i tru?c d?
        Thao t?c n?y thu?ng d?ng d? c?p nh?t l?i n?i dung c?a 1 file PDF da du? OCR v? b?c th?m 1 l?p text
        (G?i l? PDF/A)
        C? nghia l? sau khi th?c hi?n PDF/A cho 1 file PDF file g?c s? ph?i b? thay th? b?ng file m?i
        """
        assert isinstance(access_token, str), 'acccess_token must be str'
        assert isinstance(file_path, str), 'file_path must be str'
        assert isinstance(chunk_size_in_kbyte, int), 'chunk_size_in_kbyte must be int'

        assert chunk_size_in_kbyte > 0, 'chunk_size_in_kbyte must greater than zero'
        assert chunk_size_in_kbyte <= 2 * 1024, 'chunk_size_in_kbyte must less than or equal  2MB'

        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)

        size = chunk_size_in_kbyte * 1024
        bff = io.open(
            file_path, "rb")
        try:

            data = bff.read(size)
            index = 0
            while data.__len__() > 0:

                res = self.upload_update_chunk(access_token, upload_id,file_size, index,data)
                index = index + 1
                assert isinstance(res, dict), 'api.upload_chunk return wrong type, it mus return dict'
                error = res.get("error", None)
                if error != None and isinstance(error, dict):
                    raise Exception(error["message"])
                data = bff.read(size)
                print("upload {} file {}".format(index,file_path))
            return res.get("data", None)
        except Exception as e:
            print("Upload is error")
            raise e
        finally:
            bff.close()

        bff.close()

    def upload_add_pdf_content_file(self, access_token,upload_id, file_path, chunk_size_in_kbyte):
        """
        Th?m file pdf cho Upload da c? tru?c d? (d?ng d? b? sung n?i dung OCR cho file ?nh)
        ??i v?i file ?nh sau khi th?c hi?n ORC xong, h? th?ng s? t5ao th?m 1 file m?i da du?c th?c hi?n
        taho t?c PDF/A tr?n file ?nh g?c (V? file ?nh kh?ng th? ch?m th?m n?i dung text
        n?n h? th?ng s? ph?i ph?t sinh m?t file pdf tuong ?ng v?i file ?nh g?c v? k?m theo n?i dung text)
        """
        assert isinstance(access_token, str), 'acccess_token must be str'
        assert isinstance(file_path, str), 'file_path must be str'
        assert isinstance(chunk_size_in_kbyte, int), 'chunk_size_in_kbyte must be int'

        assert chunk_size_in_kbyte > 0, 'chunk_size_in_kbyte must greater than zero'
        assert chunk_size_in_kbyte <= 2 * 1024, 'chunk_size_in_kbyte must less than or equal  2MB'

        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)

        size = chunk_size_in_kbyte * 1024
        bff = io.open(
            file_path, "rb")
        try:

            data = bff.read(size)
            index = 0
            while data.__len__() > 0:

                res = self.upload_add_pdf_content_chunk(access_token, upload_id,file_size, index,data)
                index = index + 1
                assert isinstance(res, dict), 'api.upload_chunk return wrong type, it mus return dict'
                error = res.get("error", None)
                if error != None and isinstance(error, dict):
                    raise Exception(error["message"])
                data = bff.read(size)
                print("upload {} file {}".format(index,file_path))
            return res.get("data", None)
        except Exception as e:
            print("Upload is error")
            raise e
        finally:
            bff.close()

        bff.close()



    def download_file(self,url,save_to_file):
        response = requests.get(url)
        open(save_to_file, "wb").write(response.content)


def download(url: str, file_path,chunk_size):
    r = requests.get(url, stream=True)
    len = int(r.headers.get("Content-Length",0))
    total = 0
    print("size is:",len)
    if r.ok:
        print("saving to", file_path)
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                assert isinstance(chunk,bytes)
                if chunk:
                    total = total + chunk.__len__()
                    print("[",round(total/len,2)*100,"%]--",file_path)
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        raise Exception("Download failed: status code {}\n{}".format(r.status_code, r.text))
    print("download is complete")

def download_file(url,file_path):
    local_filename = file_path
    n = datetime.datetime.now()
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    t = (datetime.datetime.now()-n).total_seconds()
    print('spent {}to download {}'.format(t,url))
    return local_filename







