import streamlit as st
import pandas as pd
import io


def excel_indir_merkezi(ozet_df, detay_df=None):
    rol = st.session_state.get("kullanici_rolu")
    buffer = io.BytesIO()
    
    
    ozet_df = ozet_df.astype(str).replace(['None', 'nan', '<NA>'], '')
    
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        ozet_df.to_excel(writer, index=False, sheet_name='Analiz_Ozeti')
        worksheet_ozet = writer.sheets['Analiz_Ozeti']
        
        for i, col in enumerate(ozet_df.columns):
            
            try:
                
                max_val = ozet_df[col].map(lambda x: len(str(x))).max()
                column_len = max(max_val, len(str(col))) + 2
            except:
                
                column_len = 15
            worksheet_ozet.set_column(i, i, column_len)

        if rol == "operatör" and detay_df is not None:
            detay_df = detay_df.astype(str).replace(['None', 'nan', '<NA>'], '')
            detay_df.to_excel(writer, index=False, sheet_name='Veri_Detaylari')
            worksheet_detay = writer.sheets['Veri_Detaylari']
            for i, col in enumerate(detay_df.columns):
                try:
                    max_val = detay_df[col].map(lambda x: len(str(x))).max()
                    column_len = max(max_val, len(str(col))) + 2
                except:
                    column_len = 15
                worksheet_detay.set_column(i, i, column_len)
            
    dosya_ismi = "privia_VIP_rapor.xlsx" if rol == "operatör" else "privia_standart_rapor.xlsx"
    
    st.download_button(
        label="📥 Raporu İndir (Excel)",
        data=buffer.getvalue(),
        file_name=dosya_ismi,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        key="main_excel_btn"
    )


def detayli_liste_indir_butonu(detay_verisi):
    buffer = io.BytesIO()
    sutun_sirasi = ["İsim", "Soy İsmi", "TC No", "Telefon No", "E-Posta", "Konum"]
    
    df = pd.DataFrame(detay_verisi)
    df = df.reindex(columns=sutun_sirasi)
    
    
    df = df.astype(str).replace(['None', 'nan', '<NA>'], '')

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Detayli_Liste_Dokumu')
        worksheet = writer.sheets['Detayli_Liste_Dokumu']
        
        
        for i, col in enumerate(df.columns):
            try:
                
                val_lengths = df[col].apply(lambda x: len(str(x)) if x else 0)
                max_val_len = val_lengths.max() if not val_lengths.empty else 0
                column_len = max(max_val_len, len(str(col))) + 2
            except:
                column_len = 20
                
            worksheet.set_column(i, i, column_len)
        
    st.download_button(
        label="📥 Detaylı Veri Listesini İndir (Excel)",
        data=buffer.getvalue(),
        file_name="privia_VIP_liste_dokumu.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        key="vip_detay_dokum_btn"
    )