import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="NexusDoc Terminal", page_icon="🛡️", layout="wide")

# ==========================================
# DURUM YÖNETİMİ
# ==========================================
if "is_uploaded" not in st.session_state:
    st.session_state.is_uploaded = False
if "doc_name" not in st.session_state:
    st.session_state.doc_name = ""
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []
if "quiz_verisi" not in st.session_state:
    st.session_state.quiz_verisi = None
if "flashcard_verisi" not in st.session_state:
    st.session_state.flashcard_verisi = None

# ==========================================
# INTER FONT, SİYAH/YEŞİL TEMA VE BÜYÜK UPLOAD ALANI
# ==========================================
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Koyu Arka Plan ve Metinler */
    .stApp {
        background-color: #09090B;
        color: #F9FAFB;
    }

    /* Sekmeler (Odalar) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        gap: 32px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .stTabs [data-baseweb="tab"] {
        color: #9CA3AF;
        font-weight: 500;
        font-size: 1.05rem;
        padding-top: 16px;
        padding-bottom: 16px;
        border-radius: 0px;
    }
    .stTabs [aria-selected="true"] {
        color: #F9FAFB !important;
        border-bottom: 2px solid #22C55E !important;
        background-color: transparent !important;
    }

    /* Büyük Upload Alanı */
    [data-testid="stFileUploader"] {
        background-color: #111827;
        border: 2px dashed rgba(34, 197, 94, 0.4);
        border-radius: 16px;
        padding: 4rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #22C55E;
        background-color: #18181B;
    }
    
    /* Butonlar */
    .stButton > button {
        background-color: #18181B;
        border: 1px solid rgba(34, 197, 94, 0.3);
        color: #F9FAFB;
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        border-color: #22C55E;
        color: #22C55E;
        background-color: #111827;
    }

    /* Sohbet Balonları */
    [data-testid="stChatMessage"] {
        background-color: transparent;
        border: none;
        padding: 1.5rem 0;
    }
    [data-testid="stChatMessage"][data-baseweb="flex"]:has(div:contains("user")) {
        background-color: #18181B;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.05);
        padding: 1.5rem;
    }

    /* Girdi Alanı */
    [data-testid="stChatInput"] {
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        background-color: #18181B !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #22C55E !important;
    }

    /* Kart Tasarımları (Flashcard & Quiz Sonuçları) */
    .bilgi-karti {
        background-color: #111827;
        border-left: 4px solid #22C55E;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.2rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        border-right: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# ==========================================
# ANA EKRAN AKIŞI
# ==========================================
st.title("🛡️ NexusDoc Workspace")

if not st.session_state.is_uploaded:
    # --- YALNIZCA YÜKLEME EKRANI ---
    st.markdown("<h3 style='text-align: center; color: #9CA3AF; font-weight: 400; margin-bottom: 3rem;'>Sistemi başlatmak için dokümanınızı yükleyin</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_file = st.file_uploader("", type=["pdf"])
        if uploaded_file is not None:
            if st.button("Sisteme Yükle ve Analizi Başlat", use_container_width=True):
                with st.spinner("Doküman işleniyor ve vektörize ediliyor..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    try:
                        response = requests.post(f"{API_URL}/upload", files=files)
                        if response.status_code == 200 and response.json().get("durum") in ["basarili", "başarılı"]:
                            st.session_state.is_uploaded = True
                            st.session_state.doc_name = uploaded_file.name
                            st.rerun()
                        else:
                            st.error("Yükleme başarısız.")
                    except requests.exceptions.ConnectionError:
                        st.error("Sunucu bağlantı hatası.")
else:
    # --- DOKÜMAN YÜKLENDİKTEN SONRAKİ ÇALIŞMA ALANI ---
    col_baslik, col_buton = st.columns([4, 1])
    with col_baslik:
        st.success(f"📄 **{st.session_state.doc_name}** belleğe yüklendi ve analize hazır.")
    with col_buton:
        if st.button("Sıfırla / Yeni Belge"):
            st.session_state.clear()
            st.rerun()
            
    st.divider()

    # ODA YAPISI (SEKMELER)
    tab_chat, tab_quiz, tab_flashcard = st.tabs([
        "💬 Sohbet Odası", 
        "📝 Sınav Odası", 
        "🗂️ Bilgi Kartları"
    ])

    # 1. ODA: SOHBET
    with tab_chat:
        st.subheader("Doküman Asistanı")
        for mesaj in st.session_state.mesajlar:
            with st.chat_message(mesaj["rol"]):
                st.markdown(mesaj["icerik"])

        soru = st.chat_input("Dokümanla ilgili sorgunuzu buraya yazın...")
        if soru:
            st.session_state.mesajlar.append({"rol": "user", "icerik": soru})
            with st.chat_message("user"):
                st.markdown(soru)
                
            with st.spinner("Motor yanıtlıyor..."):
                try:
                    response = requests.post(f"{API_URL}/ask", json={"soru": soru})
                    if response.status_code == 200:
                        cevap = response.json().get("cevap", "")
                        st.session_state.mesajlar.append({"rol": "assistant", "icerik": cevap})
                        st.rerun()
                except Exception:
                    st.error("Bağlantı hatası.")

    # 2. ODA: SINAV MATRİSİ (EKSİK ŞIKLAR DÜZELTİLDİ)
    with tab_quiz:
        st.subheader("Otomatik Sınav Simülasyonu")
        st.markdown("Dokümanın tamamı analiz edilerek 3 soruluk bir test oluşturulur.")
        
        if st.button("Sınav Motorunu Çalıştır", use_container_width=True):
            with st.spinner("Sorular ve şıklar hazırlanıyor..."):
                try:
                    res = requests.get(f"{API_URL}/generate_quiz")
                    if res.status_code == 200 and res.json().get("durum") == "basarili":
                        st.session_state.quiz_verisi = res.json().get("quiz")
                except Exception:
                    st.error("Sınav üretilemedi.")
                    
        if st.session_state.quiz_verisi:
            st.write("---")
            with st.form(key="quiz_form"):
                user_answers = {}
                for idx, q in enumerate(st.session_state.quiz_verisi):
                    st.markdown(f"**Soru {idx+1}: {q['soru']}**")
                    # Şıklar (seçenekler) kullanıcının seçmesi için radio bileşeniyle ekranda!
                    secim = st.radio("Cevabınız:", options=q['secenekler'], key=f"q_{idx}")
                    user_answers[idx] = secim
                    st.write("") 
                
                submit_button = st.form_submit_button(label="🎯 Yanıtları Doğrula")
                
                if submit_button:
                    st.markdown("### 📊 Analiz Raporu")
                    dogru_sayisi = 0
                    for idx, q in enumerate(st.session_state.quiz_verisi):
                        user_ans = user_answers[idx]
                        correct_ans = q['dogru_cevap']
                        
                        if user_ans.strip() == correct_ans.strip():
                            st.success(f"✅ **Doğru!** Senin Seçimin: {user_ans}")
                            dogru_sayisi += 1
                        else:
                            st.error(f"❌ **Yanlış!** Senin Seçimin: {user_ans} | Doğru Cevap: {correct_ans}")
                        
                        st.info(f"💡 **Açıklama:** {q['aciklama']}")
                        st.write("---")
                    
                    st.metric(label="Toplam Başarı", value=f"{dogru_sayisi} / 3")

    # 3. ODA: BİLGİ KARTLARI (KART TASARIMI EKLENDİ)
    with tab_flashcard:
        st.subheader("Akıllı Bilgi Kartları")
        st.markdown("Kritik terminolojiyi öğrenmek için kavram kartları oluşturun.")
        
        if st.button("Bilgi Kartlarını Çıkar", use_container_width=True):
            with st.spinner("Kavramlar analiz ediliyor..."):
                try:
                    res = requests.get(f"{API_URL}/generate_flashcards")
                    if res.status_code == 200 and res.json().get("durum") == "basarili":
                        st.session_state.flashcard_verisi = res.json().get("kartlar")
                except Exception:
                    st.error("Kartlar üretilemedi.")

        if st.session_state.flashcard_verisi:
            st.write("---")
            for kart in st.session_state.flashcard_verisi:
                # Expander yerine profesyonel kart tasarımı (CSS ile)
                st.markdown(f"""
                <div class="bilgi-karti">
                    <h4 style="margin: 0 0 10px 0; color: #F9FAFB;">{kart['terim']}</h4>
                    <p style="margin: 0; color: #9CA3AF; line-height: 1.6;">{kart['tanim']}</p>
                </div>
                """, unsafe_allow_html=True)