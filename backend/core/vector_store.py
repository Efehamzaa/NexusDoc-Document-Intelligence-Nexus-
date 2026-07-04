import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

def get_storage_context():
    db_path="./chroma_db"
    chrome_client=chromadb.PersistentClient(path=db_path)
    chroma_collection=chrome_client.get_or_create_collection("nexus_koleksiyonu")
    vector_store=ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context=StorageContext.from_defaults(vector_store=vector_store)
    return storage_context

if __name__ == "__main__":
    print("1. Veritabani motoru başlatiliyor...")
    storage_context= get_storage_context()
    if storage_context:
        print("İşlem başarili!  StorageContext hazirlanndi.")
        print("Lutfen VS Code sol menüde 'chroma_db' adında yeni bir klasör oluşup oluşmadığını kontrol et.")
