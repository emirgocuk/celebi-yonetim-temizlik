#!/usr/bin/env python3
"""
Çelebi Yönetim ve Temizlik — Tek Seferlik Veritabanı Temizliği & Özgün İçerik Yenileme
1. otomatik_yayin_ayarlari kaydını sağlıklı '48h' temposuna günceller.
2. Mükerrer / aynı konulu 5 kopya yazıyı PocketBase 'yazilar' koleksiyonundan siler.
3. Kalan 23 benzersiz yazıdan eski sabit şablona düşenlerin başlık, kategori, SEO meta ve HTML gövdesini
   timer-runner.py içindeki çoklu OpenRouter zinciri ile %100 özgün içerikle günceller.
"""

import hashlib
import importlib.util
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TIMER_PATH = os.path.join(SCRIPT_DIR, "timer-runner.py")

spec = importlib.util.spec_from_file_location("timer_runner", TIMER_PATH)
tr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tr)

PB_URL = tr.PB_URL
SETTINGS_ID = "31zfhnoi2ecarkf"

DUPLICATE_RECORD_IDS = [
    "tfd32epstiaowiz",  # duplicate of bwp60maohdjef11
    "93gym74x37u7mfi",  # duplicate of 3y5dnx4zl6gei7p
    "qf1e66d8u5n0rje",  # duplicate of tu0ekk369a6wunt
    "lw057qhi3y18zsv",  # duplicate of fhfdgy4ehd0ozan
    "445fbntqsg40a1b",  # topic duplicate of 513dsu8hqzbi04c (had wrong Yasal Mevzuat / Site Yönetimi)
]


def pb_request(method: str, path: str, token: str = "", payload: dict = None):
    url = f"{PB_URL}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = token
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else {}


def clean_topic_from_record(baslik: str) -> tuple:
    title = str(baslik or "").strip()
    inferred_dist = tr.detect_district_from_text(title)
    if tr.tr_lower(title).startswith("adana genelinde") and not inferred_dist:
        inferred_dist = "Adana Geneli"
    elif not inferred_dist:
        inferred_dist = "Çukurova"

    topic = re.sub(
        r":\s*(?:Yasal Mevzuat ve Uygulama Rehberi|Uygulama ve Hizmet Rehberi|Hizmeti ve Fiyat Rehberi|KMK Uygulama Rehberi|Adana Yönetim Rehberi)\s*$",
        "",
        title,
        flags=re.IGNORECASE,
    ).strip()
    return topic, inferred_dist


def generate_with_backoff(topic: str, title: str, district: str, category: str) -> tuple:
    for attempt in range(1, 5):
        body_html, word_count, model_used = tr.generate_ai_body_html(topic, title, district, category)
        if body_html:
            return body_html, word_count, model_used
        wait_s = 12 * attempt
        print(f"  [RETRY {attempt}/4] Tüm modeller meşgul; {wait_s} sn bekleniyor...")
        time.sleep(wait_s)
    return None, 0, ""


