from motorlar.sonuc_motoru.sonuc_motoru import raporu_teslim_al

def luhn_kontrol(tc):
    """
    2. AŞAMA: Luhn Algoritması Kontrolü
    """
    rakamlar = [int(r) for r in tc]
    
    tekler = sum(rakamlar[0:9:2])
    ciftler = sum(rakamlar[1:8:2])
    
    kontrol_10 = (tekler * 7 - ciftler) % 10
    if kontrol_10 != rakamlar[9]:
        return False
        
    kontrol_11 = sum(rakamlar[0:10]) % 10
    if kontrol_11 != rakamlar[10]:
        return False
        
    return True

def tc_ozellik_kontrol(tc):
    """
    3. AŞAMA: TC Kimlik Kanunu Şartları
    """
    if tc[0] == '0':
        return False
    
    if int(tc[10]) % 2 != 0:
        return False
        
    return True

def tc_baslat(ham_sayilar):
    """
    ANA MOTOR tarafından gönderilen ham sayı listesini işler.
    Tüm sınavları (Hane, Luhn, Özellik) yapar ve 
    GEÇERLİ OLAN HER ŞEYİ Sonuç Motoruna gönderir.
    """
    gecerli_tcler_listesi = []

    for aday in ham_sayilar:
        if len(aday) == 11:
            
            if luhn_kontrol(aday):
                
                if tc_ozellik_kontrol(aday):
                    
                    gecerli_tcler_listesi.append(aday)

    raporu_teslim_al(motor_adi="tc_no", veri=gecerli_tcler_listesi)