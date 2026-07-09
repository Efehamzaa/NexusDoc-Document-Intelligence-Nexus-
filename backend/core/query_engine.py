import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, Settings, PromptTemplate
from backend.core.vector_store import get_storage_context

def get_query_engine():
    Settings.llm = Ollama(model="llama3", request_timeout=360.0)
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
    storage = get_storage_context()
    index = VectorStoreIndex.from_vector_store(vector_store=storage.vector_store, storage_context=storage)

    chat_engine = index.as_chat_engine(
        chat_mode="context",
        verbose=True,
        system_prompt=(
            "Sen NexusDoc sisteminin çekirdeğinde çalışan, profesyonel ve analitik bir doküman analiz uzmanısın. "
            "Kullanıcının sorularına DAİMA ve SADECE Türkçe dilinde yanıt vermelisin. "
            "Eğer sorunun cevabı bağlam bilgisinde yoksa, bunu dürüstçe Türkçe olarak belirt."
        )
    )
    return chat_engine

def get_quiz_engine():
    Settings.llm = Ollama(model="llama3", request_timeout=360.0)
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
    storage = get_storage_context()
    index = VectorStoreIndex.from_vector_store(vector_store=storage.vector_store, storage_context=storage)

    quiz_tmpl_str = (
        "Aşağıdaki bağlam bilgisini kullan:\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Sen akademik bir sınav hazırlama motorusun. "
        "Bu bağlam bilgisini kullanarak, zor seviyede 3 adet çoktan seçmeli soru hazırla. "
        "TÜM SORULAR, ŞIKLAR VE AÇIKLAMALAR KESİNLİKLE VE SADECE TÜRKÇE OLMALIDIR. "
        "Çıktın SADECE aşağıdaki JSON formatında olmalıdır. JSON dışında açıklama yapma.\n"
        "Format:\n"
        "[\n  {\n    \"soru\": \"Soru metni\",\n    \"secenekler\": [\"A şıkkı\", \"B şıkkı\", \"C şıkkı\", \"D şıkkı\", \"E şıkkı\"],\n    \"dogru_cevap\": \"Doğru olan şıkkın tam metni\",\n    \"aciklama\": \"Cevabın neden doğru olduğuna dair açıklama\"\n  }\n]\n"
    )
    quiz_tmpl = PromptTemplate(quiz_tmpl_str)
    
    quiz_engine = index.as_query_engine(
        similarity_top_k=8, # Daha fazla parçayı analiz etmesi için artırıldı
        text_qa_template=quiz_tmpl,
        response_mode="compact"
    )
    return quiz_engine

def get_flashcard_engine():
    Settings.llm = Ollama(model="llama3", request_timeout=360.0)
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
    storage = get_storage_context()
    index = VectorStoreIndex.from_vector_store(vector_store=storage.vector_store, storage_context=storage)

    flashcard_tmpl_str = (
        "Aşağıdaki bağlam bilgisini kullan:\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Sen akademik bir çalışma kartı (flashcard) hazırlama motorusun. "
        "Bu bağlam bilgisini kullanarak, konunun en kritik 4 teorik terimini veya kavramını seç. "
        "TÜM KAVRAMLAR VE TANIMLAR KESİNLİKLE TÜRKÇE OLMALIDIR. "
        "Çıktın SADECE aşağıdaki JSON formatında olmalıdır. JSON dışında açıklama yapma.\n"
        "Format:\n"
        "[\n  {\n    \"terim\": \"Kavramın Adı\",\n    \"tanim\": \"Kavramın net, anlaşılır ve kısa tanımı\"\n  }\n]\n"
    )
    flashcard_tmpl = PromptTemplate(flashcard_tmpl_str)

    flashcard_engine = index.as_query_engine(
        similarity_top_k=8,
        text_qa_template=flashcard_tmpl,
        response_mode="compact"
    )
    return flashcard_engine



