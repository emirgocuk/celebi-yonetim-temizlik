#!/usr/bin/env python3
"""
Çelebi Yönetim ve Temizlik — Otomatik Statik Sayfa, Sitemap, GSC & IndexNow İndeksleyici
1. VDS üzerinde PocketBase'e yeni eklenen makaleleri statik HTML (/yazilar/<slug>/index.html) olarak üretir.
2. /var/www/celebiyonetim/html/sitemap.xml dosyasını günceller.
3. Google Search Console API ile sitemap gönderir ve öncelikli sayfaları denetler.
4. IndexNow API üzerinden Bing / Yandex / AI arama botlarına anlık bildirim yapar.
"""

import html as html_lib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timezone

import jwt
import requests

SITE_PROPERTY = "sc-domain:celebiyonetim.com.tr"
BASE_URL = "https://celebiyonetim.com.tr"
SITEMAP_URL = f"{BASE_URL}/sitemap.xml"
INDEXNOW_KEY = "7f9b2c4e8a1d6f305b4c9e2a1d8f7036"
HTML_ROOT = "/var/www/celebiyonetim/html"
PB_URL = os.environ.get("POCKETBASE_URL") or "http://127.0.0.1:8090"

CREDENTIALS_PATHS = [
    "/var/www/credentials/gsc-service-account.json",
    os.path.join(os.path.dirname(__file__), "..", "vault", "credentials", "gsc-service-account.json"),
    os.path.join("vault", "credentials", "gsc-service-account.json"),
]

CORE_STATIC_PAGES = [
    ("", "1.0"),
    ("site-yonetimi", "0.9"),
    ("site-yonetimi-fiyat-hesapla", "0.95"),
    ("temizlik", "0.9"),
    ("cukurova-site-yonetimi", "0.9"),
    ("seyhan-apartman-yonetimi", "0.9"),
    ("saricam-site-yonetimi", "0.9"),
    ("iletisim", "0.8"),
    ("yazilar", "0.9"),
    ("yasal/kvkk-aydinlatma-metni", "0.8"),
    ("yasal/gizlilik-politikasi", "0.8"),
    ("yasal/cerez-politikasi", "0.8"),
    ("yasal/kullanim-kosullari", "0.8"),
    ("yasal/hizmet-ve-teklif-kosullari", "0.8"),
]

PRIORITY_INSPECT_URLS = [
    f"{BASE_URL}/",
    f"{BASE_URL}/site-yonetimi/",
    f"{BASE_URL}/site-yonetimi-fiyat-hesapla/",
    f"{BASE_URL}/cukurova-site-yonetimi/",
    f"{BASE_URL}/seyhan-apartman-yonetimi/",
    f"{BASE_URL}/saricam-site-yonetimi/",
]


def get_credentials_path():
    for p in CREDENTIALS_PATHS:
        if os.path.exists(p):
            return p
    return None


def get_gsc_access_token(creds_path: str) -> str:
    with open(creds_path, "r", encoding="utf-8") as f:
        cred = json.load(f)
    now = int(time.time())
    payload = {
        "iss": cred["client_email"],
        "scope": "https://www.googleapis.com/auth/webmasters",
        "aud": cred["token_uri"],
        "iat": now,
        "exp": now + 3600,
    }
    assertion = jwt.encode(payload, cred["private_key"], algorithm="RS256")
    resp = requests.post(
        cred["token_uri"],
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion,
        },
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def extract_layout_fragments(index_html_path: str):
    """Extract Astro CSS stylesheet tags, Header, and Footer from built index.html."""
    with open(index_html_path, "r", encoding="utf-8") as f:
        raw = f.read()
    stylesheets = "\n  ".join(re.findall(r'<link[^>]+rel="stylesheet"[^>]*>', raw))
    header_m = re.search(r"<header\b[^>]*>.*?</header>", raw, re.DOTALL)
    footer_m = re.search(r"<footer\b[^>]*>.*?</footer>", raw, re.DOTALL)
    header_html = header_m.group(0) if header_m else ""
    footer_html = footer_m.group(0) if footer_m else ""
    return stylesheets, header_html, footer_html


