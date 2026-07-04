import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex , Settings
from llama_index.core import PromptTemplate
from backend.core.vector_store import get_storage_context

def get_query_engine():
    Settings.llm = Ollama(model ="llama3" , request_timeout=360.0)
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    storage=get_storage_context()

    index=VectorStoreIndex.from_vector_store(
        vector_store=storage.vector_store,
        storage_context=storage
    )

    qa_prompt_tmpl_str=(
        "Sen NexusDoc sisteminin çekirdeğinde çalışan, son derece net, profesyonel ve analitik bir doküman analiz uzmanısın.\n"
        "Aşağıda sana kullanıcının yüklediği belgelerden çekilen 'Bağlam Bilgisi (Context)' verilmiştir:\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Görevlerin ve Katı Kuralların:\n"
        "1. Kullanıcının sorusuna sadece ve sadece yukarıdaki bağlam bilgisini kullanarak Türkçe yanıt ver.\n"
        "2. Eğer sorunun cevabı bağlam bilgisinde kesin olarak yoksa, asla kendi ön bilginle varsayım yapma veya bilgi uydurma. Sadece 'Bu bilgi yüklenen dokümanlarda bulunmamaktadır.' diyerek işlemi sonlandır.\n"
        "3. Cevabını verirken net, okunabilir ve profesyonel bir dil kullan. Gerekiyorsa alt başlıklar veya maddelerleme yap.\n"
        "\n"
        "Soru: {query_str}\n"
        "Cevap: "
    )

    qa_template=PromptTemplate(qa_prompt_tmpl_str)

    query_engine=index.as_query_engine(
        text_qa_template=qa_template,
        similarity_top_k=3,
    )

    return query_engine

if __name__ == "__main__":
    print("1. Sorgu Motoru Ayağa Kaldırılıyor (Bu işlem biraz zaman alabilir)...")
    engine=get_query_engine()

    print("2. Sistem Hazır. Dokumana soru soruluyor...")

    soru="Bu dökümanın ana konusu nedi?"

    print(f"Soru: {soru}")
    print("Cevap bekleniyor (Llama 3 düşünüyor)...\n ")

    cevap=engine.query(soru)
    print("--- YAPAY ZEKA YANITI ---")
    print(cevap)



