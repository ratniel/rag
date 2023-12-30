import chardet
from bs4 import BeautifulSoup
import glob
from pathlib import Path
import re

def detect_encoding(filename):
   with open(filename, 'rb') as f:
       result = chardet.detect(f.read())
   return result['encoding']

#function to delete all the scripts and styles from the html file

def clean_html_file(filename):
    path = Path(filename)
    encoding = detect_encoding(filename=filename)
    with open(filename, 'r', encoding=encoding) as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['script', 'style', 'img', 'nobr', 'meta', 'link', 'title']):
        tag.decompose()
    
    for _tag in soup(['i', 'font', 'b', 'span', 'o:p']):
        _tag.unwrap()

    for tag in soup():
        for attribute in ["class", "style", "bgcolor", "lang", "onclick", "onload", "align", "font"]:
            del tag[attribute]

    raw_html = str(soup)
    cleaned_html = re.sub(r'<\?if.*?<\?endif\?>', '', raw_html, flags=re.DOTALL)

    # Save the file with new name in current directory
    with open('tmp/' + str(path.name), 'w',) as f:
        f.write(cleaned_html)

if __name__ == '__main__':
    clean_html_file("data/Articles/Chikitsaa/Aamadosha.htm")
