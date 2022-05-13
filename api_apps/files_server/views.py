import os
import re
import mimetypes
from wsgiref.util import FileWrapper

from django.http.response import StreamingHttpResponse
range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)


class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data
def stream_video(request, path):
    import re_faster.re_streaming
    #http://192.168.18.36:5010/api/default/LV-Media/content/source/hps-file-test/c867ad74-c59e-4013-88e4-eb010994171e.mp4
    Upload_id="c867ad74-c59e-4013-88e4-eb010994171e"
    app_name = "hps-file-test"
    import lv_mongo_db
    lv_mongo_db.set_working_folder(r'C:\lv-py')
    db =lv_mongo_db.get_db(app_name)
    gridfs = lv_mongo_db.get_gridfs(db_name=app_name)
    file = gridfs.find_one({
        "filename":Upload_id+".mp4"
    })

    return re_faster.re_streaming.streaming_mongo_db_fs(request,file)