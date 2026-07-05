import os
import sys
import json

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

    chat_engine = index.as_chat_engine(
        chat_mode="context",
        verbose=True,
        system_prompt=(
            "Sen NexusDoc sisteminin çekirdeğinde çalışan, son derece profesyonel, net ve analitik bir doküman analiz uzmanısın. "
            "Kullanıcının sorularına DAİMA ve SADECE Türkçe dilinde yanıt vermelisin. "
            "Eğer sorunun cevabı bağlam bilgisinde yoksa, bunu dürüstçe Türkçe olarak belirt. "
            "Kullanıcı sana 'teşekkür ederim', 'merhaba' gibi günlük iletişim ve nezaket ifadeleri kullandığında, ona profesyonel ve nazik bir şekilde 'Rica ederim', 'Size nasıl yardımcı olabilirim?' gibi kısa yanıtlar ver. Bu durumlarda asla gereksiz bilgi veya kod üretme."
        )
    )

    return chat_engine

def get_quiz_engine():
    Settings.llm=Ollama(model="llama3", request_timeout=360.0)
    Settings.embed_model=OllamaEmbedding(model_name="nomic-embed-text")

    storage=get_storage_context()

    index=VectorStoreIndex.from_vector_store(
        vector_store=storage.vector_store,
        storage_context=storage
    )

    quiz_prompt = (
        "Sen akademik bir sınav hazırlama motorusun. "
        "Aşağıdaki bağlam bilgisini kullanarak, zor seviyede 3 adet çoktan seçmeli soru hazırla. "
        "TÜM SORULAR, ŞIKLAR VE AÇIKLAMALAR KESİNLİKLE VE SADECE TÜRKÇE DİLİNDE OLMALIDIR. İngilizce kelime kullanma. "
        "Çıktın SADECE ve SADECE aşağıdaki JSON formatında olmalıdır. JSON dışında tek bir kelime bile etme, açıklama yapma.\n"
        "Format:\n"
        "[\n"
        "  {\n"
        "    \"soru\": \"Soru metni\",\n"
        "    \"secenekler\": [\"A şıkkı\", \"B şıkkı\", \"C şıkkı\", \"D şıkkı\", \"E şıkkı\"],\n"
        "    \"dogru_cevap\": \"Doğru olan şıkkın tam metni\",\n"
        "    \"aciklama\": \"Cevabın neden doğru olduğuna dair kısa açıklama\"\n"
        "  }\n"
        "]\n"
    )

    quiz_engine = index.as_query_engine(
        similarity_top_k=5,
        response_mode="compact",
    )
    
    return quiz_engine , quiz_prompt

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



