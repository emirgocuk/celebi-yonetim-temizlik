#!/usr/bin/env python3
"""
Celebi Yonetim ve Temizlik - Otonom SEO Makale ve Icerik Motoru (Cron Worker)
Her calistiginda PocketBase seo_keywords kuyrugundan bir konu alir,
220+ kelimelik, 3+ H2 baslikli, Celebi CTA'li SEO makalesini uretir ve PocketBase yazilar tablosuna kaydeder.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime

# Load .env file automatically if present
def load_dotenv():
    search_paths = [
        os.path.join(os.path.dirname(__file__), "..", ".env"),
        os.path.join(os.path.dirname(__file__), ".env"),
        os.path.abspath(".env"),
        "/var/www/celebiyonetim/.env"
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
IMGBB_KEY = os.environ.get("IMGBB_API_KEY") or os.environ.get("PUBLIC_IMGBB_API_KEY") or ""

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

def get_pb_token():
    url = f"{PB_URL}/api/collections/_superusers/auth-with-password"
    data = json.dumps({"identity": PB_USER, "password": PB_PASS}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())["token"]

def slugify(text):
    tr_map = str.maketrans("çÇğĞıİöÖşŞüÜ", "ccggiioossuu")
    text = text.translate(tr_map).lower()
    import re
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text).strip("-")
    return text

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
    req = urllib.request.Request(url, data=data, headers={"Authorization": token, "Content-Type": "application/json"})
    req.get_method = lambda: 'PATCH'
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"[WARN] Failed to mark keyword used: {e}")

def generate_article_body(keyword, district="Çukurova"):
    # Deterministic high quality Adana KMK & Cleaning template
    months = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    now = datetime.now()
    date_str = f"{now.day} {months[now.month-1]} {now.year}"

    # Intelligent Title & Prefix Normalization
    dist = district.strip() if district else "Çukurova"
    if dist in ["Adana Geneli", "Adana", "Genel", "auto", ""]:
        prefix = "Adana Genelinde"
    elif dist.lower().startswith("adana "):
        prefix = f"{dist} Genelinde"
    else:
        prefix = f"Adana {dist} Genelinde"

    import re
    clean_kw = keyword.strip()
    if dist not in ["Adana Geneli", "Adana", "Genel", "auto", ""]:
        clean_kw = re.sub(rf"^(Adana\s+)?{re.escape(dist)}\s*", "", clean_kw, flags=re.IGNORECASE)
    clean_kw = re.sub(r"^Adana\s+(Geneli\s+)?", "", clean_kw, flags=re.IGNORECASE)
    clean_kw = re.sub(r"^Genelinde\s*", "", clean_kw, flags=re.IGNORECASE)
    clean_kw = clean_kw[0].upper() + clean_kw[1:] if clean_kw else keyword

    # Dynamic Category & Suffix Detection
    kw_lower = clean_kw.lower()
    if any(k in kw_lower for k in ["temizlik", "merdiven", "tadilat", "inşaat", "hijyen", "ofis"]):
        category = "Temizlik"
        category_color = "emerald"
        suffix = "Uygulama ve Hizmet Rehberi"
    else:
        category = "Site Yönetimi"
        category_color = "blue"
        suffix = "Yasal Mevzuat ve Uygulama Rehberi"

    if ":" in clean_kw or "?" in clean_kw:
        title = f"{prefix} {clean_kw}"
    else:
        title = f"{prefix} {clean_kw}: {suffix}"

    title = re.sub(r"\bAdana\s+Adana\b", "Adana", title, flags=re.IGNORECASE)
    title = re.sub(r"\bAdana\s+Geneli\s+Genelinde\b", "Adana Genelinde", title, flags=re.IGNORECASE)

    slug = f"{slugify(title)}-{int(time.time())}"

    body = f"""<p>Adana'da konut ve iş yeri projelerinin hızla arttığı {district} bölgesinde toplu yaşam alanlarında huzur ve düzen sağlamak, 634 Sayılı Kat Mülkiyeti Kanunu (KMK) standartlarına harfiyen uyulmasını zorunlu kılmaktadır. Bireysel yönetim girişimlerinin sıklıkla tıkandığı aidat tahsilatları, merdiven temizliği sözleşmeleri ve genel kurul süreçleri kurumsal bir yaklaşımla çözülmelidir.</p>

