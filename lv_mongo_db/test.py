import lv_mongo_db
import gridfs
test_db_name ="app-test-dev"
lv_mongo_db.set_working_folder(r'C:\lv-py')
test =r'0efefdf2-10d8-4151-a7af-a1d5e72b705d.pdf'

# lv_mongo_db.save_mongodb_file_fs_with_file_name_to(
#     db_name=test_db_name,
#     file_name= r'\\192.168.18.36\ocr\docs\out\0efefdf2-10d8-4151-a7af-a1d5e72b705d.pdf'
# )

g = lv_mongo_db.get_gridfs(test_db_name)
tt =g.find_one({
    "filename":"Ok.png"
})

lst =list(lv_mongo_db.get_db(db_name=test_db_name).list_collection_names())
print(lst)
upload_id ='07ec1951-800f-4edc-96d3-04dca15b7c55'
upload_item =lv_mongo_db.get_upload_info_by_upload_id(db_name=test_db_name,upload_id=upload_id)

lv_mongo_db.update_content_of_upload_info_by_upload_id(
    db_name=test_db_name,
    file_name=r'\\192.168.18.36\ocr\docs\out\07ec1951-800f-4edc-96d3-04dca15b7c55.pdf',
    upload_id= upload_id
)
print("Xong")