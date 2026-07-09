import os
import sys
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import SentenceSplitter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__) , '..', '..')))

from backend.core.vector_store import get_storage_context

def build_index(documents):
    # Ağır dokümanları Llama 3'ün hafıza limitlerine göre optimize ediyoruz
    Settings.text_splitter = SentenceSplitter(chunk_size=768, chunk_overlap=100)
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
    
    storage = get_storage_context(reset=True)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage)
    return index