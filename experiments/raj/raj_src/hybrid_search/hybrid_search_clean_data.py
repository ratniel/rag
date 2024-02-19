""" 
    This file runs on the nodes that are built on clean data which is without context addition.
    Index Name:- LlamaIndex_articles
"""

import weaviate
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.vector_stores.weaviate import WeaviateVectorStore

from src.indexing_utils import load_docs

Settings.embed_model = GeminiEmbedding(model_name="models/embedding-001", task_type="retrieval_query")
Settings.llm = Gemini(model_name="models/gemini-pro", temperature=0.5)

# Connect to local instance
client = weaviate.Client("http://localhost:8080")

nodes = load_docs(
    path="/home/dai/33/project/rag/storage/docstore/Articles_with_embeddings_on_chunks",
    return_docstore=False,
)

vector_store = WeaviateVectorStore(
    weaviate_client=client, index_name="LlamaIndex_articles"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes=nodes, storage_context=storage_context)

# Query Index with Hybrid Search as chat engine
chat_engine = index.as_chat_engine(
    vector_store_query_mode="hybrid", similarity_top_k=2, alpha=0.5, chat_mode="condense_plus_context"
)

response = chat_engine.chat("What is the Anukta Dravya Vichaara?")
print(response.response)

response = chat_engine.chat("Give me the exmaple for it.")
print(response.response)