<h2>Kat Mülkiyeti Kanunu Çerçevesinde Şeffaf Yönetim Esasları</h2>
<p>Apartman veya sitenizde yaşanan aidat karmaşası, geciken ortak alan arızaları ve denetlenemeyen harcamalar komşuluk bağlarına zarar verir. Kurumsal yönetim firması her ay düzenli yayınlanan banka onaylı gelir-gider tabloları ve noter tasdikli karar defterleriyle süreci tamamen şeffaf kılar.</p>
<ul>
  <li><strong>İşletme Projesi Tebliği:</strong> Tahmini yıllık bütçe tüm kat maliklerine yasal sürelerde tebliğ edilir ve kesinleşir.</li>
  <li><strong>Banka Onaylı Tahsilat:</strong> Elden para toplama usulsüzlüklerine son verilerek bina adına açılan resmi hesaplar kullanılır.</li>
  <li><strong>Hukuki Danışmanlık:</strong> Aidatını ödemeyen maliklere karşı KMK Madde 20 uyarınca aylık %5 gecikme tazminatı ve icra takipleri yürütülür.</li>
</ul>

<h2>Ortak Alanların Hijyeni ve SGK Güvenceli Temizlik</h2>
<p>Bina merdivenleri, asansör kabinleri ve giriş hollerinin temizliğinde sigortasız eleman çalıştırmak apartman yöneticilerine ve daire sakinlerine ağır idari para cezaları getirebilir. Çelebi Yönetim ve Temizlik olarak görevlendirdiğimiz tüm personel SGK'lı ve iş sağlığı güvenliği eğitimlidir.</p>

<h2>Adana İklim Şartlarına Uygun Periyodik Bakım</h2>
<p>Çukurova'nın yoğun sıcaklıkları ve yüksek nemi, hidrofor sistemleri ve su depolarında düzenli dezenfeksiyonu şart koşar. Periyodik su deposu temizliği, havuz ilaçlamaları ve bahçe peyzaj bakımları Çelebi uzmanlığıyla aksatılmadan tamamlanır.</p>

<h2>Çelebi Yönetim ile Binalarınız Güvence Altında</h2>
<p>Apartmanınızda veya sitenizde profesyonel site yönetimi ve kurumsal temizlik hizmeti almak için Adana Mahfesığmaz merkez ofisimize bekleriz. Ücretsiz yerinde keşif ve işletme projesi analizi için bize <strong>0 (322) 235 15 88</strong> santral hattımızdan veya <strong>0 (535) 873 03 24</strong> WhatsApp numaramızdan 7/24 ulaşabilirsiniz.</p>

<div id="celebi-internal-links" class="mt-8 pt-6 border-t border-slate-200/80 bg-slate-50/60 p-4 rounded-2xl">
  <p class="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">İlgili Hizmet ve Rehber Sayfalarımız:</p>
  <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-sky-700 font-semibold">
    <li><a href="/site-yonetimi">🏢 Adana Profesyonel Site ve Apartman Yönetimi</a></li>
    <li><a href="/temizlik">✨ Kurumsal Ofis, İnşaat ve Merdiven Temizliği</a></li>
    <li><a href="/yazilar">📚 Kat Mülkiyeti Kanunu ve Sektörel Makaleler</a></li>
    <li><a href="/iletisim">📍 Çukurova / Mahfesığmaz Ofisimiz ve İletişim</a></li>
  </ul>
</div>"""

    return {
        "baslik": title,
        "slug": slug,
        "ozet": body,
        "kategori": category,
        "kategoriRenk": category_color,
        "tarih": date_str,
        "okumaSuresi": "4 dk okuma",
        "aktif": True,
        "seoTitle": f"{title} | Çelebi Yönetim",
        "seoDescription": f"{title} konusunda kat mülkiyeti, aidat tahsilatı ve profesyonel temizlik çözümleri rehberi.",
        "kapakGorsel": get_royalty_free_image(keyword, category),
        "kaynak": "Çelebi Yönetim Otomasyon Masası",
        "views": 0
    }

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Celebi Content Engine Cron...")
    try:
        token = get_pb_token()
        print("[OK] Authenticated with PocketBase.")
    except Exception as e:
        print(f"[ERR] Could not authenticate with PocketBase: {e}")
        return

    kw_item = get_next_keyword(token)
    if not kw_item:
        print("[INFO] No unused keywords found in seo_keywords. Using fallback keyword.")
        keyword = "Profesyonel Site Yönetimi ve Aidat Hukuku"
        district = "Çukurova"
        kw_id = None
    else:
        keyword = kw_item.get("keyword")
        district = kw_item.get("targetDistrict", "Çukurova")
        kw_id = kw_item.get("id")
        print(f"[OK] Selected keyword from queue: '{keyword}' ({district})")

    article_payload = generate_article_body(keyword, district)

    # Save to PocketBase yazilar
    url = f"{PB_URL}/api/collections/yazilar/records"
    data = json.dumps(article_payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Authorization": token, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            saved = json.loads(r.read().decode())
            print(f"[SUCCESS] Published article to PocketBase: ID={saved['id']}, Slug={saved['slug']}")
            if kw_id:
                mark_keyword_used(token, kw_id)
                print(f"[OK] Marked keyword {kw_id} as used.")
    except Exception as e:
        print(f"[ERR] Failed to save article to PocketBase: {e}")

if __name__ == "__main__":
    main()
