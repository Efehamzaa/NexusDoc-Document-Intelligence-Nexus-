import os
import sys
import json
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from llama_index.readers.file import PyMuPDFReader

from backend.core.query_engine import get_query_engine, get_quiz_engine, get_flashcard_engine
from backend.core.indexer import build_index 

app = FastAPI(title="NexusDoc API", description="RAG tabanlı doküman analiz motoru")

print("RAG Motoru Yükleniyor. Bekleyin...")
engine = get_query_engine()
print("Sistem Çevrimiçi.")

class SoruIstegi(BaseModel):
    soru: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global engine
    try:
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        loader = PyMuPDFReader()
        documents = loader.load(file_path=temp_file_path)

        build_index(documents)

        engine = get_query_engine()
        
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        return {"durum": "basarili", "mesaj": "Doküman PyMuPDF ile derinlemesine analiz edildi ve indekslendi."}

    except Exception as e:
        return {"durum": "hata", "mesaj": f"Yükleme ve Vektörizasyon Hatası: {str(e)}"}


@app.post("/ask")
async def ask_question(istek: SoruIstegi):
    try:
        cevap = engine.chat(istek.soru)
        return {
            "soru": istek.soru,
            "cevap": str(cevap)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sorgu işlenirken kritik hata: {str(e)}")
    

@app.get("/generate_quiz")
def generate_quiz():
    try:
        # Fonksiyondan artık sadece motor dönüyor, prompt template içinde gömülü
        quiz_engine = get_quiz_engine()
        
        # SİHİRLİ DOKUNUŞ: Veritabanına talimatı değil, aranacak bağlamı gönderiyoruz.
        ham_cevap = quiz_engine.query("Dokümanın genel özeti, ana fikri, temel kavramlar ve kritik teoriler nelerdir?")
        cevap_metni = str(ham_cevap).strip()
        
        match = re.search(r'\[.*\]', cevap_metni, re.DOTALL)
        if match:
            temiz_json_metni = match.group(0)
        else:
            return {"durum": "hata", "mesaj": "Motor geçerli bir JSON dizisi üretemedi."}
        
        quiz_verisi = json.loads(temiz_json_metni)
        return {"durum": "basarili", "quiz": quiz_verisi}
        
    except Exception as e:
        return {"durum": "hata", "mesaj": f"Beklenmeyen Sunucu Hatası: {str(e)}"}
    

@app.get("/generate_flashcards")
def generate_flashcards():
    try:
        flashcard_engine = get_flashcard_engine()
        
        # Veritabanında akademik terimleri bulması için anlamsal bir arama metni gönderiyoruz
        ham_cevap = flashcard_engine.query("Dokümandaki önemli akademik terimler, tanımlar ve kurallar nelerdir?")
        cevap_metni = str(ham_cevap).strip()
        
        match = re.search(r'\[.*\]', cevap_metni, re.DOTALL)
        if match:
            temiz_json_metni = match.group(0)
        else:
            return {"durum": "hata", "mesaj": "Motor geçerli bir JSON dizisi üretemedi."}
        
        kart_verisi = json.loads(temiz_json_metni)
        return {"durum": "basarili", "kartlar": kart_verisi}
        
    except Exception as e:
        return {"durum": "hata", "mesaj": f"Beklenmeyen Sunucu Hatası: {str(e)}"}