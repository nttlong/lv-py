import threading
import pymongo
import os
import yaml
import gridfs
import bson
from .mongodb_obj import MongoDbItem

__working_folder__ = None
__connection__: None = None  # Biến toàn cục

__lock__ = threading.Lock()  # lock dùng để bảo đảm duy nhất có 1 connection đến Mongodb

__settings__ = None

__path_to_yaml_settings__ = None

__master_db_name__ = None


def __get_mongod_db_connection_string__():
    """
    'mongodb://user:passwd@node1:p1,node2:p2/?replicaSet=rsname'
    """
    if not __path_to_yaml_settings__:
        raise Exception("Please call {}.{}".format(__name__, "set_working_folder"))
    if not isinstance(__settings__, dict):
        raise Exception("Please call {}.{}".format(__name__, "set_working_folder"))
    mongo_config = __settings__.get("mongodb", None)
    if not isinstance(mongo_config, dict):
        raise Exception("{} in {} was not found or invalid value".format(__name__, "set_working_folder"))
    global __master_db_name__
    __master_db_name__ = mongo_config.get("db-auth", None)
    ret = "mongodb://{}:{}@{}/{}?replicaSet={}".format(
        mongo_config.get("username", None),
        mongo_config.get("password", None),
        mongo_config.get("servers", None),
        mongo_config.get("db-auth", None),
        mongo_config.get("replace-set", None)

    )
    return ret


def __do_connect_to_mongodb__():
    global __connection__
    global __lock__

    if not __connection__:
        __lock__.acquire()
        cnn = __get_mongod_db_connection_string__()
        __connection__ = pymongo.MongoClient(cnn)
        __lock__.release()
    return __connection__


def set_working_folder(working_folder):
    """
    cài đặt thư mục làm việc, thông tin này dùng để đọc các file cấu hình
    """
    global __settings__
    global __path_to_yaml_settings__
    assert isinstance(working_folder, str), 'working_folder phải là kiểu str'
    if not os.path.isdir(working_folder):
        raise Exception("'{}' was not found".format(working_folder))
    __path_to_yaml_settings__ = os.path.join(working_folder, "settings.yaml")
    if not os.path.isfile(__path_to_yaml_settings__):
        raise Exception("'{}' was not found".format(__path_to_yaml_settings__))
    parsed_yaml = None
    with open(
            __path_to_yaml_settings__,
            mode="r",
            encoding="utf-8") as stream:
        __settings__ = yaml.safe_load(stream)
    __do_connect_to_mongodb__()


def get_mongodb_connection():
    """
    Lấy connection đến mongodb
    """
    return __do_connect_to_mongodb__()


def get_master_db():
    """
    Lấy Database chính
    """
    assert isinstance(__connection__, pymongo.MongoClient)
    __do_connect_to_mongodb__()
    return __connection__.get_database(__master_db_name__)


def get_db(db_name):
    __do_connect_to_mongodb__()
    assert isinstance(__connection__, pymongo.MongoClient)
    db = __connection__.get_database(db_name)
    return db


def get_all_apps():
    """
    Lấy toàn bộ thông tin sys_applications
    """
    return list(get_master_db().get_collection('sys_applications').find({}))


def get_gridfs(db_name) -> gridfs.GridFS:
    """
    Lấy girid fs để truy cập vào mongodb file system
    """
    db = get_db(db_name)
    return gridfs.GridFS(db)


def get_mongodb_file_by_file_name(db_name, file_name) -> gridfs.grid_file.GridOut:
    """
    Lấy file grid trong mongodb
    """
    return get_gridfs(db_name).find_one({"filename": file_name})


def get_mongodb_file_by_file_id(db_name, file_id) -> gridfs.grid_file.GridOut:
    """
    Lấy file grid trong mongodb với đường dẫn được chỉ định trong path_to_save (bao gồm cả thên file)

    """
    assert isinstance(file_id, bson.objectid.ObjectId), 'id must be pymongo.bson.objectid.ObjectId'
    return get_gridfs(db_name).get(file_id)


def save_mongodb_file_fs_to(fs, path_to_save, read_chunk_in_KB=1024):
    """
    Lấy toàn bô nôi dung của file fs và gi vào vi trí vật lý của ổ cứng
    get content of mongodb file grid then save to physical location
    (path_to_save determine physical location, path_to_save must include physical filename)
    """
    assert isinstance(fs, gridfs.grid_file.GridOut), 'fs must be gridfs.grid_file.GridOut'
    assert isinstance(path_to_save, str), 'path_to_save must be str'
    size_to_read = read_chunk_in_KB * 1024
    outputdata = fs.read(size_to_read)
    output = open(path_to_save, "wb")
    try:
        while outputdata.__len__() > 0:
            output.write(outputdata)
            outputdata = fs.read(size_to_read)
    except Exception as e:
        raise e
    finally:
        output.close()


