import os
import re


mevcut_dizin = os.path.dirname(os.path.abspath(__file__))
ISIMLER_PATH = os.path.join(mevcut_dizin, "isimler.txt")

def cift_format_temizle_ve_kaydet(dosya_yolu):
    if not os.path.exists(dosya_yolu):
        print(f"Hata: {dosya_yolu} bulunamadı!")
        return

    try:
        
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            satirlar = f.readlines()

        yeni_liste = set()

        for satir in satirlar:
            ham_isim = satir.strip()
            if not ham_isim:
                continue
            
            
            kok_isim = re.split(r"['’\"“”\-]", ham_isim)[0].strip()
            
            if kok_isim:
                
                parcalar = kok_isim.split()
                formatli_parcalar = []
                for p in parcalar:
                    if p:
                        
                        bas = p[0].replace('i', 'İ').replace('ı', 'I').upper()
                        son = p[1:].replace('İ', 'i').replace('I', 'ı').lower()
                        formatli_parcalar.append(bas + son)
                
                bas_harfi_buyuk = " ".join(formatli_parcalar)
                yeni_liste.add(bas_harfi_buyuk)

                tamami_buyuk = kok_isim.replace('i', 'İ').replace('ı', 'I').upper()
                yeni_liste.add(tamami_buyuk)

        
        with open(dosya_yolu, "w", encoding="utf-8") as f:
            for isim in sorted(list(yeni_liste)):
                f.write(isim + "\n")
        
        print(f"İşlem Başarılı!")
        print(f"Hem 'Ali' hem 'ALİ' formatları eklendi.")
        print(f"Toplam benzersiz satır sayısı: {len(yeni_liste)}")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    cift_format_temizle_ve_kaydet(ISIMLER_PATH)