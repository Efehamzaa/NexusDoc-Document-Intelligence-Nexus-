import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="NexusDoc", page_icon="🛡️", layout="wide")
st.title("NexusDoc: Akıllı Doküman Analiz Sistemi")

# Sol Panel: Dosya Yükleme Kontrol Merkezi
with st.sidebar:
    st.header("📄 Doküman Yükle")
    uploaded_file = st.file_uploader("Analiz edilecek PDF dosyasını seçin", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("Sisteme Yükle ve Vektörize Et"):
            with st.spinner("Doküman işleniyor ve Llama 3 motoru güncelleniyor..."):
                # Dosyayı API'ye gönder
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(f"{API_URL}/upload", files=files)
                
                if response.status_code == 200:
                    st.success("Doküman başarıyla NexusDoc hafızasına eklendi.")
                else:
                    st.error("Siber güvenlik standartlarında bir hata oluştu. Yükleme başarısız.")

# Ana Ekran: Sorgu ve Analiz Merkezi
st.header("Analiz Motoru")
soru = st.text_input("Dokümanla ilgili spesifik sorunuzu buraya yazın:")

if st.button("Sorgula"):
    if soru:
        with st.spinner("Motor düşünüyor..."):
            payload = {"soru": soru}
            response = requests.post(f"{API_URL}/ask", json=payload)
            
            if response.status_code == 200:
                cevap = response.json().get("cevap", "")
                st.info(cevap)
            else:
                st.error("Sorgu işlenemedi. API bağlantısını ve arka plan loglarını kontrol edin.")
    else:
        st.warning("Lütfen geçerli bir analiz sorgusu girin.")