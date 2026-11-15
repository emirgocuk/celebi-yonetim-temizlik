#!/usr/bin/env python3
"""
Çelebi Yönetim & Temizlik - GSC ve Adana Yerel Trend Entegratörü
1. Google Search Console'dan gerçek arama sorgularını çeker.
2. Google Suggest / Autocomplete üzerinden Adana ve Çukurova yerel trendlerini araştırır.
3. Çekilen tüm yeni ve yüksek ticari niyetli konuları PocketBase 'seo_keywords' kuyruğuna kaydeder.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
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

PB_URL = os.environ.get("POCKETBASE_URL") or os.environ.get("PUBLIC_POCKETBASE_URL") or "http://127.0.0.1:8090"
PB_USER = os.environ.get("PB_USER") or os.environ.get("POCKETBASE_ADMIN_EMAIL") or "emrggck@gmail.com"
PB_PASS = os.environ.get("PB_PASS") or os.environ.get("POCKETBASE_ADMIN_PASSWORD") or "Awseqdll.12"

# Adana seed keywords for Google Suggest & local trend harvesting
ADANA_TREND_SEEDS = [
    # Site & Apartman Yönetimi
    "adana site yönetimi",
    "adana apartman yönetimi",
    "adana site yönetim şirketleri",
    "adana apartman aidat takibi",
    "adana kat mülkiyeti yönetici seçimi",
    "çukurova site yönetimi",
    "seyhan apartman yönetimi",
    "adana site işletme projesi",
    "adana apartman yönetim fiyatları",
    "adana bina yöneticiliği şirketi",
    # Temizlik Hizmetleri
    "adana temizlik şirketi",
    "adana temizlik şirketleri fiyatları",
    "adana ofis temizliği",
    "adana kurumsal temizlik firmaları",
    "adana inşaat sonrası temizlik",
    "adana apartman merdiven temizliği",
    "adana dış cephe cam temizliği vinç",
    "çukurova temizlik şirketi",
    "seyhan temizlik şirketi",
    "mahfesığmaz temizlik şirketi",
    "turgut özal bulvarı temizlik",
    "güzelyalı merdiven temizliği",
    # Hukuk & İcra Mevzuatı
    "adana aidat ödemeyen komşuya icra",
    "kat mülkiyeti aidat gecikme faizi",
    "site yöneticisi karar defteri noter"
]

# Negative keywords to filter out irrelevant noise
NEGATIVE_KEYWORDS = [
    "eleman", "iş ilanı", "iş ilanları", "eleman arayanlar", "maaş", "sahibinden",
    "kariyer", "günlük ev", "bayan", "bay", "@", ".com", "pdf", "indir", "ekşi"
]

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
    Search Console'dan son 28 günlük organik arama sorgularını çeker.
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
            print(f"[*] GSC mülkü deneniyor: {site_url}...")
            response = service.searchanalytics().query(siteUrl=site_url, body=request_body).execute()
            rows = response.get("rows", [])
            print(f"[OK] {site_url} mülkünden {len(rows)} adet organik arama sorgusu başarıyla çekildi.")
            return site_url, rows
        except Exception as e:
            last_error = e
            continue

    print(f"[!] GSC Sorgu Bildirimi: {last_error}")
    return None, []

def harvest_adana_google_trends():
    """
    Google Autocomplete API üzerinden Adana genelindeki gerçek kullanıcı arama trendlerini çeker.
    """
    print("[*] Google Autocomplete üzerinden Adana yerel trendleri taranıyor...")
    discovered = []
    seen = set()

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    for seed in ADANA_TREND_SEEDS:
        encoded = urllib.parse.quote(seed)
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&hl=tr&gl=tr&q={encoded}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read().decode("utf-8"))
                suggestions = data[1] if len(data) > 1 else []
                for s in suggestions:
                    s_clean = s.strip()
                    s_lower = s_clean.lower()
                    
                    # Filter noise
                    if any(neg in s_lower for neg in NEGATIVE_KEYWORDS):
                        continue
                    if len(s_clean) < 5 or s_lower in seen:
                        continue

                    seen.add(s_lower)
                    discovered.append({
                        "query": s_clean,
                        "source": "google_suggest",
                        "priority": 35
                    })
        except Exception as e:
            # Continue gracefully
            pass

    print(f"[OK] Adana genelinde {len(discovered)} adet gerçek arama trendi tespit edildi.")
    return discovered

def detect_district_and_category(query):
    q_lower = query.lower()
    
    district = "Adana Geneli"
    if any(k in q_lower for k in ["çukurova", "cukurova", "mahfesığmaz", "turgut özal", "kenan evren", "güzelyalı", "beyazevler", "toros", "kurttepe"]):
        district = "Çukurova"
    elif any(k in q_lower for k in ["seyhan", "ziyapaşa", "gazipaşa", "reşatbey", "cemalpaşa", "sümer"]):
        district = "Seyhan"
    elif any(k in q_lower for k in ["yüreğir", "yuregir"]):
        district = "Yüreğir"
    elif any(k in q_lower for k in ["sarıçam", "saricam"]):
        district = "Sarıçam"

    category = "Site Yönetimi"
    if any(k in q_lower for k in ["temizlik", "merdiven", "inşaat sonrası", "ofis temizliği", "dış cephe"]):
        category = "Temizlik"
    elif any(k in q_lower for k in ["aidat", "icra", "hukuk", "kmk", "kat mülkiyeti", "karar defteri", "noter", "dava"]):
        category = "Hukuk & Mevzuat"

    return district, category

def sync_to_pocketbase(gsc_rows, trend_items):
    """
    GSC ve Trend verilerini PocketBase 'seo_keywords' tablosuna kaydeder.
    """
    # 1. PocketBase Superuser Auth
    auth_data = json.dumps({"identity": PB_USER, "password": PB_PASS}).encode("utf-8")
    req = urllib.request.Request(
        f"{PB_URL}/api/collections/_superusers/auth-with-password",
        data=auth_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        token = json.loads(resp.read().decode())["token"]

    headers = {"Authorization": token, "Content-Type": "application/json"}

    # 2. Get existing keywords
    req = urllib.request.Request(f"{PB_URL}/api/collections/seo_keywords/records?page=1&perPage=500", headers=headers)
    with urllib.request.urlopen(req) as resp:
        existing = json.loads(resp.read().decode()).get("items", [])
    
    existing_keywords = {item["keyword"].lower().strip(): item["id"] for item in existing if "keyword" in item}

    added_count = 0

    # 3. Process GSC queries (highest priority)
    for row in (gsc_rows or []):
        query = row["keys"][0].strip()
        clicks = int(row.get("clicks", 0))
        impressions = int(row.get("impressions", 0))
        position = round(float(row.get("position", 0)), 1)
        priority = max(50, min(99, impressions * 2 + clicks * 10))

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
                    existing_keywords[query.lower()] = True
                    print(f"  [GSC+] Kuyruğa eklendi: '{query}' (Gösterim: {impressions}, Sıra: {position})")
            except Exception as e:
                print(f"  [!] GSC Ekleme hatası '{query}': {e}")

    # 4. Process Google Trend queries
    for item in (trend_items or []):
        query = item["query"].strip()
        priority = item.get("priority", 35)

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
                    existing_keywords[query.lower()] = True
                    print(f"  [Trend+] Kuyruğa eklendi: '{query}' ({district} - {category})")
            except Exception as e:
                print(f"  [!] Trend Ekleme hatası '{query}': {e}")

    print(f"\n[TAMAMLANDI] Toplam {added_count} adet yeni arama sorgusu/trend konusu PocketBase SEO kuyruğuna eklendi.")
    return added_count

def run_harvest():
    print(f"\n=== Çelebi GSC & Adana Trend Entegratörü [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ===")
    
    # 1. GSC Queries
    gsc_rows = []
    creds_path = get_credentials_path()
    if creds_path:
        try:
            service = get_gsc_service(creds_path)
            _, gsc_rows = fetch_search_console_queries(service)
        except Exception as e:
            print(f"[!] GSC Bağlantı Uyarısı: {e}")
    else:
        print("[!] GSC kimlik dosyası bulunamadı, doğrudan Adana trendlerine geçiliyor.")

    # 2. Adana Trend Queries
    trend_items = harvest_adana_google_trends()

    # 3. Sync all to PocketBase
    total_added = sync_to_pocketbase(gsc_rows, trend_items)
    return total_added

if __name__ == "__main__":
    run_harvest()
