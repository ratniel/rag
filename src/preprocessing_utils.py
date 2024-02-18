import glob
import io
import os
import re
from pathlib import Path

import chardet
import pandas as pd
from bs4 import BeautifulSoup
import chardet  # noqa: F811
import os  # noqa: F811
import glob  # noqa: F811


def detect_encoding(filename: str) -> str:
    """
    Detects the encoding of a file.

    Args:
        filename (str): The path to the file.

    Returns:
        str: The encoding of the file.
    """
    with open(filename, "rb") as f:
        result = chardet.detect(f.read())
    return result["encoding"]


def make_soup(filepath: str) -> BeautifulSoup:
    """
    Create a BeautifulSoup object from an HTML file.

    Args:
        filepath (str): The path to the HTML file.

    Returns:
        BeautifulSoup: The BeautifulSoup object representing the HTML file.
    """
    encoding = detect_encoding(filename=filepath)
    with open(filepath, "r", encoding=encoding) as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
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


def delete_files_except_html(path: str) -> None:
    """
    Delete all files in the given directory, except for HTML files.

    Args:
        directory (str): The directory path.

    Returns:
        None
    """
    # Use glob to match .htm and .html files
    html_files = glob.glob(path + "/**/*.htm*", recursive=True)

    # Iterate over all files in the directory
    for filename in glob.glob(path + "/**", recursive=True):
        if os.path.isfile(filename) and filename not in html_files:
            os.remove(filename)  # Remove the file


# function to delete all the scripts and styles from the html file


def clean_html_file(filepath):
    """
    Cleans the HTML content of a file by removing unwanted elements and attributes.

    Args:
        filepath (str): The path to the HTML file.

    Returns:
        str: The cleaned HTML content as a string.
    """
    encoding = detect_encoding(filename=filepath)
    with open(filepath, "r", encoding=encoding) as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # TODO: check wether to remove p tag or to remove span tag
    # Find all <p> tags with 'font-family:SD01-TTSurekh'
    try:
        spans = soup.find_all(
            "span", style=lambda value: "font-family:SD01-TTSurekh" in value
        )
        if spans:
            for span in spans:
                # Remove the tag
                span.decompose()
    except Exception as e:
        pass

    # TODO: check if this is necessary
    # This removes the unrenderable possibly Sanskrit text
    # try:
    #     for element in soup.select('.MsoPlainText'):
    #         element.decompose()
    # except Exception as e:
    #     print(f"An error occurred: {str(e)}")

    _tags_to_decopose = [
        "script",
        "style",
        "img",
        "nobr",
        "meta",
        "link",
    ]  
    # TODO: check if deleting head is ok
    _tags_to_unwrap = ["font", "span", "o:p", "i", "b", "u"]
    _attributes_to_remove = [
        "class",
        "style",
        "bgcolor",
        "lang",
        "onclick",
        "onload",
        "align",
        "font",
        "xmlns",
        "xmlns:o",
        "xmlns:v",
        "xmlns:w",
        "link",
        "id",
        "vlink",
        "border",
        "bordercolordark",
        "bordercolorlight",
        "cellpadding",
        "cellspacing",
        "size",
        "font-size",
    ]

    tags_to_decompose = soup(_tags_to_decopose)
    tags_to_unwrap = soup(_tags_to_unwrap)

    if tags_to_decompose:
        for tag in soup(_tags_to_decopose):
            tag.decompose()
    if tags_to_unwrap:
        for _tag in soup(_tags_to_unwrap):
            _tag.unwrap()

    for tag in soup():
        for attribute in _attributes_to_remove:
            del tag[attribute]
    # TODO: Implement deletion of empty tags here

    raw_html = str(soup)
    raw_html = re.sub(r"\xa0|†", "", raw_html)
    cleaned_html = re.sub(r"<\?if.*?<\?endif\?>", "", raw_html, flags=re.DOTALL)
    cleaned_html = re.sub(r"<!--.*?-->", "", cleaned_html, flags=re.DOTALL)

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
    soup = BeautifulSoup(clean_html, "html.parser")
    tables = soup.find_all("table")
    for table in tables:
        df = pd.read_html(io.StringIO(str(table)), header=0, index_col=0)
        md = df[0].to_markdown(tablefmt="grid")
        tsv = df[0].to_csv(sep="\t")
        csv = df[0].to_csv()
        # convert table tag to text tag
        table.name = "text"
        if table_parser == "md":
            table.string = md
        elif table_parser == "tsv":
            table.string = tsv
        elif table_parser == "csv":
            table.string = csv
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
    soup = BeautifulSoup(clean_html, "html.parser")
    tables = soup.find_all("table")
    if tables:
        for table in tables:
            df = pd.read_html(io.StringIO(str(table)), header=0, index_col=0)
            md = df[0].to_markdown(tablefmt="grid")
            tsv = df[0].to_csv(sep="\t")
            csv = df[0].to_csv()
            # convert table tag to text tag
            table.name = "text"
            if table_parser == "md":
                table.string = md
            elif table_parser == "tsv":
                table.string = tsv
            elif table_parser == "csv":
                table.string = csv

    return soup


def save_clean_txt(filepath, save_location, dir_path=None):
    """
    Processes html file, and saves the cleaned HTML and its text content to new files.

    Args:
        filepath (Path or str): The path to the HTML file to be cleaned.
        save_location (Path or str): The path to save the cleaned text file.

    Returns:
        None
    """
    filepath = Path(filepath)
    processed_data = Path(save_location)
    clean_file = processed_data / filepath.parent / filepath.name
    clean_file = Path(str(clean_file).replace(dir_path + "/", ""))
    clean_file.parent.mkdir(parents=True, exist_ok=True)
    clean_html = clean_html_file(filepath=filepath)
    clean_html = process_html_table_from_string(clean_html, table_parser="csv")
    with open(str(clean_file) + ".txt", "w") as f:
        f.write(clean_html.get_text())


def save_clean_html(filepath, save_location, dir_path=None):
    """
    Processes html file, and saves the cleaned HTML and its text content to new files.

    Args:
        filepath (Path or str): The path to the HTML file to be cleaned.
        save_location (Path or str): The path to save the cleaned HTML file.

    Returns:
        None
    """
    filepath = Path(filepath)
    processed_data = Path(save_location)
    clean_file = processed_data / filepath.parent / filepath.name
    clean_file = Path(str(clean_file).replace(dir_path + "/", ""))
    clean_file.parent.mkdir(parents=True, exist_ok=True)
    clean_html = clean_html_file(filepath=filepath)
    clean_html = process_html_table_from_string(clean_html, table_parser="csv")

    with open(str(clean_file), "w") as f:
        content = str(clean_html)
        content = content.replace(
            "<p></p>\n", ""
        )  # TODO: implement this in the clean_html_file function
        f.write(content)


if __name__ == "__main__":
    filepath = Path("./data/Articles/Chikitsaa/Aamadosha.htm")
    save_clean_txt(filepath)
