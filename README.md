# 🛡️ NexusDoc

NexusDoc, yerel ortamda çalışan, RAG (Retrieval-Augmented Generation) mimarisiyle güçlendirilmiş gelişmiş bir doküman analiz terminalidir. Büyük boyutlu PDF belgelerini saniyeler içinde vektörize ederek indeksler ve Llama 3 motoruyla bu dokümanlar üzerinde derinlemesine analiz yapmanızı sağlar.

## ✨ Temel Özellikler

*   **💬 Doküman Asistanı:** Yüklediğiniz PDF'in içeriğine dayalı, halüsinasyondan arındırılmış, bağlama duyarlı (context-aware) sohbet.
*   **📝 Otomatik Sınav Matrisi:** Dokümanın tamamını analiz ederek zor seviyede, çoktan seçmeli akademik sorular ve cevap anahtarları üretir.
*   **🗂️ Akıllı Bilgi Kartları (Flashcards):** Belgedeki kritik teorik kavramları ve terminolojiyi tespit edip hızlı tekrar kartlarına dönüştürür.
*   **🔒 Yerel ve Güvenli:** Verileriniz buluta gitmez. Ollama ve ChromaDB ile tamamen lokal ortamda çalışır.

## 🛠️ Teknoloji Yığını

*   **Backend:** Python, FastAPI
*   **RAG & LLM:** LlamaIndex, Ollama (Llama 3), Nomic Embeddings
*   **Vector Database:** ChromaDB
*   **Frontend:** Streamlit

## 🚀 Kurulum ve Çalıştırma

1. Depoyu klonlayın:
   ```bash
   git clone [https://github.com/KULLANICI_ADIN/nexusdoc.git](https://github.com/KULLANICI_ADIN/nexusdoc.git)
   cd nexusdoc

   Gerekli kütüphaneleri yükleyin:
pip install -r requirements.txt

    Arka plan API sunucusunu başlatın:
uvicorn backend.api.main:app --reload
    
    Yeni bir terminal açıp arayüzü başlatın:
streamlit run frontend/app.py

### 2. Güvenlik ve Temizlik (`.gitignore`)
Veritabanı dosyalarını ve gereksiz önbellekleri GitHub'a yüklememek çok önemlidir. Proje ana dizininde `.gitignore` adında bir dosya oluşturup içine şunları yaz:

```text
# Python
__pycache__/
*.py[cod]
*venv/
.env

# Veritabanı ve Geçici Dosyalar
chroma_db/
temp_*.pdf
