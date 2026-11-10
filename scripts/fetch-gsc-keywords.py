#!/usr/bin/env python3
"""
Çelebi Yönetim & Temizlik - Google Search Console (GSC) Veri Entegratörü
Google Search Console'daki gerçek arama sorgularını çeker ve PocketBase 'seo_keywords' kuyruğuna aktarır.
"""

import os
import sys
import json
import urllib.request
from datetime import datetime, timedelta

# Google Auth Libraries
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except ImportError:
    print("[WARN] google-api-python-client ve google-auth kurulu olmalıdır.")

CREDENTIALS_PATHS = [
    "/var/www/credentials/gsc-service-account.json",
    os.path.join(os.path.dirname(__file__), "..", "vault", "credentials", "gsc-service-account.json"),
    "vault/credentials/gsc-service-account.json"
]

SITE_URLS = [
    "sc-domain:celebiyonetim.com.tr",
    "https://celebiyonetim.com.tr/",
    "http://celebiyonetim.com.tr/"
]

PB_URL = os.environ.get("POCKETBASE_URL") or "http://127.0.0.1:8090"
PB_USER = os.environ.get("POCKETBASE_ADMIN_EMAIL") or "emrggck@gmail.com"
PB_PASS = os.environ.get("POCKETBASE_ADMIN_PASSWORD") or "Awseqdll.12"

def get_credentials_path():
    for p in CREDENTIALS_PATHS:
        if os.path.exists(p):
            return p
    return None

def get_gsc_service(creds_path):
    scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
    service = build("searchconsole", "v1", credentials=creds)
    return service

def fetch_search_console_queries(service):
    """
    Search Console'dan son 28 günlük arama sorgularını çeker.
    """
    end_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    request_body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query"],
        "rowLimit": 100
    }

    last_error = None
    for site_url in SITE_URLS:
        try:
            print(f"[*] Deneniyor: {site_url}...")
            response = service.searchanalytics().query(siteUrl=site_url, body=request_body).execute()
            rows = response.get("rows", [])
            print(f"[OK] {site_url} mülkünden {len(rows)} adet arama sorgusu başarıyla çekildi.")
            return site_url, rows
        except Exception as e:
            last_error = e
            # Try next format
            continue

    print(f"[!] GSC Sorgu Hatası (Search Console'a henüz veri düşmemiş veya izin bekleniyor olabilir): {last_error}")
    return None, []

def detect_district_and_category(query):
    q_lower = query.lower()
    
    district = "Adana Geneli"
    if "çukurova" in q_lower or "cukurova" in q_lower:
        district = "Çukurova"
    elif "seyhan" in q_lower:
        district = "Seyhan"
    elif "yüreğir" in q_lower or "yuregir" in q_lower:
        district = "Yüreğir"
    elif "sarıçam" in q_lower or "saricam" in q_lower:
        district = "Sarıçam"

    category = "Site Yönetimi"
    if any(k in q_lower for k in ["temizlik", "merdiven", "inşaat sonrası", "ofis temizliği"]):
        category = "Temizlik"
    elif any(k in q_lower for k in ["aidat", "icra", "hukuk", "kmk", "kat mülkiyeti", "karar"]):
        category = "Hukuk & Mevzuat"

    return district, category

def sync_queries_to_pocketbase(rows):
    if not rows:
        print("[INFO] PocketBase'e aktarılacak yeni GSC sorgusu bulunamadı.")
        return 0

    # PocketBase Superuser Auth
    auth_data = json.dumps({"identity": PB_USER, "password": PB_PASS}).encode("utf-8")
    req = urllib.request.Request(
        f"{PB_URL}/api/collections/_superusers/auth-with-password",
        data=auth_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        token = json.loads(resp.read().decode())["token"]

    headers = {"Authorization": token, "Content-Type": "application/json"}

    # Get existing keywords
    req = urllib.request.Request(f"{PB_URL}/api/collections/seo_keywords/records?page=1&perPage=500", headers=headers)
    with urllib.request.urlopen(req) as resp:
        existing = json.loads(resp.read().decode()).get("items", [])
    
    existing_keywords = {item["keyword"].lower().strip(): item["id"] for item in existing if "keyword" in item}

    added_count = 0
    for row in rows:
        query = row["keys"][0].strip()
        clicks = int(row.get("clicks", 0))
        impressions = int(row.get("impressions", 0))
        position = round(float(row.get("position", 0)), 1)
        
        # Priority score: impressions * 2 + clicks * 10
        priority = max(5, min(99, impressions * 2 + clicks * 10))

        district, category = detect_district_and_category(query)

        if query.lower() not in existing_keywords:
            payload = {
                "keyword": query,
                "category": category,
                "district": district,
                "priority": priority,
                "used": False
            }
            create_req = urllib.request.Request(
                f"{PB_URL}/api/collections/seo_keywords/records",
                data=json.dumps(payload).encode("utf-8"),
                headers=headers
            )
            try:
                with urllib.request.urlopen(create_req):
                    added_count += 1
                    print(f"  [+] Kuyruğa eklendi: '{query}' (Gösterim: {impressions}, Sıra: {position})")
            except Exception as e:
                print(f"  [!] Ekleme hatası '{query}': {e}")
        else:
            # Already exists
            pass

    print(f"\n[TAMAMLANDI] Toplam {added_count} adet yeni arama sorgusu PocketBase SEO kuyruğuna eklendi.")
    return added_count

def test_connection():
    creds_path = get_credentials_path()
    if not creds_path:
        print("[HATA] gsc-service-account.json dosyası bulunamadı!")
        return False

    print(f"[*] Kimlik dosyası bulundu: {creds_path}")
    try:
        service = get_gsc_service(creds_path)
        site_url, rows = fetch_search_console_queries(service)
        if site_url is not None:
            sync_queries_to_pocketbase(rows)
            return True
        else:
            return False
    except Exception as e:
        print(f"[HATA] Google API bağlantı hatası: {e}")
        return False

if __name__ == "__main__":
    test_connection()

