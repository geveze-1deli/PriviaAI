import os
import json
import requests
from dotenv import load_dotenv

# Hugging Face veya yerel ortam fark etmeksizin anahtarı güvenli okuma altyapısı
su_an_bulundugun_yer = os.path.dirname(os.path.abspath(__file__))
ana_sayfa_katmani = os.path.dirname(su_an_bulundugun_yer)
proje_kok_dizini = os.path.dirname(ana_sayfa_katmani)

dotenv_yolu = os.path.join(proje_kok_dizini, '.env')
if os.path.exists(dotenv_yolu):
    load_dotenv(dotenv_path=dotenv_yolu)

# Hugging Face Secret kasasından veya yerel .env'den anahtarı çeker
API_KEY = os.environ.get("OPENAI_API_KEY")

def yapay_zeka_isim_motoru(orijinal_metin):
    """
    Metni analiz ederek uydurma ilişki ağlarını  
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
    Sen PriviaAI siber güvenlik ve veri analizi sisteminin ultra kesinlikli "Şahıs İsmi Tespit Motoru"sun. 
    Sana verilen metindeki kişisel veri niteliği taşıyan GERÇEK İNSAN ÖZEL İSİMLERİNİ (Örn: Ali Yılmaz, Fatma, Saim Sakaoğlu) tespit etmekle görevlisin.
    
    KESİN UYULMASI GEREKEN FİLTRELEME KURALLARI:
    1. Sadece gerçek insan özel isimlerini al. "Annesi", "Padişah", "Müdür", "Arap", "Kız", "Kadın", "Memur" gibi unvan, rol, meslek veya cins isimlerini KESİNLİKLE LİSTEYE ALMA.
    2. "Ahmet'in babası", "Mehmet'in arkadaşı" gibi iyelik/akrabalık/ilişki belirten tamlamaları yapısal olarak pas geç. Metinde o kişilerin yalın ve gerçek bir özel ismi geçmiyorsa hiçbir şekilde listeye ekleme.
    3. Metinde açıkça yer almayan, ima edilen veya türetilen hiçbir ismi kafandan uydurma.
    4. Çıktı Biçimi: Bulguları sadece aralarında virgül olan, temiz bir isim listesi olarak dön (Örn: Ahmet Yılmaz, Mustafa, Ayşe).
    5. Eğer metinde KVKK kapsamında risk oluşturacak hiçbir gerçek şahıs özel ismi yoksa SADECE "BOŞ" yaz. Asla açıklama cümlesi kurma.
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
                # Kesme işaretinden sonrasını temizle (Örn: "Ahmet'in" -> "Ahmet" yapar, ismi çöpe atmaz)
                if "'" in isim:
                    isim = isim.split("'")[0].strip()
                if "’" in isim:
                    isim = isim.split("’")[0].strip()
                    
                isim_alt = isim.lower()
                
                # Yasaklı kelime kontrolü
                if any(y in isim_alt for y in yasakli_kelimeler) or len(isim) < 2:
                    continue
                
                if isim not in temiz_isimler:
                    temiz_isimler.append(isim)
                
            return temiz_isimler
        return []
    except:
        return []

def gemini_analiz_ve_sohbet(kullanici_mesajı, motor_sonuclari):
    if not API_KEY: 
        return "Sistem hatası: API anahtarı bulunamadı."
        
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    
    # Yapay zekanın ne iş yapacağını ve kullanıcıya nasıl cevap vereceğini netleştirdik
    sistem_talimati = (
        f"Sen PriviaAI siber güvenlik ve KVKK uzmanı yapay zekasısın. "
        f"Sistem tarafından tespit edilen mevcut şahıs isimleri şunlardır: {motor_sonuclari}. "
        f"Kullanıcının sana sorduğu sorulara bu bulgular ışığında, bilgilendirici, net ve kurumsal bir dille cevap ver."
    )
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": sistem_talimati},
            {"role": "user", "content": kullanici_mesajı}
        ],
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        res = response.json()
        if response.status_code == 200:
            return res["choices"][0]["message"]["content"].strip()
        else:
            return f"Hata Oluştu: {res.get('error', {}).get('message', 'Bilinmeyen hata')}"
    except Exception as e: 
        return f"Bağlantı hatası: {str(e)}"
