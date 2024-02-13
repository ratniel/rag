from preprocessing_utils import delete_files_except_html, delete_empty_dirs, save_clean_html, save_clean_txt
from pathlib import Path
import pickle

dir_path = "./data/raw_data"
delete_files_except_html(path=dir_path)
delete_empty_dirs(path=dir_path)

#load the file_paths list from file_paths.pkl
with open("file_paths.pkl", "rb") as f:
    file_paths = pickle.load(f)

#append the file paths
file_paths = [dir_path + "/" + file for file in file_paths]


#save the clean html files and clean text files
for file_path in file_paths:
    try:
        save_clean_html(filepath=file_path, save_location="./data/clean_html")
    except Exception as e:
        print(f"Error occurred while saving clean HTML file: {e}")

    try:
        save_clean_txt(filepath=file_path, save_location="./data/clean_text")
    except Exception as e:
        print(f"Error occurred while saving clean text file: {e}")