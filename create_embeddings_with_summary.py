from rag.embed_nodes import embed_nodes,embed_nodes_on_summary
from rag.rag_utils import load_docs

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

sentence_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
dir_path = "./data/text_data/Articles"
reader = SimpleDirectoryReader(dir_path, recursive=True)
docs = reader.load_data(show_progress=True)
nodes = sentence_splitter.get_nodes_from_documents(docs, show_progress=True)


nodes = nodes = embed_nodes_on_summary(nodes=nodes, save_dir="./rag/Articles_store/docstore", docstore_name="Articles_with_embeddings_with_summary", save_docstore=True)