def render_static_article_html(item: dict, stylesheets: str, header_html: str, footer_html: str) -> str:
    slug = str(item.get("slug", "")).strip()
    title = str(item.get("baslik") or slug)
    seo_title = str(item.get("seoTitle") or "").strip() or f"{title} | Çelebi Yönetim & Temizlik"
    raw_body = str(item.get("ozet") or "").strip()
    plain_desc = str(item.get("seoDescription") or "").strip() or re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw_body)).strip()[:175]
    category = str(item.get("kategori") or "Site Yönetimi")
    read_time = str(item.get("okumaSuresi") or "4 dk okuma")
    pub_date = str(item.get("tarih") or "Güncel")
    author = str(item.get("kaynak") or "Çelebi Hukuk & Yönetim Kurulu")
    image = str(item.get("kapakGorsel") or "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80")
    canonical = f"{BASE_URL}/yazilar/{slug}"
    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": plain_desc,
        "image": image,
        "datePublished": today_iso,
        "dateModified": today_iso,
        "author": {"@type": "Person", "name": author},
        "publisher": {
            "@type": "Organization",
            "name": "Çelebi Yönetim ve Temizlik",
            "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/assets/logo/celebi-logo.svg"},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
    }

    wa_share_text = urllib.parse.quote(f'Komşular / Yöneticiler merhaba, faydalı bir rehber paylaşmak istedim:\n"{title}"\n{canonical}?utm_source=whatsapp_share')
    wa_quote_text = urllib.parse.quote(f'Merhaba Çelebi Yönetim, "{title}" yazınızı okudum. Ücretsiz keşif ve teklif almak istiyorum.')

    e_title = html_lib.escape(title)
    e_seo_title = html_lib.escape(seo_title)
    e_desc = html_lib.escape(plain_desc)
    e_cat = html_lib.escape(category)
    e_rt = html_lib.escape(read_time)
    e_date = html_lib.escape(pub_date)
    e_author = html_lib.escape(author)
    e_img = html_lib.escape(image)

    return f"""<!doctype html>
<html lang="tr">
<head>
  <!-- Google tag (GTM-M7CC26B5) -->
  <script async src="https://www.googletagmanager.com/gtm.js?id=GTM-M7CC26B5"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
  </script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e_seo_title}</title>
  <meta name="description" content="{e_desc}" />
  <link rel="canonical" href="{canonical}" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg?v=2" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{e_seo_title}" />
  <meta property="og:description" content="{e_desc}" />
  <meta property="og:image" content="{e_img}" />
  {stylesheets}
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body class="bg-white text-slate-900 flex flex-col min-h-screen">
  {header_html}
  <div class="h-20 sm:h-24" aria-hidden="true"></div>
  <main class="flex-grow">
    <article class="pt-8 pb-16 sm:pt-14 sm:pb-24 bg-white">
      <div class="max-w-4xl mx-auto px-4 sm:px-6">
        <nav class="flex items-center gap-2 text-xs text-slate-500 mb-6" aria-label="Sayfa Yolu">
          <a href="/" class="hover:text-sky-700">Ana Sayfa</a>
          <span>/</span>
          <a href="/yazilar" class="hover:text-sky-700">Sektörel Yazılar</a>
          <span>/</span>
          <span class="text-slate-900 font-bold">{e_cat}</span>
        </nav>

        <div class="flex flex-wrap items-center gap-3 mb-4">
          <span class="px-3 py-1 rounded-full text-xs font-bold border bg-sky-50 text-sky-800 border-sky-200">{e_cat}</span>
          <span class="text-xs text-slate-400 font-medium">• {e_rt}</span>
          <span class="text-xs text-slate-400 font-medium">• {e_date}</span>
        </div>

        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-slate-900 leading-[1.15] mb-6">{e_title}</h1>

        <div class="flex flex-wrap items-center justify-between gap-4 pb-8 border-b border-slate-200">
          <div class="flex items-center gap-3.5">
            <div class="w-11 h-11 rounded-xl bg-white border border-slate-200 p-1 flex items-center justify-center shadow-sm shrink-0">
              <img src="/assets/logo/celebi-logo-mark.svg?v=2" alt="Çelebi Yönetim" width="36" height="36" class="w-full h-full object-contain" />
            </div>
            <div>
              <div class="text-sm font-bold text-slate-900">{e_author}</div>
              <div class="text-xs text-slate-500">Kat Mülkiyeti Kanunu &amp; Tesis Yönetimi Uzmanı</div>
            </div>
          </div>
          <a href="https://wa.me/?text={wa_share_text}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold text-emerald-800 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200">
            Apartman Grubunda Paylaş ↗
          </a>
        </div>

        <div class="my-8 rounded-3xl overflow-hidden shadow-xl border border-slate-200 max-h-[460px] bg-slate-100">
          <img src="{e_img}" alt="{e_title}" width="900" height="500" class="w-full h-full object-cover" loading="eager" />
        </div>

        <div class="prose prose-slate max-w-none text-slate-700 leading-relaxed space-y-5 [&>h2]:text-xl [&>h2]:sm:text-2xl [&>h2]:font-bold [&>h2]:text-slate-900 [&>h2]:pt-4 [&>p]:text-sm [&>p]:sm:text-base [&>p]:text-slate-600 [&>p]:leading-relaxed [&>ul]:list-disc [&>ul]:pl-5 [&>ul]:space-y-1.5">
          {raw_body}
        </div>

        <div class="my-8 p-6 rounded-3xl bg-gradient-to-r from-slate-900 via-slate-900 to-[#004AAD] text-white shadow-xl">
          <h2 class="text-lg sm:text-xl font-extrabold mb-1">Uzun Form Doldurmayın — Sizi 5 Dakikada Arayalım</h2>
          <p class="text-xs sm:text-sm text-slate-300 mb-4">Numaranızı bırakın, Adana yönetim uzmanımız hemen arayarak bilgi paylaşsın.</p>
          <form id="vds-quick-cb" class="flex flex-col sm:flex-row gap-2.5">
            <input type="tel" id="vds-cb-phone" required placeholder="05XX XXX XX XX" class="flex-1 px-4 py-3 text-sm font-semibold rounded-2xl bg-white text-slate-900 outline-none" />
            <button type="submit" class="px-5 py-3 rounded-2xl text-xs sm:text-sm font-extrabold text-slate-950 bg-emerald-400 hover:bg-emerald-300 cursor-pointer">Beni 5 Dakikada Arayın →</button>
          </form>
          <div id="vds-cb-msg" class="hidden mt-2 text-xs font-semibold text-emerald-200">✓ Numaranız iletildi! 5 dakika içinde dönüş yapıyoruz.</div>
          <div class="mt-4 pt-3 border-t border-white/10 flex flex-wrap gap-3 text-xs">
            <a href="tel:+903222351588" class="font-bold text-white underline">0 (322) 235 15 88</a>
            <a href="https://wa.me/905358730324?text={wa_quote_text}" target="_blank" rel="noopener noreferrer" class="font-bold text-emerald-300 underline">WhatsApp Teklif Hattı</a>
            <a href="/site-yonetimi-fiyat-hesapla" class="font-bold text-sky-300 underline">30 Sn. Maliyet Hesapla →</a>
          </div>
        </div>
      </div>
    </article>
  </main>
  {footer_html}
  <script>
    document.getElementById('vds-quick-cb')?.addEventListener('submit', function(e) {{
      e.preventDefault();
      var p = document.getElementById('vds-cb-phone').value.trim();
      if (p.replace(/[^0-9]/g, '').length < 10) return;
      fetch('/api/collections/teklif_talepleri/records', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{ fullName: 'Hızlı Geri Arama Talebi', phone: p, serviceType: 'Site & Apartman Yönetimi', buildingUnits: '-', message: {json.dumps(title)}, status: 'Yeni', channel: '5 Dk Hızlı Geri Arama', landingPage: window.location.pathname }})
      }}).catch(function(){{}});
      document.getElementById('vds-cb-msg').classList.remove('hidden');
      this.reset();
    }});
  </script>
</body>
</html>"""


