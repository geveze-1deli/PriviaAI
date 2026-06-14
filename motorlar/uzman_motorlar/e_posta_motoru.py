import re
from motorlar.sonuc_motoru.sonuc_motoru import raporu_teslim_al


EP_REGEX = r"^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$"

def kademe1_sinav(kelime):
    return bool(re.match(EP_REGEX, kelime))

def kademe2_tamir(kelime):
    
    while len(kelime) > 0 and not kelime[0].isalnum():
        kelime = kelime[1:]
    while len(kelime) > 0 and not kelime[-1].isalnum():
        kelime = kelime[:-1]
    return kelime

def hata_analizi(kelime):
    if kademe1_sinav(kademe2_tamir(kelime)):
        return "tamir_edilebilir"
    return "cope_at"

def e_posta_baslat(eposta_ham_listesi):
    gecerli_epostalar = []

    for kelime in eposta_ham_listesi:
        if kademe1_sinav(kelime):
            gecerli_epostalar.append(kelime)
        else:
            durum = hata_analizi(kelime)
            if durum == "tamir_edilebilir":
                tamir_edilen = kademe2_tamir(kelime)
                if kademe1_sinav(tamir_edilen):
                    gecerli_epostalar.append(tamir_edilen)
            else:
                continue

    raporu_teslim_al("e_posta", gecerli_epostalar)