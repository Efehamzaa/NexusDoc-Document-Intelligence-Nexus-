import fitz
import os

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF dosyasi bulunamadi: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
        text = ""  # metni biriktereceğimiz boş değişken
        for page in doc:
            page_text = page.get_text()  # sayfadaki metni al
            text += page_text + "\n"  # metni biriktir
        return text 
    except Exception as e:
        raise RuntimeError(f"PDF okunurken hata oluştu: {e}")
        return None

if __name__ == "__main__":
    test_pdf="data/ornek.pdf"

    result= extract_text_from_pdf(test_pdf)
    if result:
        print("PDF metni başarıyla çıkarıldı.")
        print("ilk 100 karakter:", result[:100])
        

