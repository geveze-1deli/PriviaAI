import streamlit as st
import os

def yonetici_girisi():
    su_an_neredeyim = os.path.dirname(os.path.abspath(__file__))
    ana_sayfa = os.path.dirname(su_an_neredeyim)
    dosya_yolu = os.path.join(ana_sayfa, "kullanicilar.txt")

    with st.sidebar:
        st.header("🛡️ PRIVIA AI V2.0")
        
        
        if not st.session_state.get("giris_basarili"):
            with st.expander("🔐 OPERATÖR GİRİŞİ", expanded=False):
                
                with st.form(key="login_form"):
                    k_adi = st.text_input("Kullanıcı Adı", key="op_user_input")
                    sifre = st.text_input("Şifre", type="password", key="op_pass_input")
                    dogrula = st.form_submit_button("Doğrula")
                
                if dogrula:
                    if os.path.exists(dosya_yolu):
                        with open(dosya_yolu, "r", encoding="utf-8") as txt_dosyasi:
                            satirlar = [s.strip() for s in txt_dosyasi.readlines() if s.strip()]
                            giris_bilgisi = "{},{}".format(k_adi.strip(), sifre.strip())
                            
                            if giris_bilgisi in satirlar:
                                st.session_state["giris_basarili"] = True
                                st.session_state["kullanici_rolu"] = "operatör"
                                
                                
                                st.session_state["analiz_aktif"] = False
                                st.session_state["son_analiz_sonucu"] = None
                                
                                st.success("Giriş Başarılı!")
                                st.rerun() 
                            else:
                                st.error("Hatalı Kullanıcı veya Şifre!")
                    else:
                        st.error("Dosya bulunamadı!")

            st.markdown("---")
            if st.button("👤 MİSAFİR GİRİŞİ", use_container_width=True, key="guest_entry"):
                st.session_state["giris_basarili"] = True
                st.session_state["kullanici_rolu"] = "misafir"
                
                
                st.session_state["analiz_aktif"] = False
                st.session_state["son_analiz_sonucu"] = None
                
                st.rerun()

        
        else:
            st.info(f"Oturum Açık: {st.session_state.kullanici_rolu.upper()}")
            
            if st.button("🚪 Oturumu Kapat", use_container_width=True):
                
                st.session_state["giris_basarili"] = False
                st.session_state["kullanici_rolu"] = None
                
                
                st.session_state["analiz_aktif"] = False
                st.session_state["son_analiz_sonucu"] = None
                
                
                if "metin_input" in st.session_state:
                    st.session_state["metin_input"] = ""
                
                st.rerun()