import os
import re
from motorlar.sonuc_motoru.sonuc_motoru import raporu_teslim_al

mevcut_dizin = os.path.dirname(__file__)
ISIMLER_PATH = os.path.join(mevcut_dizin, "isimler.txt")
YASAKLI_KELIME_PATH = os.path.join(mevcut_dizin, "yasakli_kelimeler.txt")

def veritabani_yukle(yol):
    """ Dosyayı okur, her satırı KÜÇÜK HARFE çevirir ve boşlukları siler. """
    try:
        with open(yol, "r", encoding="utf-8") as f:
            return {satir.strip().lower() for satir in f if satir.strip()}
    except FileNotFoundError:
        print(f"Hata: {yol} dosyası bulunamadı!")
        return set()

ISIM_VERITABANI = veritabani_yukle(ISIMLER_PATH)
YASAKLI_KELIMELER = veritabani_yukle(YASAKLI_KELIME_PATH)
UNVANLAR = {"sayın", "avukat", "av", "dr", "doktor", "müdür", "sn"}

def ekleri_budama(kelime):
    """ 
    Tek tırnak işaretinden itibaren kelimeyi ve sonrasını siler. 
    Örn: Mustafa'nın -> Mustafa
    """
    return re.split(r"['’\"“”]", kelime)[0]

def isim_baslat(paket_listeleri):
    tespit_edilen_kisiler = []
    romen_deseni = r'\b[IVXLCDM]+(?:-[IVXLCDM]+)*\b'

    for paket in paket_listeleri:
        paket_isim_iceriyor_mu = False
        gecerli_kelimeler = []

        for ham_kelime in paket:
            kelime_temiz = re.sub(romen_deseni, '', ham_kelime).strip()
            
            budanmis_kelime = ekleri_budama(kelime_temiz)
            
            saf_kelime = budanmis_kelime.strip(".,!?;:()[]'\"’“” ")
            
            if not saf_kelime:
                continue
            
            kelime_lower = saf_kelime.lower()
            
            if kelime_lower in YASAKLI_KELIMELER:
                continue
            
            if kelime_lower in ISIM_VERITABANI and kelime_lower not in UNVANLAR:
                paket_isim_iceriyor_mu = True
            
            gecerli_kelimeler.append(saf_kelime)

        if paket_isim_iceriyor_mu and gecerli_kelimeler:
            kisi_adi_final = " ".join(gecerli_kelimeler)
            tespit_edilen_kisiler.append(kisi_adi_final)

    raporu_teslim_al("kisi_ismi", tespit_edilen_kisiler)
    return tespit_edilen_kisiler
