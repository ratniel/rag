from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import HTMLNodeParser
from typing import List
import llama_index.core.schema as schema
from llama_index.core.storage.docstore import SimpleDocumentStore
from pathlib import Path





def extract_htmltag_nodes(input_dir: str, tag_list: list=["p", "li", "b", "i", "u", "section", "text"]) -> List[schema.TextNode]:
    """
    Extracts nodes for ["p", "li", "b", "i", "u", "section", "text"] tags \
        from HTML files in the specified directory.

    Args:
        input_dir (str): The directory path containing HTML files.

    Returns:
        List[schema.TextNode]: A list of HTML tag nodes.

    Example:
        >>> nodes = extract_htmltag_nodes('/path/to/html_files')
    """
    reader = SimpleDirectoryReader(input_dir=input_dir, recursive=True,)
    documents = reader.load_data(show_progress=True)
    node_parser = HTMLNodeParser(tags=tag_list, 
                                 include_prev_next_rel=False)
    nodes = node_parser.get_nodes_from_documents(documents, show_progress=True)
    nodes = [node for node in nodes if len(node.get_content()) > 0]
    for node in nodes:
        node.text = node.text.replace("\n", " ").replace("\t", " ")
        node.excluded_embed_metadata_keys=['tag', 'file_path', 'file_name', 'file_type', 'file_size', 'creation_date', 'last_modified_date', 'last_accessed_date']
    return nodes

def save_docstore(nodes, save_dir: str, store_name: str) -> None:
    """
    Create a document store and save it to the specified directory.

    Args:
        nodes (List[str]): List of nodes to be added to the document store.
        save_dir (str): Directory path where the document store will be saved.
        store_name (str): Name of the document store file.

    Returns:
        None
    """
    docstore = SimpleDocumentStore()
    docstore.add_documents(nodes)
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    docstore.add_documents(nodes)
    docstore.persist(persist_path=save_dir/store_name)
    return docstore

def load_docs(path, return_docstore: bool = False):
    """
    Load documents from the specified path.

    Args:
        path (str): The path to the document store.
        return_docstore (bool, optional): Whether to return the document store object instead of the loaded documents. Defaults to False.

    Returns:
        list or SimpleDocumentStore: A list of loaded documents if return_docstore is False, otherwise the document store object.
    """
    docstore = SimpleDocumentStore.from_persist_path(persist_path=path)
    if return_docstore:
        return docstore
    else:
        return list(docstore.docs.values())

if __name__ == '__main__':
    nodes = extract_htmltag_nodes('/home/dai/35/rag/data/clean_html/Articles')
    save_docstore(nodes, '/home/dai/35/rag/storage', 'articles_store')
    docs = load_docs('/home/dai/35/rag/storeage/articles_store')