def write_vds_sitemap() -> list:
    lastmod = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = []
    xml_entries = []

    for page, prio in CORE_STATIC_PAGES:
        url = f"{BASE_URL}/{page}" if page else BASE_URL
        urls.append(url)
        xml_entries.append(
            f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        )

    yazilar_dir = os.path.join(HTML_ROOT, "yazilar")
    if os.path.isdir(yazilar_dir):
        seen = set()
        for name in sorted(os.listdir(yazilar_dir)):
            if name == "oku" or name in seen:
                continue
            idx = os.path.join(yazilar_dir, name, "index.html")
            if os.path.isfile(idx):
                seen.add(name)
                url = f"{BASE_URL}/yazilar/{name}"
                urls.append(url)
                xml_entries.append(
                    f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>"
                )

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(xml_entries) + "\n</urlset>"
    sm_path = os.path.join(HTML_ROOT, "sitemap.xml")
    with open(sm_path, "w", encoding="utf-8") as f:
        f.write(xml)
    return urls


def sync_vds_static_articles(only_if_changed=False, specific_slug=None):
    """Ensure every active PocketBase article has static HTML & fresh sitemap.xml on VDS."""
    if not os.path.isdir(HTML_ROOT):
        return [], []

    index_html_path = os.path.join(HTML_ROOT, "index.html")
    if not os.path.isfile(index_html_path):
        return [], []

    try:
        r = requests.get(f"{PB_URL}/api/collections/yazilar/records?perPage=200", timeout=10)
        r.raise_for_status()
        items = r.json().get("items", [])
    except Exception as e:
        print(f"[WARN] PocketBase yazilar fetch failed: {e}")
        return [], []

    missing_items = []
    seen = set()
    for it in items:
        slug = str(it.get("slug") or "").strip()
        if not slug or slug in seen or it.get("aktif") is False:
            continue
        if not re.match(r"^[a-z0-9-]+$", slug, re.IGNORECASE):
            continue
        seen.add(slug)
        target_html = os.path.join(HTML_ROOT, "yazilar", slug, "index.html")
        if specific_slug and slug == specific_slug:
            missing_items.append(it)
        elif not os.path.isfile(target_html):
            missing_items.append(it)

    if only_if_changed and not missing_items:
        return [], []

    new_urls = []
    if missing_items:
        stylesheets, header_html, footer_html = extract_layout_fragments(index_html_path)
        for it in missing_items:
            slug = str(it["slug"]).strip()
            out_dir = os.path.join(HTML_ROOT, "yazilar", slug)
            os.makedirs(out_dir, exist_ok=True)
            out_file = os.path.join(out_dir, "index.html")
            html_str = render_static_article_html(it, stylesheets, header_html, footer_html)
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(html_str)
            new_urls.append(f"{BASE_URL}/yazilar/{slug}/")
            print(f"[SYNC+] Generated static article HTML: /yazilar/{slug}/")

    all_urls = write_vds_sitemap()
    try:
        subprocess.run(
            ["chown", "-R", "www-data:www-data", os.path.join(HTML_ROOT, "yazilar"), os.path.join(HTML_ROOT, "sitemap.xml")],
            check=False,
        )
    except Exception:
        pass

    return new_urls, all_urls


