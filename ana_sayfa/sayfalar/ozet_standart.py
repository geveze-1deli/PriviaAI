import streamlit as st
import pandas as pd
from sayfalar.ozet_excel import excel_indir_merkezi
from sayfalar.ozet_csv import csv_indir_merkezi
from motorlar.sonuc_motoru.sonuc_motoru import final_paketini_hazirla

def analiz_standart_tablosu():
    """
    Standart Analiz Paneli: 
    Arayüzden bağımsız, doğrudan sonuc_motoru ile haberleşir.
    Transpoze mantığı ile verileri tam yerine oturtur.
    """
    
    final_paket = final_paketini_hazirla()
    stats = final_paket.get('standart_istatistik', {})

    st.write("---")
    st.subheader("📊 Analiz Veri Dağılım Paneli (Misafir)")

    
    def guvenli_liste(liste):
        
        if isinstance(liste, list) and len(liste) == 3:
            return liste
        return [0, 0, 0]

    basliklar = ["TC No", "Kişi İsmi", "Telefon No", "E-Posta"]
    
    tablo_verisi = {}
    for b in basliklar:
        
        tablo_verisi[b] = guvenli_liste(stats.get(b))
 
    df_ozet = pd.DataFrame(tablo_verisi, index=["Farklı", "Aynı", "Toplam"]).T
    
    
    df_ozet.index.name = "Kategori"
    df_ozet = df_ozet.reset_index()

    
    st.dataframe(df_ozet, use_container_width=True, hide_index=True)

    
    col1, col2 = st.columns(2)
    with col1:
        excel_indir_merkezi(ozet_df=df_ozet)
    with col2:
        csv_indir_merkezi(ozet_df=df_ozet)
    
    st.warning("🔐 Detaylar kilitli. İçerik listeleri için operatör girişi yapın.")