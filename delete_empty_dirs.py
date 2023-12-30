import os

def delete_empty_dirs(path):
    for dirpath, dirnames, files in os.walk(path, topdown=False):
        if not dirnames and not files:
            os.rmdir(dirpath)

# Specify the directory you want to cleanup
directory = '/media/vedmani/F74D-58D6/projects/rag/data'
delete_empty_dirs(directory)
