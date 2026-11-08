#!/usr/bin/env python3
"""
Çelebi Yönetim ve Temizlik - Otonom Zamanlayıcı & Otomatik Yayınlayıcı (Timer Runner)
PocketBase 'otomatik_yayin_ayarlari' tablosundaki ayarlara göre periyodik olarak makale üretip yayınlar.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

# Auto-load .env
def load_dotenv():
    search_paths = [
        os.path.join(os.path.dirname(__file__), "..", ".env"),
        os.path.join(os.path.dirname(__file__), ".env"),
        "/var/www/celebiyonetim/.env",
        os.path.abspath(".env")
    ]
    for p in search_paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'").strip('"')
                        if k and k not in os.environ:
                            os.environ[k] = v
            break

load_dotenv()

PB_URL = os.environ.get("POCKETBASE_URL") or os.environ.get("PUBLIC_POCKETBASE_URL") or "http://127.0.0.1:8090"
PB_USER = os.environ.get("PB_USER") or os.environ.get("POCKETBASE_ADMIN_EMAIL") or "emrggck@gmail.com"
PB_PASS = os.environ.get("PB_PASS") or os.environ.get("POCKETBASE_ADMIN_PASSWORD") or "Awseqdll.12"
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("PUBLIC_OPENROUTER_API_KEY") or ""

STOCK_IMAGES = {
    "hukuk_icra": [
        "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=1200&q=80"
    ],
    "kurumsal_temizlik": [
        "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1628177142898-93e36e4e3a50?auto=format&fit=crop&w=1200&q=80"
    ],
    "insaat_temizlik": [
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1600565193348-f74bd3c7ccdf?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=80"
    ],
    "dis_cephe": [
        "https://images.unsplash.com/photo-1506146332389-18140dc7b2fb?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80"
    ],
    "merdiven_apartman": [
        "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1200&q=80"
    ],
    "site_yonetimi": [
        "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1574362848149-11496d93a7c7?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&q=80"
    ]
}

def get_royalty_free_image(topic, category=""):
    t = f"{topic} {category}".lower()
    import zlib
    seed = abs(zlib.crc32(topic.encode("utf-8")))

    if any(k in t for k in ["aidat", "icra", "kanun", "kmk", "hukuk", "dava", "borç", "muhasebe", "bütçe"]):
        pool = STOCK_IMAGES["hukuk_icra"]
    elif any(k in t for k in ["dış cephe", "cam", "vinç", "kompozit", "yüksek"]):
        pool = STOCK_IMAGES["dis_cephe"]
    elif any(k in t for k in ["inşaat", "tadilat", "harç", "boya", "anahtar teslim"]):
        pool = STOCK_IMAGES["insaat_temizlik"]
    elif any(k in t for k in ["ofis", "kurumsal", "plaza", "şirket", "iş yeri"]):
        pool = STOCK_IMAGES["kurumsal_temizlik"]
    elif any(k in t for k in ["merdiven", "asansör", "ortak alan", "apartman temizli"]):
        pool = STOCK_IMAGES["merdiven_apartman"]
    else:
        pool = STOCK_IMAGES["site_yonetimi"]

    return pool[seed % len(pool)]

DISTRICTS = ["Çukurova", "Seyhan", "Yüreğir", "Sarıçam"]

def slugify(text):
    tr_map = str.maketrans("çÇğĞıİöÖşŞüÜ", "ccggiioossuu")
    text = text.translate(tr_map).lower()
    import re
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text).strip("-")
    return text

def get_pb_token():
    url = f"{PB_URL}/api/collections/_superusers/auth-with-password"
    data = json.dumps({"identity": PB_USER, "password": PB_PASS}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())["token"]

def get_settings():
    url = f"{PB_URL}/api/collections/otomatik_yayin_ayarlari/records"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as r:
        res = json.loads(r.read().decode())
        if res.get("items"):
            return res["items"][0]
    return None

def update_settings(token, record_id, data):
    url = f"{PB_URL}/api/collections/otomatik_yayin_ayarlari/records/{record_id}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": token},
        method="PATCH"
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())

def get_next_keyword(token):
    filter_q = urllib.parse.quote("used = false")
    url = f"{PB_URL}/api/collections/seo_keywords/records?page=1&perPage=1&filter={filter_q}&sort=-priority"
    req = urllib.request.Request(url, headers={"Authorization": token})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            res = json.loads(r.read().decode())
            if res.get("items"):
                return res["items"][0]
    except Exception as e:
        print(f"[WARN] Error fetching keyword: {e}")
    return None

def mark_keyword_used(token, kw_id):
    url = f"{PB_URL}/api/collections/seo_keywords/records/{kw_id}"
    data = json.dumps({"used": True, "lastGenerated": datetime.now().isoformat()}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "Authorization": token}, method="PATCH")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"[WARN] Error updating keyword: {e}")
    return None

def count_remaining_keywords():
    try:
        filter_q = urllib.parse.quote("used = false")
        url = f"{PB_URL}/api/collections/seo_keywords/records?page=1&perPage=1&filter={filter_q}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode()).get("totalItems", 0)
    except Exception:
        return 0

def generate_article_content(topic, district):
    title = f"Adana {district} Genelinde {topic}: Yasal Mevzuat ve Uygulama Rehberi"
    slug = f"{slugify(title)}-{int(time.time())}"
    category = "Site Yönetimi"
    cat_color = "blue"

    body_html = f"""<p>Adana'nın yükselen yerleşim bölgesi {district} genelinde toplu yaşam alanlarında huzur ve düzenin temini, 634 Sayılı Kat Mülkiyeti Kanunu (KMK) hükümlerine harfiyen riayet edilmesinden geçer. Gerek apartman yönetim kurulları gerekse site sakinleri açısından {topic.lower()} konusu hukuki ve idari netlik gerektirir.</p>

