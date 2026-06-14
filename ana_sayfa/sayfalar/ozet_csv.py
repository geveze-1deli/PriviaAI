import streamlit as st
import pandas as pd


def csv_indir_merkezi(ozet_df):
    rol = st.session_state.get("kullanici_rolu")
    
    
    csv_data = ozet_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    
    dosya_ismi = "privia_VIP_rapor.csv" if rol == "operatör" else "privia_standart_rapor.csv"
    buton_metni = "📊 VIP Özet (CSV)" if rol == "operatör" else "📊 Standart Özet (CSV)"

    st.download_button(
        label=buton_metni,
        data=csv_data,
        file_name=dosya_ismi,
        mime="text/csv",
        use_container_width=True,
        key="main_csv_btn"
    )


def detayli_csv_indir_butonu(liste, dosya_adi="detayli_liste"):
    """
    VIP panelinden gelen Kesin veya Şüpheli listelerini CSV'ye dönüştürür.
    'ozet_vip.py' içindeki 'liste=' ve 'dosya_adi=' çağrılarıyla tam uyumludur.
    """
    
    if not liste:
        return

    df = pd.DataFrame(liste, columns=[dosya_adi.replace("_", " ").title()])
    
    
    csv_detay_data = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    
    st.download_button(
        label=f"📑 {dosya_adi.replace('_', ' ').title()} Listesini İndir (CSV)",
        data=csv_detay_data,
        file_name=f"privia_{dosya_adi}.csv",
        mime="text/csv",
        use_container_width=True,
        key=f"vip_csv_{dosya_adi}_btn" 
    )