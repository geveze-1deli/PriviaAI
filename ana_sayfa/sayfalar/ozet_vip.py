import streamlit as st
import pandas as pd
from collections import Counter
from sayfalar.ozet_excel import excel_indir_merkezi, detayli_liste_indir_butonu
from sayfalar.ozet_csv import csv_indir_merkezi, detayli_csv_indir_butonu
from motorlar.sonuc_motoru.sonuc_motoru import final_paketini_hazirla

def analiz_vip_sistemi():
    """
    VIP Analiz Paneli: 
    Aynı verileri (xN) şeklinde gruplayarak görsel kalabalığı önler.
    Artık 'Kişi İsmi' seçildiğinde doğrudan yapay zekanın bulduğu temiz listeyi basar!
    """
    final_paket = final_paketini_hazirla()
    stats = final_paket.get('vip_istatistik', {})
    canli_veriler = final_paket.get('tam_liste', {})

    st.write("---")
    st.success("💎 VIP Analiz Paneli (Tam Erişim)")
    
    
    def guvenli_liste(liste):
        return list(liste) if isinstance(liste, list) and len(liste) == 3 else [0, 0, 0]

    
    basliklar = ["TC No", "Kişi İsmi", "Telefon No", "E-Posta"]
    
    
    if "motor_sonuclari" in st.session_state and "isimler" in st.session_state.motor_sonuclari:
        yz_isimleri = st.session_state.motor_sonuclari["isimler"]
        farkli_yz = len(set(yz_isimleri))
        toplam_yz = len(yz_isimleri)
        ayni_yz = toplam_yz - farkli_yz
        stats["Kişi İsmi"] = [farkli_yz, ayni_yz, toplam_yz]

    tablo_verisi = {}
    for b in basliklar:
        tablo_verisi[b] = guvenli_liste(stats.get(b))

    
    df_ozet_vip = pd.DataFrame(tablo_verisi, index=["Farklı", "Aynı", "Toplam"]).T
    df_ozet_vip.index.name = "Kategori"
    df_ozet_vip = df_ozet_vip.reset_index()
    
    st.dataframe(df_ozet_vip, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1: excel_indir_merkezi(ozet_df=df_ozet_vip)
    with c2: csv_indir_merkezi(ozet_df=df_ozet_vip)

    st.write("---")
    
    
    st.subheader("🔍 Veri Detaylarını İncele")
    
    secenekler = ["TC No", "Kişi İsmi", "Telefon No", "E-Posta"]
    secilen = st.selectbox("İncelemek istediğiniz başlığı seçin:", secenekler)
    
    if secilen == "Kişi İsmi" and "motor_sonuclari" in st.session_state and "isimler" in st.session_state.motor_sonuclari:
        ham_liste = st.session_state.motor_sonuclari["isimler"]
    else:
        
        ham_liste = canli_veriler.get(secilen, [])

    temiz_liste = [v for v in ham_liste if v is not None and str(v).strip() != ""]

    if temiz_liste:
        
        counts = Counter(temiz_liste)
        gorsel_liste = []
        for veri, adet in counts.items():
            if adet > 1:
                gorsel_liste.append(f"{veri} (x{adet})")
            else:
                gorsel_liste.append(str(veri))
        

        if secilen == "TC No":
            st.warning("⚠️ Bu sayı muhtemel bir TC kimlik numarasıdır.")

        st.write(f"📊 **{secilen}** başlığı altındaki güncel kayıtlar:")
        df_detay = pd.DataFrame(gorsel_liste, columns=[secilen])
        st.table(df_detay)
    else:
        st.info(f"Henüz analiz edilmedi veya {secilen} verisi bulunamadı.")