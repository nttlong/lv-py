import pymongo
import gridfs
import os
from pathlib import Path
import shutil
import logging
ignore_list = [
    'mp3',
    'mp4',
    'exe',
    'dll'
]
fs_craler_path = r'\\192.168.18.36\fscrawler-es7-2.9\docs'
working_dir = Path(os.path.dirname( __file__)).parent.absolute()
log_path = os.path.join(working_dir, "fscrawler_logs")
if not os.path.isdir(log_path):
    os.mkdir(log_path)
logger = logging.getLogger()
logger.setLevel(
    logging.DEBUG

)
__logger_info_handler__ = logging.FileHandler(os.path.join(log_path, 'logs.txt'))
logger.addHandler(__logger_info_handler__)

fs_craler_path_tmp =os.path.join(Path(os.path.dirname( __file__)).parent.absolute(),"fs_craler_tmp")
if not os.path.isdir(fs_craler_path_tmp):
    os.mkdir(fs_craler_path_tmp)
cnn = pymongo.MongoClient('mongodb://admin-doc:123456@192.168.18.36:27018/lv-docs?replicaSet=rs0')
def get_all_app():
    db_docs=cnn["lv-docs"]
    apps = db_docs["sys_applications"].find()
    return list(apps)
def run_in_app(app):
    app_id = app['_id']
    print('app id={}'.format(app_id))

    app_name = app['Name']
    fs_craler_path_to_app = os.path.join(fs_craler_path,app_name)
    fs_craler_path_to_app_tmp =os.path.join(fs_craler_path_tmp, app_name)

    if not os.path.isdir(fs_craler_path_to_app):
        os.mkdir(fs_craler_path_to_app)
    if not os.path.isdir(fs_craler_path_to_app_tmp):
        os.mkdir(fs_craler_path_to_app_tmp)
    print('app name={}'.format(app_name))
    app_db = cnn[app_name]
    app_fs = gridfs.GridFS(app_db)
    doc_upload_register_coll =app_db['DocUploadRegister']
    doc_upload_registers = doc_upload_register_coll.find()
    for doc in doc_upload_registers:
        if doc['FileExt'] in ignore_list:
            continue
        try:
            fs_file =  os.path.join(fs_craler_path_to_app,doc["ServerFileName"])
            if not os.path.isfile(fs_file):
                file = app_fs.find_one({"filename": doc["ServerFileName"]})
                fs_tmp_file = os.path.join(fs_craler_path_to_app_tmp,doc["ServerFileName"])
                if os.path.isfile(fs_tmp_file):
                    os.remove(fs_tmp_file)
                if isinstance(file, gridfs.grid_file.GridOut):
                    file_reader = app_fs.get(file._id).read()
                    with open(fs_tmp_file, 'wb') as f:
                        f.write(file_reader)
                        f.flush()
                        os.fsync(f.fileno())
                    shutil.move(fs_tmp_file, fs_file)
                    print("{} is ok".format(fs_tmp_file))
                    print("{} has been move to {}".format(fs_tmp_file, fs_file))
                    logger.info("{} has been move to {}".format(fs_tmp_file, fs_file))

        except Exception as e:
            logger.debug(e)



