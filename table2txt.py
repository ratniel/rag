import io

import pandas as pd
from bs4 import BeautifulSoup

from utils import clean_html_file


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


if __name__ == '__main__':
    result = process_html_table(file_path='processed_data/data/Articles/Chikitsaa/AushadhaSevanaKaala.htm', table_parser='md')
    print(result.text)
