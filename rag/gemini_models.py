from dotenv import load_dotenv
load_dotenv()

from llama_index.llms.gemini import Gemini
from llama_index.llms import ChatMessage
from llama_index.embeddings.gemini import GeminiEmbedding

llm = Gemini()
emebedding_model = GeminiEmbedding()
