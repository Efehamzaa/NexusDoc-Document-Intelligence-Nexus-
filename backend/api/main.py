import os
import sys
import shutil
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
        cevap = engine.query(istek.soru)
        
        # Sonucu JSON formatında geri fırlat
        return {
            "soru": istek.soru,
            "cevap": str(cevap)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sorgu işlenirken kritik hata: {str(e)}")