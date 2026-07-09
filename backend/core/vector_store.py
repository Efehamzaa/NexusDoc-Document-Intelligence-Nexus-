import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

def get_storage_context(reset=False):
    db_path="./chroma_db"
    chrome_client=chromadb.PersistentClient(path=db_path)
    
    if reset:
        try:
            chrome_client.delete_collection("nexus_koleksiyonu")
            print("SİSTEM BİLDİRİMİ: Eski vektör hafızası başarıyla imha edildi. Temiz sayfa açılıyor.")
        except Exception:
            pass
            
    chroma_collection=chrome_client.get_or_create_collection("nexus_koleksiyonu")
    vector_store=ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context=StorageContext.from_defaults(vector_store=vector_store)
    return storage_context