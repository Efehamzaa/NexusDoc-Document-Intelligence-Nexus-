import os
import sys
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__) , '..', '..')))

from backend.services.parser import extract_text_from_pdf
from backend.core.chunker import get_text_chunks
from backend.core.vector_store import get_storage_context

def build_index(pdf_path):
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    raw_text = extract_text_from_pdf(pdf_path)
    nodes= get_text_chunks(raw_text)
    storage= get_storage_context()

    index=VectorStoreIndex(nodes=nodes, storage_context=storage)
    return index

if __name__ == "__main__":
    test_pdf = "data/ornek.pdf" 
    print("1. İndeksleme ve Vektörleştirme başlatılıyor. Bu işlem modelin hızına göre 1-2 dakika sürebilir...")
    
    try:
        index = build_index(test_pdf)
        print("İşlem Başarılı! RAG Mimarisi ayağa kalktı ve hafıza ChromaDB'ye kaydedildi.")
    except Exception as e:
        print(f"Sistem Çöktü. Hata: {e}")