def fetch_sitemap_urls():
    if os.path.isfile(os.path.join(HTML_ROOT, "sitemap.xml")):
        with open(os.path.join(HTML_ROOT, "sitemap.xml"), "r", encoding="utf-8") as f:
            sm = f.read()
    else:
        r = requests.get(SITEMAP_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        r.raise_for_status()
        sm = r.text
    return re.findall(r"<loc>(.*?)</loc>", sm)


def submit_gsc_sitemap(token: str):
    enc_site = urllib.parse.quote(SITE_PROPERTY, safe="")
    enc_sm = urllib.parse.quote(SITEMAP_URL, safe="")
    endpoint = f"https://www.googleapis.com/webmasters/v3/sites/{enc_site}/sitemaps/{enc_sm}"
    hdrs = {"Authorization": f"Bearer {token}"}

    put_resp = requests.put(endpoint, headers=hdrs, timeout=20)
    print(f"[GSC PUT Sitemap] HTTP {put_resp.status_code}")
    put_resp.raise_for_status()

    get_resp = requests.get(endpoint, headers=hdrs, timeout=20)
    if get_resp.ok:
        info = get_resp.json()
        print(
            f"[GSC Sitemap Info] lastSubmitted={info.get('lastSubmitted')} "
            f"lastDownloaded={info.get('lastDownloaded')} contents={info.get('contents')}"
        )


def submit_indexnow(urls: list):
    if not urls:
        return
    clean_urls = [u if u.endswith("/") or "." in u.rsplit("/", 1)[-1] else f"{u}/" for u in urls][:100]
    payload = {
        "host": "celebiyonetim.com.tr",
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": clean_urls,
    }
    try:
        resp = requests.post(
            "https://api.indexnow.org/indexnow",
            json=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=20,
        )
        print(f"[IndexNow] HTTP {resp.status_code} (pushed {len(clean_urls)} URLs)")
    except Exception as e:
        print(f"[IndexNow WARN] {e}")


def inspect_priority_urls(token: str):
    hdrs = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    endpoint = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
    print("[GSC URL Inspection]")
    for u in PRIORITY_INSPECT_URLS:
        try:
            r = requests.post(endpoint, headers=hdrs, json={"inspectionUrl": u, "siteUrl": SITE_PROPERTY}, timeout=20)
            if r.ok:
                idx = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
                print(f"  - {u} -> verdict={idx.get('verdict')} | coverage={idx.get('coverageState')} | lastCrawl={idx.get('lastCrawlTime', 'Henüz taranmadı')}")
            else:
                print(f"  - {u} -> HTTP {r.status_code}")
        except Exception as e:
            print(f"  - {u} -> ERR {e}")


def main():
    args = sys.argv[1:]
    sync_if_changed = "--sync-if-changed" in args
    submit_all = "--submit-all" in args
    inspect_flag = "--inspect" in args or submit_all
    specific_slug = None
    if "--new-slug" in args:
        idx = args.index("--new-slug")
        if idx + 1 < len(args):
            specific_slug = args[idx + 1]

    if sync_if_changed:
        new_urls, _ = sync_vds_static_articles(only_if_changed=True)
        if not new_urls:
            # Silent no-op when no new articles appeared
            return
        target_urls = new_urls
    elif specific_slug:
        new_urls, all_urls = sync_vds_static_articles(only_if_changed=False, specific_slug=specific_slug)
        target_urls = new_urls or [f"{BASE_URL}/yazilar/{specific_slug}/"]
    else:
        _, all_urls = sync_vds_static_articles(only_if_changed=False)
        target_urls = all_urls or fetch_sitemap_urls()

    creds_path = get_credentials_path()
    if not creds_path:
        print("[ERR] GSC kimlik dosyası bulunamadı.")
        sys.exit(1)

    token = get_gsc_access_token(creds_path)
    submit_gsc_sitemap(token)
    submit_indexnow(target_urls)

    if inspect_flag:
        inspect_priority_urls(token)


if __name__ == "__main__":
    main()
