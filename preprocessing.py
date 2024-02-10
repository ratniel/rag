from preprocessing_utils import delete_files_except_html, delete_empty_dirs, save_clean_file
from pathlib import Path
import glob

dir_path = "./data"
delete_files_except_html(path=dir_path)
delete_empty_dirs(path=dir_path)

#get all the file paths in dir and subdirs
file_paths = [str(file_path) for file_path in Path(dir_path).rglob('*') if file_path.is_file()]

#save the clean files
for file_path in file_paths:
    save_clean_file(Path(file_path))