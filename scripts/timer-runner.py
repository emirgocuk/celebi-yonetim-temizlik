#!/usr/bin/env python3
"""
Çelebi Yönetim ve Temizlik - Otonom Zamanlayıcı & Yapay Zekâ SEO İçerik Motoru
PocketBase 'otomatik_yayin_ayarlari' ve 'seo_keywords' tablolarına göre özgün makale üretir.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib
from datetime import datetime


def load_dotenv():
    search_paths = [
        "/var/www/celebiyonetim/.env",
        os.path.join(os.path.dirname(__file__), "..", ".env"),
        os.path.join(os.path.dirname(__file__), ".env"),
        os.path.abspath(".env"),
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

DISTRICTS = ["Çukurova", "Seyhan", "Sarıçam", "Yüreğir"]
BACKOFF_FILE = os.path.join(tempfile.gettempdir(), "celebi-ai-backoff.ts")
BACKOFF_SECONDS = 1800

OPENROUTER_MODELS = [
    ("nvidia/nemotron-3-ultra-550b-a55b:free", {"reasoning": {"enabled": False}, "max_tokens": 2400}),
    ("baidu/ernie-5.5-flash-preview:free", {"max_tokens": 2400}),
    ("openrouter/free", {"max_tokens": 2400}),
    ("nvidia/nemotron-3.5-lightning:free", {"max_tokens": 4000}),
]

BOILERPLATE_MARKERS = (
    "Kat Mülkiyeti Kanunu Çerçevesinde Yasal Sorumluluklar ve Süreçler",
    "Kat Mülkiyeti Kanunu Çerçevesinde Şeffaf Yönetim Esasları",
    "Ortak Alanların Hijyeni ve SGK Güvenceli Profesyonel Temizlik",
    "Ortak Alanların Hijyeni ve SGK Güvenceli Temizlik",
    "Çukurova İkliminde Tesis ve Mekanik Donanım Bakımları",
    "Adana İklim Şartlarına Uygun Periyodik Bakım",
)

INTERNAL_LINKS_HTML = """<div id="celebi-internal-links" class="mt-8 pt-6 border-t border-slate-200/80 bg-slate-50/60 p-4 rounded-2xl">
  <p class="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">İlgili Hizmet ve Rehber Sayfalarımız:</p>
  <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-sky-700 font-semibold">
    <li><a href="/site-yonetimi-fiyat-hesapla/">🧮 30 Sn. Site Yönetimi &amp; Aidat Maliyeti Hesapla</a></li>
    <li><a href="/apartman-karar-defteri-ornekleri/">📋 KMK Karar Defteri, Fesih &amp; Devir Örnekleri</a></li>
    <li><a href="/site-yonetimi/">🏢 Adana Profesyonel Site ve Apartman Yönetimi</a></li>
    <li><a href="/temizlik/">✨ Kurumsal Ofis, İnşaat ve Merdiven Temizliği</a></li>
    <li><a href="/cukurova-site-yonetimi/">📍 Çukurova Site &amp; Apartman Yönetimi</a></li>
    <li><a href="/seyhan-apartman-yonetimi/">🏛️ Seyhan Apartman &amp; İş Merkezi Yönetimi</a></li>
    <li><a href="/saricam-site-yonetimi/">🏗️ Sarıçam Toplu Konut &amp; Site Yönetimi</a></li>
    <li><a href="/iletisim/">📞 Mahfesığmaz / Çukurova İletişim &amp; Keşif</a></li>
  </ul>
