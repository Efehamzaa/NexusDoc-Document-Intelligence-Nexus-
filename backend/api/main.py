import os
import sys
import shutil
import json

from backend.core.query_engine import get_query_engine, get_quiz_engine
from fastapi import FastAPI , HTTPException, UploadFile, File
from pydantic import BaseModel


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.core.query_engine import get_query_engine
from backend.core.indexer import build_index 

app=FastAPI(title="NexusDoc API", description="RAG tabanlı doküman analiz motoru" )

print(" RAG Motoru Yükleniyor. Bekleyin...")
engine = get_query_engine()
print("Sistem Çevrimiçi.")

class SoruIstegi(BaseModel):
    soru: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
        os.makedirs(data_dir, exist_ok=True) 
        
        file_path = os.path.join(data_dir, file.filename)
        
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        print(f"SİSTEM BİLDİRİMİ: {file.filename} diske kaydedildi. Vektörizasyon başlıyor...")
        
        
        build_index(file_path)
        
        
        global engine
        engine = get_query_engine()
        
        print("SİSTEM BİLDİRİMİ: Hafıza güncellendi ve motor yeniden bağlandı.")
        
        return {
            "durum": "başarılı", 
            "mesaj": f"{file.filename} başarıyla yüklendi, parçalandı ve NexusDoc hafızasına eklendi."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dosya yükleme veya indeksleme sırasında kritik hata: {str(e)}")
    
@app.post("/ask")
async def ask_question(istek: SoruIstegi):
    try:
        # Gelen soruyu ChromaDB + Llama 3 motoruna at
        cevap = engine.chat(istek.soru)
        
        # Sonucu JSON formatında geri fırlat
        return {
            "soru": istek.soru,
            "cevap": str(cevap)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sorgu işlenirken kritik hata: {str(e)}")
    

@app.get("/generate_quiz")
def generate_quiz():
    try:
        engine , prompt = get_quiz_engine()

        ham_cevap = engine.query(prompt)
        cevap_metni= str(ham_cevap).strip()

        if cevap_metni.startswith("```json"):
            cevap_metni = cevap_metni[7:]
        if cevap_metni.endswith("```"):
            cevap_metni = cevap_metni[:-3]
        
        cevap_metni = cevap_metni.strip()

        quiz_verisi=json.loads(cevap_metni)

        return {
            "durum": "başarılı",
            "quiz_verisi": quiz_verisi
        }
    except json.JSONDecodeError as e:
        return {"durum": "hata", "mesaj": "Motor JSON formatına uymadı. Halüsinasyon engellendi.", "detay": str(e)}
    except Exception as e:
        return {"durum": "hata", "mesaj": "Quiz oluşturulurken kritik hata oluştu.", "detay": str(e)}
    