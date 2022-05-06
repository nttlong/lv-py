import settings
import os
from pathlib import Path
import shutil

def dispatcher(input_file, app_name):
    """
    Chuy?n ti?p x? ly
    """
    try:
        assert isinstance(input_file, str),'H?nh nhu thi?u ho?c sai ki?u input_file , input_file ph?i l? str'
        assert isinstance(app_name, str), 'H?nh nhu thi?u ho?c sai ki?u app_name, app_name ph?i l? str'

        directory_of_app_in_fs_crawler = os.path.join(settings.fs_crawler_path, app_name)
        if not os.path.isdir(directory_of_app_in_fs_crawler):  # ki?m tra n?u chua c? thu m?c
            os.mkdir(directory_of_app_in_fs_crawler)  # t?o lu?n
        # move_to_path = os.path.join(
        #     directory_of_app_in_fs_crawler,
        #     Path(input_file).name
        # )  # T?o du?ng d?n file d? chu?n b? chuy?n ti?p
        ret = shutil.move(input_file, directory_of_app_in_fs_crawler)
        return  None, ret
    except Exception as e:
        return  e,None



