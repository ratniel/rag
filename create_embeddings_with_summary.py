from rag.embed_nodes import embed_nodes,embed_nodes_on_summary
from rag.rag_utils import load_docs

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

nodes = load_docs("/home/dai/rag/Articles_store/docstore/Articles_with_summary_revised")


nodes = nodes = embed_nodes_on_summary(nodes=nodes, save_dir="/home/dai/35/rag/Articles_store/docstore", docstore_name="Articles_with_embeddings_with_summary", save_docstore=True)