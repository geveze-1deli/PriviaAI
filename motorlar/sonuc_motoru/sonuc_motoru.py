from collections import Counter

merkezi_havuz = {
    "tc_no": [], 
    "kisi_ismi": [], 
    "telefon_no": [], 
    "e_posta": [], 
    "konum": []
}

def raporu_teslim_al(motor_adi, veri):
    """
    Uzman motorlardan gelen listeleri teslim alır ve havuza boşaltır.
    """
    if motor_adi in merkezi_havuz:
        merkezi_havuz[motor_adi] = veri if isinstance(veri, list) else []

def final_paketini_hazirla():
    """
    Havuzdaki verileri sayar, istatistik çıkarır ve panellere (VIP/Standart) hazır hale getirir.
    """
    
    
    from motorlar.uzman_motorlar.tel_no_motoru import tel_no_sonuclar
    raporu_teslim_al("telefon_no", tel_no_sonuclar)
    

    istatistik_ozeti = {}

    
    esleme = {
        "tc_no": "TC No",
        "kisi_ismi": "Kişi İsmi", 
        "telefon_no": "Telefon No",
        "e_posta": "E-Posta",
        "konum": "Konum"
    }

    for havuz_anahtari, tablo_basligi in esleme.items():
        liste = merkezi_havuz.get(havuz_anahtari, [])
        
        
        counts = Counter(liste) 
        farkli_adet = sum(1 for x in counts.values() if x == 1)
        ayni_adet = sum(x for x in counts.values() if x > 1)
        toplam_adet = len(liste)
        istatistik_ozeti[tablo_basligi] = [farkli_adet, ayni_adet, toplam_adet]

    
    final_paket = {
        "standart_istatistik": istatistik_ozeti,
        "vip_istatistik": istatistik_ozeti,
        "tam_liste": {
            "TC No": merkezi_havuz["tc_no"],
            "Kişi İsmi": merkezi_havuz["kisi_ismi"], 
            "Telefon No": merkezi_havuz["telefon_no"],
            "E-Posta": merkezi_havuz["e_posta"],
            "Konum": merkezi_havuz["konum"]
        }
    }
    
    return final_paket