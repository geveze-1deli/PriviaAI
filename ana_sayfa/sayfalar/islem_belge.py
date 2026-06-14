import streamlit as st
import io
import PyPDF2
from docx import Document
from motorlar.ana_motor.ana_motor import analiz_baslat

def belge_yukleme_alani():
    st.subheader("📁 Belge Analizi")
    
    
    if "belge_analiz_aktif" not in st.session_state:
        st.session_state["belge_analiz_aktif"] = False

    
    yuklenen_dosya = st.file_uploader(
        "Analiz edilecek dosyayı seçin (PDF, TXT, DOCX)", 
        type=["pdf", "txt", "docx"],
        key="belge_uploader"
    )

    
    if st.button("🚀 Belgeyi Analiz Et", use_container_width=True):
        if yuklenen_dosya is not None:
            ham_metin = ""
            dosya_adi = yuklenen_dosya.name
            
            try:
                with st.spinner("Belge okunuyor ve motorlara gönderiliyor..."):
                    
                    if dosya_adi.endswith(".pdf"):
                        pdf_okuyucu = PyPDF2.PdfReader(yuklenen_dosya)
                        for sayfa in pdf_okuyucu.pages:
                            text = sayfa.extract_text()
                            if text:
                                ham_metin += text + "\n"
                    
                    
                    elif dosya_adi.endswith(".docx"):
                        doc = Document(yuklenen_dosya)
                        for paragraf in doc.paragraphs:
                            ham_metin += paragraf.text + "\n"
                    
                    
                    elif dosya_adi.endswith(".txt"):
                        ham_metin = yuklenen_dosya.getvalue().decode("utf-8")

                    
                    if ham_metin.strip() != "":
                        analiz_baslat(ham_metin)
                        st.session_state["belge_analiz_aktif"] = True
                        st.success(f"'{dosya_adi}' başarıyla analiz edildi.")
                    else:
                        st.warning("Dosya içeriği boş veya metin ayıklanamadı!")
                        st.session_state["belge_analiz_aktif"] = False

            except Exception as e:
                st.error(f"Dosya işlenirken bir hata oluştu: {e}")
                st.session_state["belge_analiz_aktif"] = False
        else:
            st.warning("Lütfen önce bir dosya yükleyin!")
            st.session_state["belge_analiz_aktif"] = False

    
    if st.session_state.get("belge_analiz_aktif") and yuklenen_dosya is not None:
        rol = st.session_state.get("kullanici_rolu")
        st.write("---")
        
        if rol == "operatör":
            from sayfalar.ozet_vip import analiz_vip_sistemi
            analiz_vip_sistemi()
        else:
            from sayfalar.ozet_standart import analiz_standart_tablosu
            analiz_standart_tablosu()