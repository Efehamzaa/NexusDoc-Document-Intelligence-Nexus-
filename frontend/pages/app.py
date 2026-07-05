import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="NexusDoc", page_icon="🛡️", layout="wide")
st.title("🛡️ NexusDoc: Gelişmiş Analiz ve Eğitim Terminali")

# --- 1. SOHBET VE SINAV HAFIZASINI BAŞLATMA ---
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []

if "quiz_verisi" not in st.session_state:
    st.session_state.quiz_verisi = None

# Sol Panel: Dosya Yükleme Kontrol Merkezi
with st.sidebar:
    st.header("📄 Doküman Yükle")
    uploaded_file = st.file_uploader("Analiz edilecek PDF dosyasını seçin", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("Sisteme Yükle ve Vektörize Et"):
            with st.spinner("Doküman işleniyor ve tüm hafıza temizleniyor..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(f"{API_URL}/upload", files=files)
                
                if response.status_code == 200:
                    st.success("Doküman başarıyla NexusDoc hafızasına eklendi.")
                    # Yeni dosya gelince eski sohbeti ve eski sınavı sıfırla
                    st.session_state.mesajlar = []
                    st.session_state.quiz_verisi = None
                else:
                    st.error("Yükleme başarısız.")

# --- 2. SEKMELİ MİMARİ ENJEKSİYONU ---
tab_chat, tab_quiz, tab_flashcard = st.tabs([
    "💬 Sohbet Odası", 
    "📝 Akademik Sınav Odası", 
    "🗂️ Bilgi Kartları (Yakında)"
])

# ==========================================
# SEBME 1: SOHBET ODASI
# ==========================================
with tab_chat:
    st.subheader("Doküman Asistanı")
    
    # Geçmiş mesajları ekrana dök
    for mesaj in st.session_state.mesajlar:
        with st.chat_message(mesaj["rol"]):
            st.markdown(mesaj["icerik"])

    # Kullanıcıdan yeni girdi al
    soru = st.chat_input("Dokümanla ilgili sorunuzu buraya yazın...", key="chat_input_unique")

    if soru:
        st.session_state.mesajlar.append({"rol": "user", "icerik": soru})
        with st.chat_message("user"):
            st.markdown(soru)

        with st.spinner("NexusDoc düşünüyor..."):
            payload = {"soru": soru}
            try:
                response = requests.post(f"{API_URL}/ask", json=payload)
                if response.status_code == 200:
                    cevap = response.json().get("cevap", "")
                    with st.chat_message("assistant"):
                        st.markdown(cevap)
                    st.session_state.mesajlar.append({"rol": "assistant", "icerik": cevap})
                else:
                    st.error("Sorgu işlenemedi.")
            except requests.exceptions.ConnectionError:
                st.error("FastAPI sunucusuna bağlanılamadı.")

# ==========================================
# SEKME 2: AKADEMİK SINAV ODASI
# ==========================================
with tab_quiz:
    st.subheader("Otomatik Çoktan Seçmeli Sınav Modülü")
    st.write("Yüklediğiniz dokümandaki verilere dayanarak zor seviyede 3 adet soru üretilir.")
    
    if st.button("🔄 Yeni Sınav Oluştur / Yenile"):
        with st.spinner("Llama 3 dokümanı tarıyor ve soruları hazırlıyor..."):
            try:
                res = requests.get(f"{API_URL}/generate_quiz")
                data = res.json()
                
                
                if data.get("durum") in ["basarili", "başarılı"]:
                    st.session_state.quiz_verisi = data.get("quiz") or data.get("quiz_verisi")
                    st.success("Sınav başarıyla hazırlandı! Aşağıdan yanıtlayabilirsiniz.")
                elif "mesaj" in data:
                    st.error(f"Hata: {data.get('mesaj')}")
                else:
                    st.error(f"Beklenmeyen Sistem Durumu: {data}")
            
            
            except Exception as e:
                st.error(f"Sunucu bağlantı hatası: {str(e)}")

    
    if st.session_state.quiz_verisi:
        st.write("---")
        
        # Streamlit Rerun'larında şıkların sıfırlanmaması için formu kilitleyeceğiz
        with st.form(key="quiz_form"):
            user_answers = {}
            
            # JSON'dan gelen her bir soruyu döngüyle ekrana basıyoruz
            for idx, q in enumerate(st.session_state.quiz_verisi):
                st.markdown(f"**Soru {idx+1}:** {q['soru']}")
                
                # Kullanıcının seçeceği şıkkı kaydetmek için radio bileşeni
                secim = st.radio(
                    "Şıkkı Seçin:", 
                    options=q['secenekler'], 
                    key=f"q_{idx}"
                )
                user_answers[idx] = secim
                st.write("") # Boşluk
            
            # Formun gönderilme butonu (Cevapları Kontrol Et)
            submit_button = st.form_submit_button(label="🎯 Cevapları Kontrol Et")
            
            if submit_button:
                st.write("### Sınav Sonuç Değerlendirmesi")
                dogru_sayisi = 0
                
                for idx, q in enumerate(st.session_state.quiz_verisi):
                    user_ans = user_answers[idx]
                    correct_ans = q['dogru_cevap']
                    
                    st.markdown(f"**Soru {idx+1} Değerlendirmesi:**")
                    st.write(f"Senin Seçimin: `{user_ans}`")
                    st.write(f"Doğru Cevap: `{correct_ans}`")
                    
                    if user_ans.strip() == correct_ans.strip():
                        st.success("✅ DOĞRU!")
                        dogru_sayisi += 1
                    else:
                        st.error("❌ YANLIŞ!")
                    
                    # Çözüm açıklamasını ekrana bas
                    st.info(f"💡 **Çözüm Açıklaması:** {q['aciklama']}")
                    st.write("---")
                
                # Skoru ekrana bas
                st.metric(label="Toplam Başarı Skoru", value=f"{dogru_sayisi} / 3")

# ==========================================
# SEKME 3: BİLGI KARTLARI (YAKINDA)
# ==========================================
with tab_flashcard:
    st.info("Bu modül bir sonraki geliştirme fazında (Faz 6 - Kısım B) aktif edilecektir.")
    