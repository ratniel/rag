from ratniel_src.context_addition import process_nodes
from src.indexing_utils import extract_htmltag_nodes

file_path = "/home/dai/rag/data/clean_html/Articles"
nodes = extract_htmltag_nodes(file_path, tag_list=["p","section"])

if __name__ =="__main__":
    process_nodes(nodes)