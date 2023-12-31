import glob
import os
import re
from pathlib import Path

import chardet
from bs4 import BeautifulSoup


def detect_encoding(filename):
   with open(filename, 'rb') as f:
       result = chardet.detect(f.read())
   return result['encoding']

def make_soup (filepath):
    encoding = detect_encoding(filename=filepath)
    with open(filepath, 'r', encoding=encoding) as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def delete_empty_dirs(path):
    for dirpath, dirnames, files in os.walk(path, topdown=False):
        if not dirnames and not files:
            os.rmdir(dirpath)


def delete_files_except_html(directory):
    # Use glob to match .htm and .html files
    html_files = glob.glob(directory + '/**/*.htm*', recursive=True)

    # Iterate over all files in the directory
    for filename in glob.glob(directory + '/**', recursive=True):
        if os.path.isfile(filename) and filename not in html_files:
            os.remove(filename)  # Remove the file


#function to delete all the scripts and styles from the html file

def clean_html_file(filepath):
    encoding = detect_encoding(filename=filepath)
    with open(filepath, 'r', encoding=encoding) as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
   
   #this removes the unrenderable possibly sanskrit text
    for element in soup.select('.MsoPlainText'):
     element.decompose()

    tags_to_decopose = ['script', 'style', 'img', 'nobr', 'meta', 'link', 'title', 'head'] #TODO: check if deleting head is ok
    tags_to_unwrap = ['i', 'font', 'b', 'span', 'o:p']
    attributes_to_remove = ["class", "style", "bgcolor", "lang", "onclick", "onload", "align", "font"]

    for tag in soup(tags_to_decopose):
        tag.decompose()
    
    for _tag in soup(tags_to_unwrap):
        _tag.unwrap()

    for tag in soup():
        for attribute in attributes_to_remove:
            del tag[attribute]

    raw_html = str(soup)
    raw_html = re.sub(r'\xa0|†', '', raw_html)
    cleaned_html = re.sub(r'<\?if.*?<\?endif\?>', '', raw_html, flags=re.DOTALL)
    cleaned_html = re.sub(r'<!--.*?-->', '', cleaned_html, flags=re.DOTALL)

    return cleaned_html



if __name__ == '__main__':
    clean_html_file("data/Articles/Chikitsaa/Aamadosha.htm")