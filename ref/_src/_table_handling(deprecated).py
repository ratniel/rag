#https://www.phind.com/search?cache=vh14oxfy29j569piysnnqm1e

from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
from src.preprocessing_utils import detect_encoding
filepath = "data/Articles/Chikitsaa/AushadhaSevanaKaala.htm"
path = Path(filepath)
encoding = detect_encoding(filename=filepath)
with open(filepath, 'r', encoding=encoding) as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find the table in the HTML document
tables = soup.find_all('table')
#pandas can convert all the tables 
table_dfs = pd.read_html(str(tables),header=0, index_col=0)
# print(table_dfs)
markdown_str = table_dfs[0].to_markdown(tablefmt="grid")
print(markdown_str)
tsv_str = table_dfs[0].to_csv(sep='|')
print(tsv_str)