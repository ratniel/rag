import gradio as gr
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
from ved_src.utils import load_docs

Settings.embed_model = GeminiEmbedding(model_name="models/embedding-001")
Settings.llm = Gemini(model_name="models/gemini-pro", temperature=0.5)

nodes = load_docs(
    "/media/vedmani/F74D-58D6/projects/rag/storage/docstore/article_nodes_embedded_combined"
)

index = VectorStoreIndex(nodes, embed_model=None)
chat_engine = index.as_chat_engine(chat_mode="condense_plus_context", verbose=True)


def respond(message, history):
    # streaming_response = chat_engine.stream_chat(message)
    # for token in streaming_response.response_gen:
    #     print(token, end="")
    #     yield token
    response = chat_engine.chat(message)
    print(response.response)
    return response.response


def reset():
    chat_engine.reset()
    gr.Info("Chat history has been reset.")

with gr.Blocks() as demo:
    reset_button = gr.Button("Click to reset chat history")
    reset_button.click(reset)
    chat = gr.ChatInterface(respond, undo_btn=None, fill_height=True)

demo.launch()