def main():
    force = "--force" in sys.argv
    token = tr.get_pb_token()

    # 1. Update schedule to 48h FIRST so cron cannot fire mid-run
    try:
        tr.update_settings(token, SETTINGS_ID, {"siklik": "48h", "aktif": True, "hedefIlce": "auto"})
        print(f"[OK] otomatik_yayin_ayarlari ({SETTINGS_ID}) -> siklik='48h', aktif=True, hedefIlce='auto'")
    except Exception as e:
        print(f"[ERR] otomatik_yayin_ayarlari güncellenemedi: {e}")
        sys.exit(1)

    # 2. Delete 5 duplicate records if present
    deleted = 0
    for rec_id in DUPLICATE_RECORD_IDS:
        try:
            pb_request("DELETE", f"/api/collections/yazilar/records/{rec_id}", token=token)
            deleted += 1
            print(f"[DEL] Mükerrer kayıt silindi: {rec_id}")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"[SKIP] Kayıt zaten yok: {rec_id}")
            else:
                print(f"[WARN] Silme hatası ({rec_id}): HTTP {e.code}")

    # 3. Fetch remaining records and rewrite any boilerplate articles
    res = pb_request("GET", "/api/collections/yazilar/records?perPage=200", token=token)
    items = res.get("items", [])
    print(f"\n[*] Kalan toplam kayıt: {len(items)} (silinen mükerrer: {deleted})")

    updated_count = 0
    skipped_count = 0
    failed_ids = []

    for idx, item in enumerate(items, 1):
        rec_id = item["id"]
        old_title = str(item.get("baslik") or "")
        old_body = str(item.get("ozet") or "")
        slug = str(item.get("slug") or "")
        needs_rewrite = force or tr.has_boilerplate(old_body) or len(re.findall(r"\S+", re.sub(r"<[^>]+>", " ", old_body))) < 220

        if not needs_rewrite:
            skipped_count += 1
            print(f"[{idx}/{len(items)}] SKIP (zaten özgün): {slug}")
            continue

        topic, district = clean_topic_from_record(old_title)
        category, cat_color = tr.detect_category(topic)
        clean_title = tr.build_clean_title(topic, district, category)
        seo_title, seo_desc = tr.build_seo_metadata(clean_title, district, category)
        cover_img = tr.get_royalty_free_image(topic, category)

        print(f"[{idx}/{len(items)}] Üretiliyor ({category} / {district}): {clean_title}")
        body_html, words, model_used = generate_with_backoff(topic, clean_title, district, category)
        if not body_html:
            print(f"  [FAIL] {rec_id} için özgün içerik üretilemedi!")
            failed_ids.append(rec_id)
            continue

        read_mins = max(3, round(words / 160))
        author_map = {
            "Temizlik": "Çelebi Kurumsal Temizlik & İSG Birimi",
            "Hukuk & Mevzuat": "Çelebi Yönetim & KMK Hukuk Servisi",
            "Site Yönetimi": "Çelebi Site & Tesis Yönetimi Ekibi",
        }
        patch_payload = {
            "baslik": clean_title,
            "ozet": body_html,
            "kategori": category,
            "kategoriRenk": cat_color,
            "okumaSuresi": f"{read_mins} dk okuma",
            "seoTitle": seo_title,
            "seoDescription": seo_desc,
            "kapakGorsel": cover_img,
            "kaynak": author_map.get(category, "Çelebi Yönetim & Hukuk Servisi"),
        }
        pb_request("PATCH", f"/api/collections/yazilar/records/{rec_id}", token=token, payload=patch_payload)
        updated_count += 1
        print(f"  [PATCH OK] {rec_id} | {words} kelime | model={model_used}")
        time.sleep(2)

    # 4. Final verification summary from PocketBase
    final_res = pb_request("GET", "/api/collections/yazilar/records?perPage=200", token=token)
    final_items = final_res.get("items", [])
    cfg_res = pb_request("GET", f"/api/collections/otomatik_yayin_ayarlari/records/{SETTINGS_ID}", token=token)

    slugs = [i.get("slug") for i in final_items]
    dup_slugs = {k: v for k, v in Counter(slugs).items() if v > 1}
    boilerplate_left = sum(1 for i in final_items if tr.has_boilerplate(i.get("ozet", "")))
    hashes = set(hashlib.md5((i.get("ozet") or "").encode("utf-8")).hexdigest()[:10] for i in final_items)
    cat_dist = dict(Counter(i.get("kategori") or "" for i in final_items))
    bad_titles = [i.get("baslik") for i in final_items if "Adana Adana" in (i.get("baslik") or "") or "Adana Geneli Genelinde" in (i.get("baslik") or "")]

    print("\n=== DOĞRULAMA ÖZETİ ===")
    print(f"Güncellenen: {updated_count} | Atlanan: {skipped_count} | Başarısız: {len(failed_ids)}")
    if failed_ids:
        print("Başarısız ID'ler:", failed_ids)
    print(f"Toplam kayıt: {len(final_items)} | Benzersiz slug: {len(set(slugs))} | Mükerrer slug: {len(dup_slugs)}")
    print(f"Eski şablon kalan: {boilerplate_left}/{len(final_items)} | Benzersiz gövde hash: {len(hashes)}/{len(final_items)}")
    print(f"Kategori dağılımı: {cat_dist}")
    print(f"Hatalı çift başlık sayısı: {len(bad_titles)}")
    print(f"Zamanlayıcı siklik: {cfg_res.get('siklik')} | aktif: {cfg_res.get('aktif')} | hedefIlce: {cfg_res.get('hedefIlce')}")

    if failed_ids:
        sys.exit(2)


if __name__ == "__main__":
    main()