<h2>Kat Mülkiyeti Kanunu Çerçevesinde Yasal Sorumluluklar ve Süreçler</h2>
<p>Kat malikleri kurulunun olağan veya olağanüstü toplantılarında alınan kararlar, noter onaylı karar defterine işlenmediği takdirde yasal geçerlilik kazanmaz. KMK Madde 20 kapsamında her kat maliki, ortak alanların bakım, onarım ve personel giderlerine arsa payı oranında katılmakla mükelleftir. Vaktinde ifa edilmeyen aidat ve avans ödemeleri için aylık %5 gecikme tazminatı işletilerek ilamsız icra takibi başlatılabilir.</p>
<ul>
  <li><strong>Resmi Banka Hesabı Zorunluluğu:</strong> Apartman adına açılmış vadeli/vadesiz hesaplar üzerinden şeffaf harcama dökümü.</li>
  <li><strong>Denetim Raporlarının İlanı:</strong> Yılda en az bir defa bağımsız denetçi tarafından hazırlanan gelir-gider teftiş raporu.</li>
  <li><strong>İşletme Projesi Tebliği:</strong> Tahmini yıllık bütçenin kat maliklerine noter veya taahhütlü mektupla yazılı bildirimi.</li>
</ul>

<h2>Ortak Alanların Hijyeni ve SGK Güvenceli Profesyonel Temizlik</h2>
<p>Merdiven boşlukları, asansör kabinleri, kapalı otoparklar ve sığınak alanlarının periyodik dezenfeksiyonu bina sağlığı açısından kritiktir. Sigortasız gündelikçi istihdamı, bina yönetimini ve tüm daire sahiplerini ağır idari para cezaları ve iş kazası tazminat riskleriyle karşı karşıya bırakır. Çelebi Yönetim bünyesinde görev yapan tüm personel SGK güvenceli ve mesleki yeterlilik belgelidir.</p>

