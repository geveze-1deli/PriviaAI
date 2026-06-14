import re
from motorlar.uzman_motorlar.tc_no_motoru import tc_baslat
from motorlar.uzman_motorlar.e_posta_motoru import e_posta_baslat
from motorlar.uzman_motorlar.isim_motoru import isim_baslat
from motorlar.uzman_motorlar.tel_no_motoru import tel_no_baslat
def parantez_izole_et(metin):
    """
    E-posta ayıklama öncesi parantezleri çevre kelimelerden ayırır.
    """
    yeni_metin = ""
    for i in range(len(metin)):
        karakter = metin[i]
        if karakter == "(" and i > 0:
            if metin[i-1] != " ":
                yeni_metin += " "
        yeni_metin += karakter
        if karakter == ")" and i < len(metin) - 1:
            if metin[i+1] != " ":
                yeni_metin += " "
    return yeni_metin

def buyuk_harf_grupla(ham_metin):
    """
    KİŞİ İSMİ PAKETLEME SİSTEMİ (GÜNCELLENDİ):
    Büyük harfle başlayan kelimeleri gruplar. 
    Eğer kelime içinde veya sonunda harf/rakam olmayan (noktalama, sembol vb.)
    bir karakter varsa grubu orada böler.
    """
    izole_metin = parantez_izole_et(ham_metin)
    kelimeler = izole_metin.split()
    
    gruplar = []
    gecici_grup = []

    for kelime in kelimeler:
        ayirici_var_mi = re.search(r'[^a-zA-Z0-9çğıöşüÇĞİÖŞÜ]', kelime)
        
        
        if kelime and kelime[0].isupper():
            gecici_grup.append(kelime) 
            
            
            if ayirici_var_mi:
                gruplar.append(gecici_grup)
                gecici_grup = []
        else:
            
            if gecici_grup:
                gruplar.append(gecici_grup)
                gecici_grup = []
    
    if gecici_grup:
        gruplar.append(gecici_grup)
        
    return gruplar

def analiz_baslat(ham_metin):
    """
    ANADOLU DAĞITIM MERKEZİ:
    Ham metni parçalar ve ilgili uzman motorlara kargolar.
    """
    
    
    tc_ham_verisi = re.findall(r'\d+', ham_metin)
    
    
    izole_metin = parantez_izole_et(ham_metin)
    kelimeler = izole_metin.split()
    eposta_ham_verisi = [kelime for kelime in kelimeler if '@' in kelime]

    
    isim_paketleri = buyuk_harf_grupla(ham_metin)

    
    potansiyel_tel_gruplari = re.findall(r'[+\d\s().-]{7,25}', ham_metin)
    tel_ham_verisi = []
    
    for grup in potansiyel_tel_gruplari:
        
        temiz_rakam = re.sub(r'\D', '', grup)
        if 7 <= len(temiz_rakam) <= 12:
            tel_ham_verisi.append(grup.strip())

    
    tc_baslat(tc_ham_verisi)
    e_posta_baslat(eposta_ham_verisi)
    isim_baslat(isim_paketleri)
    tel_no_baslat(tel_ham_verisi)