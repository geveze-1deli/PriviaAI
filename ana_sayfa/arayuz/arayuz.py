import streamlit as st
import sys
import os

su_an = os.path.dirname(os.path.abspath(__file__)) 
ana_sayfa_yolu = os.path.dirname(su_an)           
ana_kok_dizin = os.path.dirname(ana_sayfa_yolu) 

if ana_sayfa_yolu not in sys.path:
    sys.path.insert(0, ana_sayfa_yolu)
if ana_kok_dizin not in sys.path:
    sys.path.insert(0, ana_kok_dizin)

try:
    from sayfalar.yonetici_paneli import yonetici_girisi
    from sayfalar.islem_metin import metin_isleme_alani
    from sayfalar.islem_belge import belge_yukleme_alani
    from yapay_zeka import yapay_zeka_isim_motoru, gemini_analiz_ve_sohbet
except ImportError as e:
    st.error(f"❌ Modül yükleme hatası: {e}")
    st.stop()

st.set_page_config(page_title="Privia AI v2.0", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

yonetici_girisi()

st.title("🛡️Privia AI v2.0")
st.caption("Veri Analiz ve İstihbarat Platformu")
st.divider()

if not st.session_state.get("giris_basarili"):
    st.warning("⚠️ Erişim Kısıtlı! Lütfen sol taraftaki panelden giriş yöntemini seçin.")
else:
    rol = st.session_state.get("kullanici_rolu", "misafir")
    if rol == "operatör":
        st.success("✅ **Operatör Modu Aktif.**")
    else:
        st.info("👤 **Misafir Modu Aktif.**")

    
    if 'motor_sonuclari' not in st.session_state:
        st.session_state.motor_sonuclari = {"isimler": []}

    sekme_analiz, sekme_yapay_zeka = st.tabs(["📊 Veri Analiz Motorları", "Chat GPT - 4"])

    with sekme_analiz:
        islem_turu = st.radio("İşlem Türü:", ["Metin Girişi", "Belge Yükleme"], horizontal=True)
        st.divider()

        if islem_turu == "Metin Girişi":
            metin_isleme_alani()
            
            
            if st.session_state.get("analiz_aktif") and not st.session_state.get("yapay_zeka_taramasi_bitti"):
                orijinal_metin = st.session_state.get("girilen_metin", "")
                
                if orijinal_metin.strip() != "":
                    bulunan_isimler = yapay_zeka_isim_motoru(orijinal_metin)
                    
                    if 'motor_sonuclari' not in st.session_state:
                        st.session_state.motor_sonuclari = {}
                        
                    st.session_state.motor_sonuclari["isimler"] = bulunan_isimler
                    st.session_state.yapay_zeka_taramasi_bitti = True
                    st.rerun()
            
        elif islem_turu == "Belge Yükleme":
            belge_yukleme_alani()

    with sekme_yapay_zeka:
        st.subheader("🤖 PriviaAI Akıllı Karar Destek Sistemi")
        
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Merhaba. Ben PriviaAI. Verileri analiz edebilir veya sorularını yanıtlayabilirim."}]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if kullanici_girdisi := st.chat_input("Bir şey sorun..."):
            with st.chat_message("user"):
                st.markdown(kullanici_girdisi)
            st.session_state.messages.append({"role": "user", "content": kullanici_girdisi})

            with st.chat_message("assistant"):
                ai_cevabi = gemini_analiz_ve_sohbet(kullanici_girdisi, st.session_state.motor_sonuclari)
                st.markdown(ai_cevabi)
            st.session_state.messages.append({"role": "assistant", "content": ai_cevabi})

    st.divider()
