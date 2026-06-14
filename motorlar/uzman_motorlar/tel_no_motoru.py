import re

tel_no_sonuclar = []

def tel_no_baslat(gelen_veri_listesi):
    """
    Ana motordan gelen potansiyel veri gruplarını 
    T.C. telefon numarası standartlarına göre doğrular.
    """
    global tel_no_sonuclar
    tel_no_sonuclar.clear() 

    for veri in gelen_veri_listesi:
        saf_rakam = re.sub(r'\D', '', veri)

        if len(saf_rakam) == 11 and saf_rakam.startswith("0"):
            saf_rakam = saf_rakam[1:]
        elif len(saf_rakam) == 12 and saf_rakam.startswith("90"):
            saf_rakam = saf_rakam[2:]

        if tc_telefon_mu(saf_rakam):
            tel_no_sonuclar.append(formatla_ve_maskele(saf_rakam))

def tc_telefon_mu(rakam_dizisi):
    """
    Bir rakam dizisinin T.C. telefon numarası olup olmadığını teyit eder.
    Zaten yukarıda temizlediğimiz için burada ağırlıklı 10 hane kontrolü yapacağız.
    """
    uzunluk = len(rakam_dizisi)
    
    if uzunluk not in [7, 10]:
        return False

    if uzunluk == 7:
        return rakam_dizisi.startswith("444")

    if uzunluk == 10:
        alan_kodu = rakam_dizisi[:3]
        if alan_kodu.startswith(("2", "3", "4", "5", "8")):
            return True

    return False

def formatla_ve_maskele(rakam_dizisi):
    """
    Tespit edilen numarayı standart 10 haneli formatta tutar.
    """
    return rakam_dizisi

def sonuclari_getir():
    """Arayüz katmanının sonuçları çekmesi için kullanılır."""
    return list(set(tel_no_sonuclar))