<h2>Çukurova İkliminde Tesis ve Mekanik Donanım Bakımları</h2>
<p>Adana'nın nemli ve sıcak yaz şartlarında hidrofor motorları, asansör halatları ve çatılardaki güneş enerjisi sistemleri arıza riskini artırır. Periyodik teknik kontroller ve sözleşmeli mühendislik hizmetleri bina sakinlerinin güvenliğini garanti altına alır.</p>

<h2>Çelebi Yönetim ve Temizlik ile Profesyonel Çözüm Ortaklığı</h2>
<p>Adana Çukurova Mahfesığmaz merkezli Çelebi Yönetim ve Temizlik olarak; şeffaf muhasebe yazılımı, 7/24 teknik müdahale ve uzman temizlik kadromuzla yanınızdayız. Apartmanınız veya siteniz için ücretsiz keşif ve işletme projesi analizi almak üzere <strong>0 (322) 235 15 88</strong> santralimizden veya <strong>0 (535) 873 03 24</strong> WhatsApp hattımızdan bize 7/24 ulaşabilirsiniz.</p>

<div id="celebi-internal-links" class="mt-8 pt-6 border-t border-slate-200/80 bg-slate-50/60 p-4 rounded-2xl">
  <p class="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">İlgili Hizmet ve Rehber Sayfalarımız:</p>
  <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-sky-700 font-semibold">
    <li><a href="/site-yonetimi">🏢 Adana Profesyonel Site ve Apartman Yönetimi</a></li>
    <li><a href="/temizlik">✨ Kurumsal Ofis, İnşaat ve Merdiven Temizliği</a></li>
    <li><a href="/yazilar">📚 Kat Mülkiyeti Kanunu ve Sektörel Makaleler</a></li>
    <li><a href="/iletisim">📍 Çukurova / Mahfesığmaz Ofisimiz ve İletişim</a></li>
  </ul>
</div>"""

    # If OpenRouter Key is configured, attempt AI enrichment
    if OPENROUTER_KEY:
        try:
            req_data = json.dumps({
                "model": "nvidia/nemotron-3.5-lightning:free",
                "messages": [
                    {
                        "role": "system",
                        "content": "Sen Adana Çelebi Yönetim ve Temizlik firmasının içerik uzmanısın. Kat Mülkiyeti Kanunu ve profesyonel temizlik üzerine 250+ kelimelik, 3+ <h2> başlıklı, son paragrafında Çelebi Yönetim (0 322 235 15 88 / WhatsApp 0 535 873 03 24) iletişim çağrılı HTML gövdesi üret. Asla <h1> kullanma."
                    },
                    {
                        "role": "user",
                        "content": f"Konu: {topic} ({district}). Profesyonel Adana yerel SEO makalesi üret."
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1200
            }).encode("utf-8")
            
            ai_req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=req_data,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://celebiyonetim.com.tr",
                    "X-Title": "Celebi Yonetim Content Engine"
                }
            )
            with urllib.request.urlopen(ai_req, timeout=15) as r:
                ai_res = json.loads(r.read().decode())
                ai_text = ai_res.get("choices", [{}])[0].get("message", {}).get("content", "")
                if ai_text and "<p>" in ai_text and "<h2>" in ai_text:
                    body_html = ai_text
                    if "celebi-internal-links" not in body_html:
                        body_html += """
<div id="celebi-internal-links" class="mt-8 pt-6 border-t border-slate-200/80 bg-slate-50/60 p-4 rounded-2xl">
  <p class="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">İlgili Hizmet ve Rehber Sayfalarımız:</p>
  <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-sky-700 font-semibold">
    <li><a href="/site-yonetimi">🏢 Adana Profesyonel Site ve Apartman Yönetimi</a></li>
    <li><a href="/temizlik">✨ Kurumsal Ofis, İnşaat ve Merdiven Temizliği</a></li>
    <li><a href="/yazilar">📚 Kat Mülkiyeti Kanunu ve Sektörel Makaleler</a></li>
    <li><a href="/iletisim">📍 Çukurova / Mahfesığmaz Ofisimiz ve İletişim</a></li>
  </ul>