def save_mongodb_file_fs_with_file_name_to(db_name, file_name, path_to_save, read_chunk_in_KB=1024):
    """
    Đọc nội dung file trong mongodb và lưu vào file  với đường dẫn được chỉ định trong path_to_save
    """
    fs = get_mongodb_file_by_file_name(db_name, file_name)
    if not isinstance(fs, gridfs.grid_file.GridOut):
        raise FileNotFoundError("'{}' in '{}' was not found".format(file_name, db_name))
    save_mongodb_file_fs_to(fs, path_to_save, read_chunk_in_KB)


def create_mongodb_fs_from_file(
        db_name,
        full_path_to_file) -> gridfs.grid_file.GridIn:
    """
    Tạo file trong mongodb theo noi dung nam trong full_path_to_file

    """
    try:
        dir_path, file_name = os.path.split(full_path_to_file)
        g = get_gridfs(db_name)

        fs = g.new_file()
        fs.name = file_name
        fs.filename = file_name
        assert isinstance(fs, gridfs.grid_file.GridIn)

        with open(full_path_to_file, 'rb') as r_file:
            read_data = r_file.read(fs.chunk_size)
            while read_data.__len__() > 0:
                fs.write(read_data)
                read_data = r_file.read(fs.chunk_size)

    except Exception as e:
        raise e
    finally:
        fs.close()
    return fs


def get_upload_info_by_upload_id(db_name, upload_id):
    """
    Lấy thông tin upload theo upload id
    """
    assert isinstance(db_name, str), "db_name must be str"
    assert isinstance(upload_id, str), "db_name must be str"
    ret = get_db(db_name).get_collection("DocUploadRegister").find_one({
        "_id": upload_id
    })
    if ret:
        return MongoDbItem(ret)
    else:
        return None


def update_content_of_upload_info_by_upload_id(db_name, upload_id, file_name):
    """
    Cập nhật lại nội dung cùa upload_id
    """
    assert isinstance(db_name, str), "db_name must be str"
    assert isinstance(upload_id, str), "upload_id must be str"
    assert isinstance(file_name, str), "file_name must be str"

    upload_item = get_upload_info_by_upload_id(  # lấy thông tin upload
        db_name=db_name,
        upload_id=upload_id
    )
    if not upload_item:  # Nếu không tồn tại upload
        print("Upload with {} was not found".format(upload_id))  # Thông báo
        return  # Kết thúc
    if not os.path.isfile(file_name):
        raise FileNotFoundError()
    new_fs = create_mongodb_fs_from_file(  # Tải nội dung mới
        db_name=db_name,
        full_path_to_file=file_name
    )
    db_docs = get_db(db_name)  # truy cập vào database tanent
    """
    Đánh dấu xóa file cũ
    """
    db_docs.get_collection("fs.files").update_one(
        {
            "filename": upload_item.ServerFileName
        }, {
            "$set": {"filename": "delete." + upload_item.ServerFileName}
        }
    )

    """
    Cập nhật nội dung mới
    """
    ret_update = db_docs.get_collection("fs.files").update_one(
        {
            "_id": new_fs._id}, {
            "$set": {
                "filename": upload_item.ServerFileName
            }
        }
    )
    if ret_update.matched_count > 0:
        """
        Cập nhật nộ dung mới thành công
        Xóa nội dung cũ
        """
        db_docs.get_collection("fs.files").delete_one(
            {
                "filename": "delete." + upload_item.ServerFileName
            }
        )
    else:
        """
        Không thành công trả lại nội dung cũ
        """
        db_docs.get_collection("fs.files").update_one(
            {
                "filename": "delete." + upload_item.ServerFileName
            },
            {
                "$set": {"filename": upload_item.ServerFileName}
            }
        )


def add_more_content_to_upload_by_upload_id(
        db_name,
        attr_name,
        upload_id,
        file_name
):
    """
    Thêm nội dung file cho upload
    """
    assert isinstance(attr_name, str), "attr_name must be str"
    assert isinstance(db_name, str), "db_name must be str"
    assert isinstance(upload_id, str), "upload_id must be str"
    assert isinstance(file_name, str), "file_name must be str"

    upload_item = get_upload_info_by_upload_id(  # lấy thông tin upload
        db_name=db_name,
        upload_id=upload_id
    )
    if not upload_item:  # Nếu không tồn tại upload
        print("Upload with {} was not found".format(upload_id))  # Thông báo
        return  # Kết thúc
    if not os.path.isfile(file_name):
        raise FileNotFoundError()
    new_fs = create_mongodb_fs_from_file(  # Tải nội dung mới
        db_name=db_name,
        full_path_to_file=file_name
    )
    db_docs = get_db(db_name)  # truy cập vào database tanent

    db_docs.get_collection("DocUploadRegister").update_one({
        "_id": upload_item._id,
    }, {
        "$set": {
            attr_name: new_fs.filename
        }
    })


def add_ocr_pfd_for_image_upload(
        db_name,
        upload_id,
        file_name
):
    """
    PdfFileServer
    """
    add_more_content_to_upload_by_upload_id(
        db_name,
        "PdfFileServer",
        upload_id,
        file_name
    )
