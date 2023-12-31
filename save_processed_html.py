import io

import pandas as pd
from bs4 import BeautifulSoup

from utils import clean_html_file
from pathlib import Path


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

def save_clean_html_file(filepath):
    ext = Path('.txt')
    processed_data = Path('processed_data')
    clean_file = processed_data / filepath.parent / filepath.name 
    clean_file.parent.mkdir(parents=True, exist_ok=True)
    clean_html = clean_html_file(filepath=filepath)
    clean_html = process_html_table_from_string(clean_html, table_parser='md')
    print(clean_html.get_text())

    with open(str(clean_file)+".txt", 'w') as f:
        f.write(clean_html.get_text())


if __name__ == '__main__':
    filepath = Path("data/Articles/Chikitsaa/AushadhaSevanaKaala.htm")
    save_clean_html_file(filepath)
