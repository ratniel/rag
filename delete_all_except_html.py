import os
import glob

# Specify the directory you want to cleanup
directory = '/media/vedmani/F74D-58D6/projects/rag/data'

# Use glob to match .htm and .html files
html_files = glob.glob(directory + '/**/*.htm*', recursive=True)

# Iterate over all files in the directory
for filename in glob.glob(directory + '/**', recursive=True):
    if os.path.isfile(filename) and filename not in html_files:
        os.remove(filename)  # Remove the file
