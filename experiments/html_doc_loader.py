from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import HTMLNodeParser
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini

reader = SimpleDirectoryReader(input_dir="data/clean_html",
                                  recursive=True)

documents = reader.load_data()
print(len(documents))

node_parser = HTMLNodeParser()
nodes = node_parser.get_nodes_from_documents(documents)

embedding_model = GeminiEmbedding(embed_batch_size=1,
                                  )
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex(nodes, embed_model=embedding_model, show_progress=True)


