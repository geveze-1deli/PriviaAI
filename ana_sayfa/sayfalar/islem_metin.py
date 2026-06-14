import streamlit as st
from motorlar.ana_motor.ana_motor import analiz_baslat

def metin_isleme_alani():
    st.subheader("📝 Metin Analizi")
    
    
    if "analiz_aktif" not in st.session_state:
        st.session_state["analiz_aktif"] = False

    
    user_text = st.text_area("Analiz Edilecek Metin:", height=250, key="metin_input")

    
    if st.button("🔍 Analizi Başlat", use_container_width=True):
        if user_text.strip() != "":
            with st.spinner("Motorlar çalışıyor..."):
                
                st.session_state["girilen_metin"] = user_text
                st.session_state["yapay_zeka_taramasi_bitti"] = False
                if "motor_sonuclari" in st.session_state:
                    st.session_state.motor_sonuclari["isimler"] = []
                
                
                analiz_baslat(user_text)
                st.session_state["analiz_aktif"] = True
        else:
            st.warning("Metin girilmedi!")
            st.session_state["analiz_aktif"] = False

    
    if st.session_state.get("analiz_aktif"):
        rol = st.session_state.get("kullanici_rolu")
        
        if rol == "operatör":
            from sayfalar.ozet_vip import analiz_vip_sistemi
            analiz_vip_sistemi() 
        else:
            from sayfalar.ozet_standart import analiz_standart_tablosu
            analiz_standart_tablosu()