#!/usr/bin/env python3
"""
Çelebi Yönetim & Temizlik - Yüksek Satın Alma / Arama Niyetli Anahtar Kelime Yükleyici
Adana yerel pazarında telefon araması ve teklif talebi getirecek ticari niyetli sorguları PocketBase'e yükler.
"""

import paramiko
import json

SERVER_IP = "2.27.101.128"
USERNAME = "root"
PASSWORD = "aQsu1G72f!"

HIGH_INTENT_KEYWORDS = [
    # 1. Merdiven ve Ortak Alan Temizliği (Yüksek Çağrı Hacmi)
    {
        "keyword": "Apartman Merdiven Temizliği Fiyatları 2026",
        "category": "Temizlik",
        "district": "Çukurova",
        "priority": 95
    },
    {
        "keyword": "Merdiven Temizliği Şirketleri ve Fiyat Teklifi",
        "category": "Temizlik",
        "district": "Seyhan",
        "priority": 90
    },
    {
        "keyword": "Bina Ortak Alan ve Asansör Temizliği Sözleşmesi",
        "category": "Temizlik",
        "district": "Çukurova",
        "priority": 85
    },
    {
        "keyword": "Haftalık Düzenli Apartman Temizliği Ücretleri",
        "category": "Temizlik",
        "district": "Sarıçam",
        "priority": 85
    },
    {
        "keyword": "Apartman Görevlisi Yerine Temizlik Şirketi Maliyet Avantajı",
        "category": "Temizlik",
        "district": "Adana Geneli",
        "priority": 80
    },
    {
        "keyword": "Mahfesığmaz Merdiven Temizliği Hizmeti ve Fiyatları",
        "category": "Temizlik",
        "district": "Çukurova",
        "priority": 92
    },
    {
        "keyword": "Beyazevler Apartman Temizlik Şirketi Tavsiye",
        "category": "Temizlik",
        "district": "Çukurova",
        "priority": 88
    },
    {
        "keyword": "Turgut Özal Bulvarı Site ve Apartman Temizlik Hizmetleri",
        "category": "Temizlik",
        "district": "Çukurova",
        "priority": 90
    },

    # 2. İnşaat ve Tadilat Sonrası Temizlik (Yüksek Gelirli Hizmetler)
    {
        "keyword": "İnşaat Sonrası Daire ve Villa Temizliği Fiyatları",
        "category": "Temizlik",
        "district": "Çukurova",
        "priority": 96
    },
    {
        "keyword": "Tadilat Sonrası Anahtar Teslim Temizlik Şirketleri",
        "category": "Temizlik",
        "district": "Seyhan",
        "priority": 92
    },
    {
        "keyword": "Sıfır Daire İnşaat Pisliği ve Harç Lekesi Temizliği",
        "category": "Temizlik",
        "district": "Adana Geneli",
        "priority": 88
    },
    {
        "keyword": "Yeni Teslim Edilen Toplu Konut ve Site İnşaat Temizliği",
        "category": "Temizlik",
        "district": "Sarıçam",
        "priority": 86
    },
    {
        "keyword": "Taşınma Öncesi Boş Ev ve Daire Temizliği Fiyatları",
        "category": "Temizlik",
        "district": "Çukurova",
        "priority": 90
    },

    # 3. Profesyonel Site & Apartman Yönetimi (Yıllık Kurumsal Sözleşmeler)
    {
        "keyword": "Profesyonel Site Yönetimi Fiyatları ve Hizmet Kapsamı 2026",
        "category": "Site Yönetimi",
        "district": "Çukurova",
        "priority": 98
    },
    {
        "keyword": "Apartman Yönetim Şirketleri Telefon Numaraları ve Danışmanlık",
        "category": "Site Yönetimi",
        "district": "Seyhan",
        "priority": 94
    },
    {
        "keyword": "Site İşletme Projesi Hazırlama ve Noter Onay Süreçleri",
        "category": "Site Yönetimi",
        "district": "Çukurova",
        "priority": 88
    },
    {
        "keyword": "Apartman Aidatını Ödemeyen Maliklere İcra Takibi Nasıl Başlatılır?",
        "category": "Site Yönetimi",
        "district": "Adana Geneli",
        "priority": 95
    },
    {
        "keyword": "Bina Yönetimini Profesyonel Şirkete Devretme Karar Defteri Örneği",
        "category": "Site Yönetimi",
        "district": "Çukurova",
        "priority": 90
    },
    {
        "keyword": "Site Yöneticiliği Hizmet Sözleşmesi ve Yasal Sorumluluklar",
        "category": "Site Yönetimi",
        "district": "Yüreğir",
        "priority": 82
    },
    {
        "keyword": "En İyi Site ve Apartman Yönetim Firmaları Karşılaştırma",
        "category": "Site Yönetimi",
        "district": "Adana Geneli",
        "priority": 85
    },

    # 4. Kurumsal Ofis ve İş Yeri Temizliği (B2B Müşteriler)
    {
        "keyword": "Kurumsal Ofis ve İş Yeri Temizliği Aylık Fiyat Teklifi",
        "category": "Temizlik",
        "district": "Seyhan",
        "priority": 94
    },
    {
        "keyword": "Klinik, Muayenehane ve Sağlık Merkezi Hijyen Protokolleri",
        "category": "Temizlik",
        "district": "Çukurova",
        "priority": 90
    },
    {
        "keyword": "Plaza ve İş Merkezi Periyodik Temizlik Hizmetleri",
        "category": "Temizlik",
        "district": "Seyhan",
        "priority": 86
    },
    {
        "keyword": "Akşam Mesai Sonrası Ofis Temizliği Şirketleri",
        "category": "Temizlik",
        "district": "Çukurova",
        "priority": 88
    },

    # 5. Özel Tesis ve Acil Bakım Hizmetleri
    {
        "keyword": "Apartman Su Deposu Temizliği ve Dezenfeksiyonu Fiyatları",
        "category": "Temizlik",
        "district": "Çukurova",
        "priority": 92
    },
    {
        "keyword": "Dış Cephe Cam Temizliği ve Vinçli Yıkama Hizmeti",
        "category": "Temizlik",
        "district": "Adana Geneli",
        "priority": 89
    },
    {
        "keyword": "Apartman Aydınlatma, Hidrofor ve Ortak Alan Teknik Bakımı",
        "category": "Site Yönetimi",
        "district": "Seyhan",
        "priority": 80
    }
]

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, 22, USERNAME, PASSWORD, timeout=10)

    # 1. Fetch existing keywords to prevent duplicates
    cmd = 'curl -s "http://127.0.0.1:8090/api/collections/seo_keywords/records?page=1&perPage=500"'
    _, o, _ = ssh.exec_command(cmd)
    raw = o.read().decode()
    existing_items = json.loads(raw).get('items', [])
    existing_names = {it['keyword'].strip().lower(): it['id'] for it in existing_items if 'keyword' in it}

    print(f"[*] Veritabanındaki mevcut kayıt sayısı: {len(existing_names)}")
    added = 0
    updated = 0

    for item in HIGH_INTENT_KEYWORDS:
        kw = item["keyword"].strip()
        kw_lower = kw.lower()

        payload = {
            "keyword": kw,
            "category": item["category"],
            "district": item["district"],
            "priority": item["priority"],
            "used": False
        }
        payload_json = json.dumps(payload).replace("'", "'\\''")

        if kw_lower in existing_names:
            # Update priority
            rec_id = existing_names[kw_lower]
            up_cmd = f"curl -s -X PATCH 'http://127.0.0.1:8090/api/collections/seo_keywords/records/{rec_id}' -H 'Content-Type: application/json' -d '{payload_json}'"
            ssh.exec_command(up_cmd)
            updated += 1
        else:
            # Create new
            in_cmd = f"curl -s -X POST 'http://127.0.0.1:8090/api/collections/seo_keywords/records' -H 'Content-Type: application/json' -d '{payload_json}'"
            _, res, _ = ssh.exec_command(in_cmd)
            res_str = res.read().decode()
            if '"id"' in res_str:
                added += 1
                print(f"  [+] Yeni eklendi: '{kw}' ({item['district']} - Öncelik: {item['priority']})")
            else:
                print(f"  [!] Ekleme hatası '{kw}': {res_str[:150]}")

    print(f"\n[TAMAMLANDI] Toplam {added} adet yüksek ticari niyetli anahtar kelime eklendi, {updated} adet güncellendi.")
    ssh.close()

if __name__ == "__main__":
    main()

