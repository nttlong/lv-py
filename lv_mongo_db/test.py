import lv_mongo_db
import gridfs
lv_mongo_db.set_working_folder(r'C:\lv-py')
test =r'5e00f014-d67d-4980-b905-d1051259a01d.delete..png'

fs = lv_mongo_db.get_mongodb_file_by_file_name("app-test-dev", test)
lv_mongo_db.save_mongodb_file_fs_to(fs,r'C:\lv-py\docs\in\test.png')