</div>"""

STOCK_IMAGES = {
    "hukuk_icra": [
        "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=1200&q=80",
    ],
    "kurumsal_temizlik": [
        "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1628177142898-93e36e4e3a50?auto=format&fit=crop&w=1200&q=80",
    ],
    "insaat_temizlik": [
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1600565193348-f74bd3c7ccdf?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=80",
    ],
    "dis_cephe": [
        "https://images.unsplash.com/photo-1506146332389-18140dc7b2fb?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80",
    ],
    "merdiven_apartman": [
        "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1200&q=80",
    ],
    "site_yonetimi": [
        "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1574362848149-11496d93a7c7?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&q=80",
    ],
}


def tr_lower(text: str) -> str:
    return (
        str(text or "")
        .replace("İ", "i")
        .replace("I", "ı")
        .translate(str.maketrans("ÇĞÖŞÜ", "çğöşü"))
        .lower()
    )


def tr_cap_first(text: str) -> str:
    if not text:
        return text
    up_map = {"i": "İ", "ı": "I", "ç": "Ç", "ğ": "Ğ", "ö": "Ö", "ş": "Ş", "ü": "Ü"}
    first = up_map.get(text[0], text[0].upper())
    return first + text[1:]


def slugify(text: str) -> str:
    tr_map = str.maketrans("çÇğĞıİöÖşŞüÜ", "ccggiioossuu")
    s = str(text or "").translate(tr_map).lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s-]+", "-", s).strip("-")
    return s


def detect_category(topic: str, raw_cat: str = "") -> tuple:
    combined = tr_lower(f"{topic} {raw_cat}")
    cleaning_terms = [
        "temizlik", "merdiven", "tadilat", "inşaat", "insaat", "hijyen", "ofis",
        "cam", "vinç", "vinc", "depo", "dezenfeksiyon", "klinik", "plaza",
        "dış cephe", "dis cephe", "boş ev", "bos ev", "daire temizli",
        "halı", "hali", "koltuk", "villa temizli", "muayenehane", "sağlık merkezi",
    ]
    legal_terms = [
        "aidat", "icra", "kmk", "kat mülkiyeti", "kat mulkiyeti", "karar defteri",
        "genel kurul", "yönetici seçimi", "yonetici secimi", "noter", "borç", "borc",
        "dava", "işletme projesi", "isletme projesi", "hukuk", "kanun", "sözleşme", "sozlesme",
    ]
    if any(k in combined for k in cleaning_terms):
        return "Temizlik", "emerald"
    if any(k in combined for k in legal_terms):
        return "Hukuk & Mevzuat", "amber"
    return "Site Yönetimi", "blue"


def detect_district_from_text(text: str):
    low = tr_lower(text)
    if any(k in low for k in ["çukurova", "cukurova", "mahfesığmaz", "mahfesigmaz", "turgut özal", "turgut ozal", "kenan evren", "güzelyalı", "guzelyali", "beyazevler", "toros", "kurttepe"]):
        return "Çukurova"
    if any(k in low for k in ["seyhan", "ziyapaşa", "ziyapasa", "gazipaşa", "gazipasa", "reşatbey", "resatbey", "cemalpaşa", "cemalpasa", "sümer", "sumer"]):
        return "Seyhan"
    if any(k in low for k in ["sarıçam", "saricam"]):
        return "Sarıçam"
    if any(k in low for k in ["yüreğir", "yuregir"]):
        return "Yüreğir"
    return None


def normalize_district(district, settings=None, topic: str = "") -> str:
    alias_map = {
        "çukurova": "Çukurova",
        "cukurova": "Çukurova",
        "seyhan": "Seyhan",
        "sarıçam": "Sarıçam",
        "saricam": "Sarıçam",
        "yüreğir": "Yüreğir",
        "yuregir": "Yüreğir",
    }

    # If the topic itself mentions a specific Adana district or neighborhood, honor it
    topic_dist = detect_district_from_text(topic)
    if topic_dist:
        return topic_dist

    raw = str(district or "").strip()
    if tr_lower(raw) in alias_map:
        return alias_map[tr_lower(raw)]

    hedef_ilce = str((settings or {}).get("hedefIlce") or "").strip()
    if tr_lower(hedef_ilce) in alias_map:
        return alias_map[tr_lower(hedef_ilce)]

    if tr_lower(raw) in ("adana geneli", "adana"):
        return "Adana Geneli"

    idx = int((settings or {}).get("toplamUretilen", 0) or 0) % len(DISTRICTS)
    return DISTRICTS[idx]


def build_clean_title(topic: str, district: str, category: str) -> str:
    clean = str(topic or "").strip()
    # Strip old boilerplate suffixes if cleaning up an existing title
    clean = re.sub(
        r":\s*(?:Yasal Mevzuat ve Uygulama Rehberi|Uygulama ve Hizmet Rehberi|Hizmeti ve Fiyat Rehberi|KMK Uygulama Rehberi|Adana Yönetim Rehberi)\s*$",
        "",
        clean,
        flags=re.IGNORECASE,
    ).strip()

    # Fix duplicated city/prefix artifacts iteratively
    for _ in range(3):
        clean = re.sub(r"^(?:Adana\s+Geneli\s+Genelinde|Adana\s+Genelinde|Adana\s+Adana)\s+", "", clean, flags=re.IGNORECASE).strip()
        clean = re.sub(r"^(?:Adana\s+)?(?:Çukurova|Seyhan|Sarıçam|Yüreğir)(?:\s+Genelinde)?(?:\s*[:\-]\s*|\s+)", "", clean, flags=re.IGNORECASE).strip()
        clean = re.sub(r"^Adana\s+", "", clean, flags=re.IGNORECASE).strip()

    clean = tr_cap_first(clean) if clean else tr_cap_first(str(topic or "").strip())

    if district in ("", "auto", "Genel", "Adana", "Adana Geneli"):
        prefix = "Adana Genelinde"
    else:
        prefix = f"Adana {district} Genelinde"

    # Avoid putting "Adana Genelinde" or district twice if topic already begins naturally
    if tr_lower(clean).startswith(tr_lower(prefix)):
        base_title = clean
    else:
        base_title = f"{prefix} {clean}"

    base_title = re.sub(r"\bAdana\s+Adana\b", "Adana", base_title, flags=re.IGNORECASE)
    base_title = re.sub(r"\bAdana\s+Geneli\s+Genelinde\b", "Adana Genelinde", base_title, flags=re.IGNORECASE)
    base_title = re.sub(r"\s{2,}", " ", base_title).strip()

    if ":" not in base_title and "?" not in base_title:
        suffix_map = {
            "Temizlik": "Hizmeti ve Fiyat Rehberi",
            "Hukuk & Mevzuat": "KMK Uygulama Rehberi",
            "Site Yönetimi": "Adana Yönetim Rehberi",
        }
        suffix = suffix_map.get(category, "Adana Yönetim Rehberi")
        return f"{base_title}: {suffix}"
    return base_title


def get_royalty_free_image(topic: str, category: str = "") -> str:
    t = tr_lower(f"{topic} {category}")
    seed = abs(zlib.crc32(str(topic).encode("utf-8")))

    if any(k in t for k in ["dış cephe", "dis cephe", "cam", "vinç", "vinc", "yüksek"]):
        pool = STOCK_IMAGES["dis_cephe"]
    elif any(k in t for k in ["inşaat", "insaat", "tadilat", "harç", "boya", "anahtar teslim", "sıfır daire"]):
        pool = STOCK_IMAGES["insaat_temizlik"]
    elif any(k in t for k in ["ofis", "kurumsal temizlik", "plaza", "şirket", "iş yeri", "klinik", "muayenehane", "sağlık", "dezenfeksiyon", "su deposu"]):
        pool = STOCK_IMAGES["kurumsal_temizlik"]
    elif any(k in t for k in ["merdiven", "asansör", "ortak alan temiz", "boş ev", "daire temizli", "temizlik"]):
        pool = STOCK_IMAGES["merdiven_apartman"]
    elif any(k in t for k in ["aidat", "icra", "kanun", "kmk", "hukuk", "dava", "borç", "muhasebe", "bütçe", "karar defteri", "genel kurul"]):
        pool = STOCK_IMAGES["hukuk_icra"]
    else:
        pool = STOCK_IMAGES["site_yonetimi"]

    return pool[seed % len(pool)]


def build_seo_metadata(title: str, district: str, category: str) -> tuple:
    # Keep seoTitle <= 65 chars cleanly on word boundary
    clean_t = title.split(":", 1)[0].strip() if len(title) > 55 else title
    if len(clean_t) > 55:
        clean_t = clean_t[:55].rsplit(" ", 1)[0].strip(" ,:-")
    seo_title = f"{clean_t} | Çelebi"

    loc = "Adana genelinde" if district in ("", "Adana Geneli", "Adana") else f"Adana {district} bölgesinde"
    if category == "Temizlik":
        seo_desc = f"{loc} {clean_t} hakkında SGK'lı ekip, endüstriyel hijyen standartları, süreç adımları ve şeffaf fiyat rehberi."
    elif category == "Hukuk & Mevzuat":
        seo_desc = f"{loc} {clean_t} konusunda 634 Sayılı Kat Mülkiyeti Kanunu, yasal süreler ve apartman yönetimi uygulama rehberi."
    else:
        seo_desc = f"{loc} {clean_t} hakkında şeffaf site yönetimi, mali denetim, bakım planlaması ve kurumsal çözüm rehberi."

    if len(seo_desc) > 158:
        seo_desc = seo_desc[:155].rsplit(" ", 1)[0] + "..."
    return seo_title, seo_desc


def _strip_fences_and_sanitize_html(raw_text: str) -> str:
    txt = str(raw_text or "").strip()
    # Strip markdown code blocks
    txt = re.sub(r"^```(?:html|xml)?\s*\n?", "", txt, flags=re.IGNORECASE)
    txt = re.sub(r"\n?```\s*$", "", txt)
    txt = txt.strip()
    # Convert accidental h1 tags to h2
    txt = re.sub(r"<h1(\b[^>]*)>", r"<h2\1>", txt, flags=re.IGNORECASE)
    txt = re.sub(r"</h1>", "</h2>", txt, flags=re.IGNORECASE)
    # Remove any model-hallucinated internal links block before appending our canonical one
    txt = re.sub(r'<div\s+id=["\']celebi-internal-links["\'].*?</div>', "", txt, flags=re.DOTALL | re.IGNORECASE).strip()
    return txt


def has_boilerplate(html_body: str) -> bool:
    return any(marker in (html_body or "") for marker in BOILERPLATE_MARKERS)


def validate_generated_html(html_body: str):
    if not html_body or "<p>" not in html_body:
        return False, "missing <p> tags", 0
    if has_boilerplate(html_body):
        return False, "contains forbidden boilerplate marker", 0
    h2_count = len(re.findall(r"<h2\b[^>]*>.*?</h2>", html_body, flags=re.IGNORECASE | re.DOTALL))
    if h2_count < 3:
        return False, f"only {h2_count} <h2> sections (min 3)", 0
    plain = re.sub(r"<[^>]+>", " ", html_body)
    words = len(re.findall(r"\S+", plain))
    if words < 260:
        return False, f"too short ({words} words < 260)", words
    return True, "ok", words


def build_prompts(title: str, topic: str, district: str, category: str) -> tuple:
    loc_label = "Adana ve tüm ilçelerinde (Çukurova, Seyhan, Sarıçam, Yüreğir)" if district in ("", "Adana Geneli", "Adana") else f"Adana {district} ilçesinde"

    common_rules = (
        "Sen Adana Mahfesığmaz merkezli Çelebi Yönetim ve Temizlik Hizmetleri'nin kıdemli içerik uzmanısın. "
        "KESİN FORMAT KURALLARI:\n"
        "1. Çıktıyı YALNIZCA saf HTML olarak ver. Markdown (``` veya # veya **) KESİNLİKLE kullanma.\n"
        "2. Asla <h1> etiketi kullanma. Makale açılışını 1 kısa giriş <p> paragrafı ile yap, ardından tam 4 adet özgün <h2> alt başlığı kullan.\n"
        "3. Toplam uzunluk 500–700 kelime arasında, akıcı, tekrar içermeyen ve doğrudan soruya/başlığa yanıt veren pratik bilgilerden oluşsun.\n"
        "4. En az bir bölümde <ul><li><strong>...</strong> ...</li></ul> kontrol listesi ekle.\n"
        "5. Son <h2> bölümünden hemen önce veya son bölüm içinde 'Sıkça Sorulan Sorular' alt başlığı altında 2-3 kısa <p><strong>Soru?</strong><br/>Cevap</p> ekle.\n"
        "6. Son paragrafta Çelebi Yönetim ve Temizlik ile Adana Mahfesığmaz merkez ofisi üzerinden ücretsiz keşif / teklif çağrısı yap: "
        "0 (322) 235 15 88 sabit hat ve 0 (535) 873 03 24 WhatsApp hattını ekle."
    )

    if category == "Temizlik":
        system_prompt = (
            f"{common_rules}\n"
            "KONU KISITI (TEMİZLİK): Bu yazı bir TEMİZLİK ve HİJYEN makalesidir. Yalnızca temizlik teknikleri, doğru kimyasal/makine seçimi, "
            "Adana'nın sıcak iklimi, tozu ve kireçli suyu koşulları, SGK güvenceli ve İSG belgeli ekip avantajı ile "
            "fiyatlandırmayı etkileyen kriterleri (m², kat/pencere sayısı, kirlilik düzeyi, periyot sıklığı) anlat. "
            "Bu yazıda KESİNLİKLE KMK Madde 20, aidat icra takibi, hidrofor bakımı veya yönetici genel kurul şablon cümleleri yazma."
        )
        user_prompt = (
            f"Başlık: {title}\n"
            f"Hedef Konu: {topic}\n"
            f"Bölge: {loc_label}\n"
            "Yukarıdaki başlığa birebir odaklanan, müşterinin aradığı pratik yanıtları ve fiyat/süreç kriterlerini net veren özgün HTML makale gövdesi üret."
        )
    elif category == "Hukuk & Mevzuat":
        system_prompt = (
            f"{common_rules}\n"
            "KONU KISITI (KMK & MEVZUAT): Bu yazı 634 Sayılı Kat Mülkiyeti Kanunu, yönetim kurulu kararları, işletme projesi veya aidat/icra süreçlerine odaklıdır. "
            "Adım adım yasal süreleri, noter/tebligat gerekliliklerini, kat maliklerinin hak ve sorumluluklarını somut örneklerle açıkla. "
            "Kopyala-yapıştır temizlik veya hidrofor/güneş enerjisi cümleleri ekleme (konu özellikle onlarla ilgili değilse)."
        )
        user_prompt = (
            f"Başlık: {title}\n"
            f"Hedef Konu: {topic}\n"
            f"Bölge: {loc_label}\n"
            "Adana apartman ve site yöneticilerinin karar alırken rehber edineceği, mevzuata uygun ve uygulanabilir özgün HTML makale gövdesi üret."
        )
    else:
        system_prompt = (
            f"{common_rules}\n"
            "KONU KISITI (SİTE & TESİS YÖNETİMİ): Bu yazı profesyonel site/apartman yönetimi, şeffaf bütçe-muhasebe, teknik/idari denetim ve "
            "komşuluk huzuru üzerine odaklıdır. Doğrudan başlığın konusunu işle; gereksiz klişe şablon paragraflardan kaçın."
        )
        user_prompt = (
            f"Başlık: {title}\n"
            f"Hedef Konu: {topic}\n"
            f"Bölge: {loc_label}\n"
            "Adana'daki apartman ve siteler için doğrudan uygulanabilir, güven veren ve dönüşüm odaklı özgün HTML makale gövdesi üret."
        )

    return system_prompt, user_prompt


def generate_ai_body_html(topic: str, title: str, district: str, category: str, api_key: str = "") -> tuple:
    key = api_key or OPENROUTER_KEY
    if not key:
        print("[ERR] OPENROUTER_API_KEY tanımlı değil; şablon spamı önlemek için üretim durduruldu.")
        return None, 0, ""

    sys_prompt, usr_prompt = build_prompts(title, topic, district, category)

    for model_id, extra_params in OPENROUTER_MODELS:
        payload_obj = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": usr_prompt},
            ],
            "temperature": 0.65,
            **extra_params,
        }
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(payload_obj).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://celebiyonetim.com.tr",
                "X-Title": "Celebi Yonetim Content Engine",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                raw = (data.get("choices") or [{}])[0].get("message", {}).get("content") or ""
                cleaned = _strip_fences_and_sanitize_html(raw)
                ok, reason, words = validate_generated_html(cleaned)
                if ok:
                    final_html = f"{cleaned}\n\n{INTERNAL_LINKS_HTML}"
                    used = data.get("model") or model_id
                    return final_html, words, used
                print(f"[WARN] Model {model_id} kalite kapısından geçemedi ({reason}), sonraki modele geçiliyor...")
        except urllib.error.HTTPError as e:
            err_preview = e.read().decode("utf-8", errors="replace")[:200]
            print(f"[WARN] Model {model_id} HTTP {e.code}: {err_preview}")
        except Exception as e:
            print(f"[WARN] Model {model_id} hata verdi: {e}")

    return None, 0, ""


def get_pb_token() -> str:
    url = f"{PB_URL}/api/collections/_superusers/auth-with-password"
    data = json.dumps({"identity": PB_USER, "password": PB_PASS}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())["token"]


def get_settings():
    url = f"{PB_URL}/api/collections/otomatik_yayin_ayarlari/records"
    with urllib.request.urlopen(urllib.request.Request(url), timeout=10) as r:
        res = json.loads(r.read().decode())
        if res.get("items"):
            return res["items"][0]
    return None


def update_settings(token: str, record_id: str, data: dict):
    url = f"{PB_URL}/api/collections/otomatik_yayin_ayarlari/records/{record_id}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": token},
        method="PATCH",
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())


def get_existing_slugs(token: str = "") -> set:
    slugs = set()
    try:
        hdrs = {"Authorization": token} if token else {}
        req = urllib.request.Request(f"{PB_URL}/api/collections/yazilar/records?perPage=300", headers=hdrs)
        with urllib.request.urlopen(req, timeout=10) as r:
            for it in json.loads(r.read().decode()).get("items", []):
                s = str(it.get("slug") or "").strip()
                if s:
                    slugs.add(s)
    except Exception:
        pass
    return slugs


def make_unique_slug(title: str, existing_slugs: set) -> str:
    base = slugify(title) or f"yazi-{int(time.time())}"
    if base not in existing_slugs:
        return base
    suffix = str(int(time.time()))[-4:]
    candidate = f"{base}-{suffix}"
    n = 2
    while candidate in existing_slugs:
        candidate = f"{base}-{suffix}-{n}"
        n += 1
    return candidate


def get_next_keyword(token: str = ""):
    filter_q = urllib.parse.quote("used = false")
    url = f"{PB_URL}/api/collections/seo_keywords/records?page=1&perPage=1&filter={filter_q}&sort=-priority"
    hdrs = {"Authorization": token} if token else {}
    req = urllib.request.Request(url, headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            res = json.loads(r.read().decode())
            if res.get("items"):
                return res["items"][0]
    except Exception as e:
        print(f"[WARN] Error fetching keyword: {e}")
    return None


def mark_keyword_used(token: str, kw_id: str):
    url = f"{PB_URL}/api/collections/seo_keywords/records/{kw_id}"
    data = json.dumps({"used": True, "lastGenerated": datetime.now().isoformat()}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "Authorization": token}, method="PATCH")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"[WARN] Error updating keyword: {e}")
    return None


def ensure_fresh_keywords(token: str):
    try:
        url = f"{PB_URL}/api/collections/seo_keywords/records?filter=(used=false)&perPage=10"
        req = urllib.request.Request(url, headers={"Authorization": token})
        with urllib.request.urlopen(req, timeout=5) as r:
            res = json.loads(r.read().decode())
            unused_count = res.get("totalItems", 0)
            if unused_count < 10:
                print(f"[INFO] Kullanılmamış anahtar kelime sayısı az ({unused_count}), GSC ve Adana Trend taraması başlatılıyor...")
                script_path = os.path.join(os.path.dirname(__file__), "fetch-gsc-keywords.py")
                if os.path.exists(script_path):
                    subprocess.run([sys.executable, script_path], timeout=60)
    except Exception as e:
        print(f"[WARN] Keyword check warning: {e}")


def generate_article_content(topic: str, district: str, settings: dict = None, existing_slugs: set = None):
    category, cat_color = detect_category(topic)
    chosen_district = normalize_district(district, settings=settings, topic=topic)
    title = build_clean_title(topic, chosen_district, category)

    body_html, word_count, model_used = generate_ai_body_html(topic, title, chosen_district, category)
    if not body_html:
        return None

    slug = make_unique_slug(title, existing_slugs or set())
    read_mins = max(3, round(word_count / 160))
    seo_title, seo_desc = build_seo_metadata(title, chosen_district, category)

    tr_months = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    now = datetime.now()
    tarih_str = f"{now.day} {tr_months[now.month - 1]} {now.year}"

    author_map = {
        "Temizlik": "Çelebi Kurumsal Temizlik & İSG Birimi",
        "Hukuk & Mevzuat": "Çelebi Yönetim & KMK Hukuk Servisi",
        "Site Yönetimi": "Çelebi Site & Tesis Yönetimi Ekibi",
    }

    return {
        "baslik": title,
        "slug": slug,
        "ozet": body_html,
        "kategori": category,
        "kategoriRenk": cat_color,
        "tarih": tarih_str,
        "okumaSuresi": f"{read_mins} dk okuma",
        "aktif": True,
        "seoTitle": seo_title,
        "seoDescription": seo_desc,
        "kapakGorsel": get_royalty_free_image(topic, category),
        "kaynak": author_map.get(category, "Çelebi Yönetim & Hukuk Servisi"),
        "views": 1,
        "_model_used": model_used,
        "_words": word_count,
    }


def save_article_to_pb(token: str, article_data: dict):
    payload = {k: v for k, v in article_data.items() if not k.startswith("_")}
    url = f"{PB_URL}/api/collections/yazilar/records"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": token},
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())


def write_backoff_marker():
    try:
        with open(BACKOFF_FILE, "w", encoding="utf-8") as f:
            f.write(str(time.time()))
    except Exception:
        pass


def clear_backoff_marker():
    try:
        if os.path.exists(BACKOFF_FILE):
            os.remove(BACKOFF_FILE)
    except Exception:
        pass


def run_single_publish(token: str, settings: dict, district: str = None):
    ensure_fresh_keywords(token)
    kw_item = get_next_keyword(token)
    if kw_item:
        topic = kw_item.get("keyword")
        raw_kw_district = kw_item.get("targetDistrict") or kw_item.get("district") or ""
        kw_id = kw_item.get("id")
    else:
        topic = "Kat Mülkiyeti Kanunu Apartman Aidatı Tahsilat Rehberi"
        raw_kw_district = ""
        kw_id = None

    chosen_district = normalize_district(district or raw_kw_district, settings=settings, topic=topic)
    existing_slugs = get_existing_slugs(token)

    article_data = generate_article_content(topic, chosen_district, settings=settings, existing_slugs=existing_slugs)
    if not article_data:
        write_backoff_marker()
        try:
            update_settings(
                token,
                settings["id"],
                {
                    "sonDurum": "AI geçici olarak yanıt vermedi; şablon kopyası yayınlanmadı, sonra tekrar denenecek",
                    "tetikle": False,
                },
            )
        except Exception as e:
            print(f"[WARN] Status update failed: {e}")
        print("[WARN] OpenRouter modelleri başarısız; şablon kopyası yayınlanmadan 30 dk bekleme moduna alındı.")
        return None

    clear_backoff_marker()
    model_used = article_data.get("_model_used", "")
    words = article_data.get("_words", 0)
    saved = save_article_to_pb(token, article_data)
    print(f"[SUCCESS] Published: ID={saved.get('id')}, Kat={saved.get('kategori')}, Words={words}, Model={model_used}, Title='{saved.get('baslik')}'")

    if kw_id:
        mark_keyword_used(token, kw_id)

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_total = int(settings.get("toplamUretilen", 0) or 0) + 1
    update_settings(
        token,
        settings["id"],
        {
            "sonCalisma": now_str,
            "sonBaslik": saved.get("baslik"),
            "sonDurum": f"Başarıyla yayınlandı ({model_used})",
            "toplamUretilen": new_total,
            "tetikle": False,
        },
    )

    try:
        idx_script = os.path.join(os.path.dirname(__file__), "gsc-auto-index.py")
        if os.path.exists(idx_script) and saved.get("slug"):
            subprocess.run([sys.executable, idx_script, "--new-slug", saved.get("slug")], timeout=60)
    except Exception as e:
        print(f"[WARN] Auto index hook skipped: {e}")

    return saved


def should_run(settings: dict) -> tuple:
    if not settings.get("aktif", False):
        return False, "Zamanlayıcı devre dışı (Kapalı)"

    if os.path.exists(BACKOFF_FILE):
        try:
            ts = float(open(BACKOFF_FILE, "r", encoding="utf-8").read().strip())
            rem = BACKOFF_SECONDS - (time.time() - ts)
            if rem > 0:
                return False, f"AI geçici bekleme modunda ({int(rem // 60) + 1} dk kaldı)"
        except Exception:
            pass

    last_str = settings.get("sonCalisma")
    if not last_str:
        return True, "İlk çalışma"

    try:
        last_dt = datetime.strptime(last_str, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return True, "Geçersiz son tarih"

    now = datetime.now()
    diff_sec = (now - last_dt).total_seconds()
    siklik = settings.get("siklik", "48h")

    intervals = {
        "1h": 3600,
        "3h": 10800,
        "6h": 21600,
        "12h": 43200,
        "24h": 86400,
        "daily": 86400,
        "48h": 172800,
        "72h": 259200,
    }

    req_sec = intervals.get(siklik, 172800)
    if diff_sec >= req_sec:
        return True, f"Periyot doldu ({diff_sec:.0f}s >= {req_sec}s)"

    return False, f"Bekleniyor ({int((req_sec - diff_sec) / 60)} dakika kaldı)"


def run_dry_run(settings: dict):
    can_run, reason = should_run(settings)
    print(f"[DRY-RUN] Aktif={settings.get('aktif')} | Sıklık={settings.get('siklik')} | Hedefİlçe={settings.get('hedefIlce')}")
    print(f"[DRY-RUN] Schedule check: can_run={can_run} | {reason}")
    kw_item = get_next_keyword()
    if kw_item:
        topic = kw_item.get("keyword")
        raw_dist = kw_item.get("targetDistrict") or kw_item.get("district") or ""
        cat, color = detect_category(topic)
        dist = normalize_district(raw_dist, settings=settings, topic=topic)
        title = build_clean_title(topic, dist, cat)
        slug = make_unique_slug(title, get_existing_slugs())
        print(f"[DRY-RUN] Next keyword: '{topic}' (raw_dist='{raw_dist}', prio={kw_item.get('priority')})")
        print(f"[DRY-RUN] Normalized -> District='{dist}' | Category='{cat}' ({color})")
        print(f"[DRY-RUN] Title -> '{title}'")
        print(f"[DRY-RUN] Slug  -> '{slug}'")
    else:
        print("[DRY-RUN] Kuyrukta bekleyen anahtar kelime yok.")


def main():
    args = sys.argv[1:]
    force = "--force" in args or "-f" in args
    dry_run = "--dry-run" in args

    settings = get_settings()
    if not settings:
        print("[ERR] No 'otomatik_yayin_ayarlari' record found in PocketBase.")
        return

    if dry_run:
        run_dry_run(settings)
        return

    if settings.get("tetikle", False) or force:
        print("[INFO] Manual trigger detected! Publishing article immediately...")
        token = get_pb_token()
        run_single_publish(token, settings)
        return

    can_run, reason = should_run(settings)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Schedule check: {reason}")
    if can_run:
        token = get_pb_token()
        run_single_publish(token, settings)


if __name__ == "__main__":
    main()
