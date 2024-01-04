import glob
import io
import os
import re
from pathlib import Path

import chardet
import pandas as pd
from bs4 import BeautifulSoup


def detect_encoding(filename: str) -> str:
    """
    Detects the encoding of a file.

    Args:
        filename (str): The path to the file.

    Returns:
        str: The encoding of the file.
    """
    with open(filename, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def make_soup(filepath: str) -> BeautifulSoup:
    """
    Create a BeautifulSoup object from an HTML file.

    Args:
        filepath (str): The path to the HTML file.

    Returns:
        BeautifulSoup: The BeautifulSoup object representing the HTML file.
    """
    encoding = detect_encoding(filename=filepath)
    with open(filepath, 'r', encoding=encoding) as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup



def delete_empty_dirs(path: str) -> None:
    """
    Deletes empty directories recursively starting from the given path.

    Args:
        path (str): The path to start deleting empty directories from.

    Returns:
        None
    """
    for dirpath, dirnames, files in os.walk(path, topdown=False):
        if not dirnames and not files:
            os.rmdir(dirpath)


def delete_files_except_html(directory: str) -> None:
    """
    Delete all files in the given directory, except for HTML files.

    Args:
        directory (str): The directory path.

    Returns:
        None
    """
    # Use glob to match .htm and .html files
    html_files = glob.glob(directory + '/**/*.htm*', recursive=True)

    # Iterate over all files in the directory
    for filename in glob.glob(directory + '/**', recursive=True):
        if os.path.isfile(filename) and filename not in html_files:
            os.remove(filename)  # Remove the file


#function to delete all the scripts and styles from the html file

def clean_html_file(filepath):
    """
    Cleans the HTML content of a file by removing unwanted elements and attributes.

    Args:
        filepath (str): The path to the HTML file.

    Returns:
        str: The cleaned HTML content as a string.
    """
    encoding = detect_encoding(filename=filepath)
    with open(filepath, 'r', encoding=encoding) as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
   
    # This removes the unrenderable possibly Sanskrit text
    for element in soup.select('.MsoPlainText'):
        element.decompose()

    tags_to_decopose = ['script', 'style', 'img', 'nobr', 'meta', 'link', 'title', 'head'] # TODO: check if deleting head is ok
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



def process_html_table(file_path: str, table_parser: str) -> BeautifulSoup:
    """
    Process the HTML table in the given file path and convert it to the specified format.

    Args:
        file_path (str): The path to the HTML file.
        table_parser (str): The format to convert the table to. Valid options are 'md' for Markdown and 'tsv' for TSV.

    Returns:
        BeautifulSoup: The modified BeautifulSoup object with the converted table.

    """
    clean_html = clean_html_file(file_path)
    soup = BeautifulSoup(clean_html, 'html.parser')
    tables = soup.find_all('table')
    for table in tables:
        df = pd.read_html(io.StringIO(str(table)), header=0, index_col=0)
        md = df[0].to_markdown(tablefmt="grid")
        tsv = df[0].to_csv(sep='\t')
        # convert table tag to text tag
        table.name = 'text'
        if table_parser == 'md':
            table.string = md
        elif table_parser == 'tsv':
            table.string = tsv

    return soup

 


def process_html_table_from_string(html: str, table_parser: str) -> BeautifulSoup:
    """
    Process the HTML table in the given HTML string and convert it to the specified format.
 
    Args:
        html (str): The HTML string.
        table_parser (str): The format to convert the table to. Valid options are 'md' for Markdown and 'tsv' for TSV.

    Returns:
        BeautifulSoup: The modified BeautifulSoup object with the converted table.

    """
    clean_html = html
    soup = BeautifulSoup(clean_html, 'html.parser')
    tables = soup.find_all('table')
    for table in tables:
        df = pd.read_html(io.StringIO(str(table)), header=0, index_col=0)
        md = df[0].to_markdown(tablefmt="grid")
        tsv = df[0].to_csv(sep='\t')
        # convert table tag to text tag
        table.name = 'text'
        if table_parser == 'md':
            table.string = md
        elif table_parser == 'tsv':
            table.string = tsv

    return soup

def save_clean_files(filepath):
    """
    Processes html file, and saves the cleaned HTML and its text content to new files.

    Args:
        filepath (Path or str): The path to the HTML file to be cleaned.

    Returns:
        None
    """
    processed_data = Path('processed_data')
    clean_file = processed_data / filepath.parent / filepath.name 
    clean_file.parent.mkdir(parents=True, exist_ok=True)
    clean_html = clean_html_file(filepath=filepath)
    clean_html = process_html_table_from_string(clean_html, table_parser='md')
    print(clean_html.text)
    with open(clean_file, 'w') as f:
        f.write(str(clean_html))
    with open(str(clean_file) + ".txt", 'w') as f:
        f.write(clean_html.get_text())


if __name__ == '__main__':
    filepath = Path("data/Articles/Other/Mantra.htm")
    save_clean_files(filepath)