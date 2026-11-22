#!/usr/bin/env python3
"""
Çelebi Yönetim ve Temizlik — Google Search Console & Google Analytics 4 Bağlayıcı & Raporlayıcı
Mevcut service account (vault/credentials/gsc-service-account.json) ile:
  --check       : GSC ve GA4 API bağlantı/yetki durumunu doğrular
  --report      : (Varsayılan) Son 28 gün GSC + canlı/28 gün GA4 dönüşüm ve trafik raporunu basar
  --index-now   : gsc-auto-index.py --submit-all çalıştırır (Sitemap + IndexNow + URL Inspection)
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

import jwt
import requests

ROOT_DIR = Path(__file__).resolve().parent.parent
CREDS_CANDIDATES = [
    ROOT_DIR / "vault" / "credentials" / "gsc-service-account.json",
    Path("/var/www/credentials/gsc-service-account.json"),
]
GSC_SITE = "sc-domain:celebiyonetim.com.tr"
DEFAULT_PROJECT_ID = "celebi-yonetim"
CONVERSION_EVENTS = ["generate_lead", "whatsapp_click", "phone_call_click"]


def load_service_account():
    for path in CREDS_CANDIDATES:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8")), path
    print("[HATA] Service account JSON dosyası bulunamadı:", CREDS_CANDIDATES[0])
    sys.exit(1)


def get_access_token(sa: dict, scopes: list) -> str:
    now = int(time.time())
    assertion = jwt.encode(
        {
            "iss": sa["client_email"],
            "scope": " ".join(scopes),
            "aud": sa["token_uri"],
            "iat": now,
            "exp": now + 3600,
        },
        sa["private_key"],
        algorithm="RS256",
    )
    resp = requests.post(
        sa["token_uri"],
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion,
        },
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def api_err_summary(resp: requests.Response) -> str:
    try:
        msg = resp.json().get("error", {}).get("message", "")
        return msg or resp.text[:240]
    except Exception:
        return resp.text[:240]


def normalize_tr(text: str) -> str:
    return (
        str(text or "")
        .replace("İ", "i")
        .replace("I", "ı")
        .translate(str.maketrans("çğöşıüÇĞÖŞÜ", "cgosiucgosu"))
        .lower()
    )


def gsc_query(token: str, body: dict) -> dict:
    enc_site = urllib.parse.quote(GSC_SITE, safe="")
    url = f"https://www.googleapis.com/webmasters/v3/sites/{enc_site}/searchAnalytics/query"
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=body,
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()


def check_gsc(token: str) -> tuple:
    enc_site = urllib.parse.quote(GSC_SITE, safe="")
    url = f"https://www.googleapis.com/webmasters/v3/sites/{enc_site}/sitemaps"
    try:
        resp = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=20)
        if resp.status_code == 200:
            sitemaps = resp.json().get("sitemap", [])
            return True, "BAĞLI", sitemaps
        return False, f"HTTP {resp.status_code}: {api_err_summary(resp)}", []
    except Exception as e:
        return False, f"BAĞLANTI HATASI: {e}", []


def discover_ga4_property(token: str, explicit_prop_id: str = "") -> tuple:
    if explicit_prop_id:
        pid = explicit_prop_id.replace("properties/", "").strip()
        return "OK", pid, f"properties/{pid} (manuel)", []

    try:
        resp = requests.get(
            "https://analyticsadmin.googleapis.com/v1beta/accountSummaries",
            headers={"Authorization": f"Bearer {token}"},
            timeout=20,
        )
    except Exception as e:
        return "ERR", "", str(e), []

    if resp.status_code == 403:
        msg = api_err_summary(resp)
        if "disabled" in msg.lower() or "has not been used" in msg.lower():
            return "API_DISABLED", "", msg, []
        return "NO_PERMISSION", "", msg, []

    if not resp.ok:
        return "ERR", "", f"HTTP {resp.status_code}: {api_err_summary(resp)}", []

    summaries = resp.json().get("accountSummaries", [])
    props = []
    for acc in summaries:
        for p in acc.get("propertySummaries", []):
            props.append(
                {
                    "id": p.get("property", "").replace("properties/", ""),
                    "name": p.get("displayName", ""),
                    "account": acc.get("displayName", ""),
                }
            )

    if not props:
        return "NO_ACCESS", "", "Service account henüz hiçbir GA4 mülküne eklenmemiş.", []

    # Prefer property containing Celebi/Çelebi
    for p in props:
        if "celebi" in normalize_tr(p["name"]):
            return "OK", p["id"], f"{p['name']} (properties/{p['id']})", props

    first = props[0]
    return "OK", first["id"], f"{first['name']} (properties/{first['id']})", props


def ga4_realtime_check(token: str, prop_id: str) -> tuple:
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{prop_id}:runRealtimeReport"
    try:
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"metrics": [{"name": "activeUsers"}]},
            timeout=20,
        )
    except Exception as e:
        return "ERR", None, str(e)

    if resp.status_code == 403:
        msg = api_err_summary(resp)
        if "disabled" in msg.lower() or "has not been used" in msg.lower():
            return "DATA_API_DISABLED", None, msg
        return "NO_ACCESS", None, msg

    if not resp.ok:
        return "ERR", None, f"HTTP {resp.status_code}: {api_err_summary(resp)}"

    rows = resp.json().get("rows", [])
    active = int(rows[0]["metricValues"][0]["value"]) if rows else 0
    return "OK", active, "BAĞLI"


def ga4_run_report(token: str, prop_id: str, payload: dict) -> dict:
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{prop_id}:runReport"
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()


def print_activation_help(sa_email: str, project_id: str, gsc_ok: bool, gsc_msg: str, admin_status: str, data_status: str):
    print("\n--- Google API Etkinleştirme Adımları (Tek Seferlik ~2 dk) ---")
    needs_api = (
        admin_status == "API_DISABLED"
        or data_status == "DATA_API_DISABLED"
        or (not gsc_ok and "disabled" in gsc_msg.lower())
    )
    if needs_api:
        print(f"1. Google Cloud Console ({project_id}) projesinde kapalı API'ler için 'Enable / Etkinleştir' butonuna basın:")
        if not gsc_ok and "disabled" in gsc_msg.lower():
            print(f"   • Search Console API : https://console.developers.google.com/apis/api/searchconsole.googleapis.com/overview?project={project_id}")
        if admin_status == "API_DISABLED" or data_status == "DATA_API_DISABLED":
            print(f"   • Analytics Data API : https://console.developers.google.com/apis/api/analyticsdata.googleapis.com/overview?project={project_id}")
            print(f"   • Analytics Admin API: https://console.developers.google.com/apis/api/analyticsadmin.googleapis.com/overview?project={project_id}")
    if not gsc_ok:
        print("2. Google Search Console -> Ayarlar -> Kullanıcılar ve izinler -> Kullanıcı ekle:")
        print(f"   • E-posta: {sa_email} (Tam yetki)")
    if admin_status in ("NO_ACCESS", "NO_PERMISSION", "API_DISABLED") or data_status == "NO_ACCESS":
        print("3. Google Analytics -> Yönetici -> Mülk erişimi yönetimi -> '+' Kullanıcı ekle:")
        print(f"   • E-posta: {sa_email} (Görüntüleyen veya Düzenleyen)")


def print_gsc_report(token: str, sitemaps: list):
    print("\n================ GOOGLE SEARCH CONSOLE (SON 28 GÜN) ================")
    for sm in sitemaps:
        contents = sm.get("contents") or []
        sub = contents[0].get("submitted", "0") if contents else "0"
        idx = contents[0].get("indexed", "0") if contents else "0"
        print(
            f"• Sitemap: {sm.get('path')} | Durum: hata={sm.get('errors', 0)}, uyarı={sm.get('warnings', 0)} | "
            f"Gönderilen={sub}, İndeksli={idx} | Son okuma={sm.get('lastDownloaded', '-')}"
        )

    end_d = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    start_d = (datetime.now() - timedelta(days=28)).strftime("%Y-%m-%d")

    tot = gsc_query(token, {"startDate": start_d, "endDate": end_d}).get("rows", [])
    if tot:
        r = tot[0]
        print(
            f"• Toplam ({start_d}..{end_d}): {int(r.get('clicks', 0))} tıklama | "
            f"{int(r.get('impressions', 0))} gösterim | "
            f"TO=%{r.get('ctr', 0)*100:.2f} | Ort. sıra={r.get('position', 0):.1f}"
        )
    else:
        print(f"• {start_d}..{end_d} aralığında henüz arama verisi birikmemiş.")

    q_rows = gsc_query(token, {"startDate": start_d, "endDate": end_d, "dimensions": ["query"], "rowLimit": 10}).get("rows", [])
    if q_rows:
        print("\nEn Çok Gösterim Alan İlk 10 Sorgu:")
        for i, row in enumerate(q_rows, 1):
            q = row["keys"][0]
            print(f"  {i:2d}. {q} (tık={int(row['clicks'])}, gör={int(row['impressions'])}, sıra={row['position']:.1f})")

    p_rows = gsc_query(token, {"startDate": start_d, "endDate": end_d, "dimensions": ["page"], "rowLimit": 10}).get("rows", [])
    if p_rows:
        print("\nEn Çok Görünürlük Alan İlk 10 Sayfa:")
        for i, row in enumerate(p_rows, 1):
            p = row["keys"][0].replace("https://celebiyonetim.com.tr", "") or "/"
            print(f"  {i:2d}. {p} (tık={int(row['clicks'])}, gör={int(row['impressions'])}, sıra={row['position']:.1f})")


def print_ga4_report(token: str, prop_id: str, prop_label: str, realtime_users: int):
    print(f"\n================ GOOGLE ANALYTICS 4: {prop_label} ================")
    print(f"• Son 30 Dakika Canlı Kullanıcı: {realtime_users}")

    for label, days in [("Son 7 Gün", "7daysAgo"), ("Son 28 Gün", "28daysAgo")]:
        rep = ga4_run_report(
            token,
            prop_id,
            {
                "dateRanges": [{"startDate": days, "endDate": "today"}],
                "metrics": [{"name": "activeUsers"}, {"name": "sessions"}, {"name": "screenPageViews"}],
            },
        )
        rows = rep.get("rows", [])
        if rows:
            vals = [int(v.get("value", 0)) for v in rows[0].get("metricValues", [])]
            print(f"• {label}: {vals[0]} aktif kullanıcı | {vals[1]} oturum | {vals[2]} sayfa görüntüleme")
        else:
            print(f"• {label}: Veri henüz oluşmadı.")

    pages_rep = ga4_run_report(
        token,
        prop_id,
        {
            "dateRanges": [{"startDate": "28daysAgo", "endDate": "today"}],
            "dimensions": [{"name": "pagePath"}],
            "metrics": [{"name": "screenPageViews"}, {"name": "activeUsers"}],
            "limit": 10,
        },
    ).get("rows", [])
    if pages_rep:
        print("\nEn Çok Ziyaret Edilen İlk 10 Sayfa (28 Gün):")
        for i, r in enumerate(pages_rep, 1):
            path = r["dimensionValues"][0]["value"]
            views = r["metricValues"][0]["value"]
            users = r["metricValues"][1]["value"]
            print(f"  {i:2d}. {path} (görüntüleme={views}, kullanıcı={users})")

    src_rep = ga4_run_report(
        token,
        prop_id,
        {
            "dateRanges": [{"startDate": "28daysAgo", "endDate": "today"}],
            "dimensions": [{"name": "sessionSourceMedium"}],
            "metrics": [{"name": "sessions"}, {"name": "activeUsers"}],
            "limit": 10,
        },
    ).get("rows", [])
    if src_rep:
        print("\nTrafik Kaynakları (28 Gün):")
        for i, r in enumerate(src_rep, 1):
            src = r["dimensionValues"][0]["value"]
            sess = r["metricValues"][0]["value"]
            users = r["metricValues"][1]["value"]
            print(f"  {i:2d}. {src} (oturum={sess}, kullanıcı={users})")

    ev_rep = ga4_run_report(
        token,
        prop_id,
        {
            "dateRanges": [{"startDate": "28daysAgo", "endDate": "today"}],
            "dimensions": [{"name": "eventName"}],
            "metrics": [{"name": "eventCount"}],
            "dimensionFilter": {
                "filter": {
                    "fieldName": "eventName",
                    "inListFilter": {"values": CONVERSION_EVENTS},
                }
            },
        },
    ).get("rows", [])
    counts = {ev: 0 for ev in CONVERSION_EVENTS}
    for r in ev_rep:
        counts[r["dimensionValues"][0]["value"]] = int(r["metricValues"][0]["value"])
    print("\nDönüşüm Olayları (Son 28 Gün):")
    for ev in CONVERSION_EVENTS:
        print(f"  • {ev}: {counts[ev]}")


def main():
    parser = argparse.ArgumentParser(description="Çelebi Google Search Console & GA4 Bağlayıcı")
    parser.add_argument("--check", action="store_true", help="Bağlantı ve yetki durumunu kontrol et")
    parser.add_argument("--report", action="store_true", help="GSC ve GA4 birleşik raporunu yazdır (varsayılan)")
    parser.add_argument("--index-now", action="store_true", help="gsc-auto-index.py --submit-all çalıştır")
    parser.add_argument("--property-id", default=os.environ.get("GA4_PROPERTY_ID", ""), help="Opsiyonel GA4 mülk ID")
    args = parser.parse_args()

    if args.index_now:
        script = ROOT_DIR / "scripts" / "gsc-auto-index.py"
        rc = subprocess.run([sys.executable, str(script), "--submit-all"], check=False).returncode
        sys.exit(rc)

    run_report = args.report or not args.check
    sa, creds_path = load_service_account()
    token = get_access_token(
        sa,
        [
            "https://www.googleapis.com/auth/webmasters.readonly",
            "https://www.googleapis.com/auth/analytics.readonly",
        ],
    )

    print(f"Servis Hesabı : {sa['client_email']} (Proje: {sa.get('project_id')})")
    print(f"Kimlik Dosyası: {creds_path}")

    gsc_ok, gsc_msg, sitemaps = check_gsc(token)
    print(f"[GSC API] {gsc_msg} ({GSC_SITE})")

    admin_status, prop_id, admin_detail, all_props = discover_ga4_property(token, args.property_id)
    data_status, rt_users, data_detail = ("SKIPPED", None, "")
    if admin_status == "OK" and prop_id:
        data_status, rt_users, data_detail = ga4_realtime_check(token, prop_id)
        print(f"[GA4 API] Mülk={admin_detail} | Durum={data_status} ({data_detail})")
        if len(all_props) > 1:
            print("  Erişilen diğer GA4 mülkleri:", ", ".join(f"{p['name']} ({p['id']})" for p in all_props))
    elif admin_status == "API_DISABLED":
        print("[GA4 API] API KAPALI (Cloud Console'da Analytics Admin/Data API etkinleştirilmemiş)")
    elif admin_status in ("NO_ACCESS", "NO_PERMISSION"):
        print(f"[GA4 API] YETKİ EKSİK ({admin_detail})")
    else:
        print(f"[GA4 API] {admin_status}: {admin_detail}")

    if not gsc_ok or admin_status != "OK" or data_status != "OK":
        project_id = sa.get("project_id") or DEFAULT_PROJECT_ID
        print_activation_help(sa["client_email"], project_id, gsc_ok, gsc_msg, admin_status, data_status)

    if run_report:
        if gsc_ok:
            print_gsc_report(token, sitemaps)
        if admin_status == "OK" and data_status == "OK" and prop_id:
            print_ga4_report(token, prop_id, admin_detail, rt_users or 0)


if __name__ == "__main__":
    main()
