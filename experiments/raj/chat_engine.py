from src.indexing_utils import load_docs
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.core import Settings
import streamlit as st

Settings.embed_model = GeminiEmbedding(model_name='models/embedding-001')
Settings.llm = Gemini(model_name='models/gemini-pro', temperature=0.5)

st.header("Chat with the Ayurveda bot")

# Initialize the chat message history
if "messages" not in st.session_state.keys(): 
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about anything related to Ayurveda!"}
    ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the Ayurveda docs hang tight! This should take 1-2 minutes."):
        nodes = load_docs("/home/dai/33/project/rag/storage/docstore/article_nodes_embedded_combined")
        index = VectorStoreIndex(nodes, embed_model=None)
        return index

index = load_data()

chat_engine = index.as_chat_engine(chat_mode="condense_plus_context")

# Prompt for user input and save to chat history
if prompt := st.chat_input("Your question"): 
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display the prior chat messages
for message in st.session_state.messages: 
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_engine.chat(prompt)
            print(response.response)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history


# # def predict(message,history):
# #     global chat_engine
# #     print(history)
# #     streaming_response = chat_engine.stream_chat(message)
# #     for token in streaming_response.response_gen:
# #         yield(token)

# # gr.ChatInterface(predict).launch()

# chat_engine = index.as_chat_engine(chat_mode="condense_plus_context")
# while True:
#     message = input("You: ")
#     streaming_response = chat_engine.stream_chat(message)
#     for token in streaming_response.response_gen:
#         print(token, end="")
#     print()