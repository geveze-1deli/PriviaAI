import os
import json
import requests
from dotenv import load_dotenv

su_an_bulundugun_yer = os.path.dirname(os.path.abspath(__file__))
ana_sayfa_katmani = os.path.dirname(su_an_bulundugun_yer)
proje_kok_dizini = os.path.dirname(ana_sayfa_katmani)

dotenv_yolu = os.path.join(proje_kok_dizini, '.env')
load_dotenv(dotenv_path=dotenv_yolu)

API_KEY = os.environ.get("OPENAI_API_KEY")

def yapay_zeka_isim_motoru(orijinal_metin):
    """
    Metni analiz ederek uydurma ilişki ağlarını ("Keloğlan'ın karısı" vb.) 
    ve cins isimleri ("Padişah", "Annesi" vb.) tamamen eleyen, 
    sadece gerçek şahıs özel isimlerini bulan ultra kesinlikli motor.
    """
    if not API_KEY:
        return []

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    sistem_talimati = """
    Sen PriviaAI siber güvenlik sisteminin Şahıs İsmi Tespit Motorusun. Sana verilen metindeki GERÇEK İNSAN ÖZEL İSİMLERİNİ bulmalısın.
    
    YASAKLAR VE KESİN KURALLAR:
    1. "Annesi", "Padişah", "Arap", "Kız", "Koca nine", "Kadın", "Zebella", "Tellâl", "Cariye" gibi kelimeler ÖZEL İNSAN İSMİ DEĞİLDİR, unvan veya roldür. Bunları LİSTEYE ALMAK KESİNLİKLE YASAKTIR.
    2. "Keloğlan'ın karısı", "Keloğlan'ın bacısı", "Keloğlan'ın dostu" gibi iyelik takısı almış ilişki ve akrabalık tanımlarını LİSTEYE ASLA ALMA. Metinde o kişilerin gerçek bir özel ismi (Örn: Ali, Fatma) geçmiyorsa onları tamamen pas geç.
    3. "Zümrüt-ü Anka" bir kuş/yaratık adıdır, insan ismi değildir. ASLA ALMA.
    4. Metinde açıkça yazmayan hiçbir ismi kafandan uydurma, türetme.
    5. Çıktıyı sadece saf isimlerden oluşan, aralarında virgül olan temiz bir liste olarak ver. (Örn: Keloğlan, Saim Sakaoğlu)
    6. Eğer metinde hiçbir gerçek şahıs özel ismi yoksa SADECE "BOŞ" yaz. Cümle kurma.
    """

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": sistem_talimati},
            {"role": "user", "content": f"Metin:\n{orijinal_metin}"}
        ],
        "temperature": 0.1  
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        cevap_json = response.json()
        if response.status_code == 200:
            sonuc = cevap_json["choices"][0]["message"]["content"].strip()
            if sonuc == "BOŞ" or not sonuc:
                return []
            
            ham_isimler = [i.strip() for i in sonuc.split(",") if i.strip()]
            
            temiz_isimler = []
            yasakli_kelimeler = ["annesi", "padişah", "arap", "karısı", "bacısı", "kardeşi", "sevgilisi", "düşmanı", "komşusu", "arkadaşı", "akrabası", "dostu", "anka", "kuşu"]
            
            for isim in ham_isimler:
                isim_alt = isim.lower()
                
                if "’" in isim or "'" in isim or any(y in isim_alt for y in yasakli_kelimeler):
                    continue
                temiz_isimler.append(isim)
                
            return temiz_isimler
        return []
    except:
        return []

def gemini_analiz_ve_sohbet(kullanici_mesajı, motor_sonuclari):
    
    if not API_KEY: return ""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": f"Sen PriviaAI KVKK uzmanısın. Mevcut sonuçlar: {motor_sonuclari}"},
            {"role": "user", "content": kullanici_mesajı}
        ],
        "temperature": 0.7
    }
    try:
        res = requests.post(url, headers=headers, json=payload).json()
        return res["choices"][0]["message"]["content"].strip()
    except: return ""