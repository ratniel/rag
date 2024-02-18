from ved_src.utils import load_docs
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.core import Settings
import gradio as gr

Settings.embed_model = GeminiEmbedding(model_name='models/embedding-001')
Settings.llm = Gemini(model_name='models/gemini-pro', temperature=0.5)

nodes = load_docs("/media/vedmani/F74D-58D6/projects/rag/storage/docstore/article_nodes_embedded_combined")

index = VectorStoreIndex(nodes, embed_model=None)
chat_engine = index.as_chat_engine()

# def predict(message,history):
#     global chat_engine
#     print(history)
#     streaming_response = chat_engine.stream_chat(message)
#     for token in streaming_response.response_gen:
#         yield(token)

# gr.ChatInterface(predict).launch()

chat_engine = index.as_chat_engine(chat_mode="condense_plus_context")
while True:
    message = input("You: ")
    streaming_response = chat_engine.stream_chat(message)
    for token in streaming_response.response_gen:
        print(token, end="")
    print()