</div>"""
        except Exception as e:
            print(f"[INFO] OpenRouter polish skipped: {e}, using template engine.")

    return {
        "baslik": title,
        "slug": slug,
        "ozet": body_html,
        "kategori": category,
        "kategoriRenk": cat_color,
        "tarih": datetime.now().strftime("%d %B %Y"),
        "okumaSuresi": "4 dk okuma",
        "aktif": True,
        "seoTitle": f"{title[:55]} | Çelebi",
        "seoDescription": f"Adana {district} bölgesinde {topic} hakkında Kat Mülkiyeti Kanunu ve uzman site yönetimi esasları. Detaylı rehber.",
        "kapakGorsel": get_royalty_free_image(topic, category),
        "kaynak": "Çelebi Yönetim & Hukuk Servisi",
        "views": 1
    }

def save_article_to_pb(token, article_data):
    url = f"{PB_URL}/api/collections/yazilar/records"
    data = json.dumps(article_data).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "Authorization": token})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())

def run_single_publish(token, settings, district=None):
    kw_item = get_next_keyword(token)
    if kw_item:
        topic = kw_item.get("keyword")
        chosen_district = district or kw_item.get("targetDistrict") or "Çukurova"
        kw_id = kw_item.get("id")
    else:
        topic = "Kat Mülkiyeti Kanunu Apartman Aidatı Tahsilat Rehberi"
        chosen_district = district or "Çukurova"
        kw_id = None

    if chosen_district == "auto" or not chosen_district:
        idx = int(settings.get("toplamUretilen", 0)) % len(DISTRICTS)
        chosen_district = DISTRICTS[idx]

    article_data = generate_article_content(topic, chosen_district)
    saved = save_article_to_pb(token, article_data)
    print(f"[SUCCESS] Published: ID={saved.get('id')}, Title='{saved.get('baslik')}'")

    if kw_id:
        mark_keyword_used(token, kw_id)

    # Update settings stats
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_total = int(settings.get("toplamUretilen", 0)) + 1
    update_settings(token, settings["id"], {
        "sonCalisma": now_str,
        "sonBaslik": saved.get("baslik"),
        "sonDurum": "Başarıyla yayınlandı",
        "toplamUretilen": new_total,
        "tetikle": False
    })
    return saved

def should_run(settings):
    if not settings.get("aktif", False):
        return False, "Zamanlayıcı devre dışı (Kapalı)"

    last_str = settings.get("sonCalisma")
    if not last_str:
        return True, "İlk çalışma"

    try:
        last_dt = datetime.strptime(last_str, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return True, "Geçersiz son tarih"

    now = datetime.now()
    diff_sec = (now - last_dt).total_seconds()
    siklik = settings.get("siklik", "6h")

    intervals = {
        "1h": 3600,
        "3h": 10800,
        "6h": 21600,
        "12h": 43200,
        "24h": 86400,
        "daily": 86400
    }

    req_sec = intervals.get(siklik, 21600)
    if diff_sec >= req_sec:
        return True, f"Periyot doldu ({diff_sec:.0f}s >= {req_sec}s)"
    
    return False, f"Bekleniyor ({int((req_sec - diff_sec) / 60)} dakika kaldı)"

def main():
    force = "--force" in sys.argv or "-f" in sys.argv
    settings = get_settings()
    if not settings:
        print("[ERR] No 'otomatik_yayin_ayarlari' record found in PocketBase.")
        return

    # Check if manual trigger requested from admin panel
    if settings.get("tetikle", False) or force:
        print("[INFO] Manual trigger detected! Publishing article immediately...")
        token = get_pb_token()
        run_single_publish(token, settings)
        return

    # Check schedule
    can_run, reason = should_run(settings)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Schedule check: {reason}")
    if can_run:
        token = get_pb_token()
        run_single_publish(token, settings)

if __name__ == "__main__":
    main()

