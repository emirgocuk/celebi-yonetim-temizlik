#!/usr/bin/env python3
"""
Çelebi Yönetim ve Temizlik — GA4 Dönüşüm, Özel Boyut ve Yeniden Pazarlama Kitle Kurulumu
Hedef mülk: properties/565409453 (Çelebi Yönetim ve Temizlik)
"""

import importlib.util
import sys
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
REPORT_SCRIPT = SCRIPT_DIR / "google-analytics-gsc-report.py"

spec = importlib.util.spec_from_file_location("gsc_ga4_report", str(REPORT_SCRIPT))
report_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report_mod)

PROPERTY = "properties/565409453"
TARGET_KEY_EVENTS = {"generate_lead", "whatsapp_click", "phone_call_click"}

CUSTOM_DIMENSIONS = [
    {
        "parameterName": "service_type",
        "displayName": "Hizmet Türü",
        "description": "Ziyaretçinin ilgilendiği site yönetimi veya temizlik hizmeti",
        "scope": "EVENT",
    },
    {
        "parameterName": "method",
        "displayName": "Dönüşüm Yöntemi",
        "description": "Hızlı geri arama, teklif formu, WhatsApp veya telefon tıklaması",
        "scope": "EVENT",
    },
    {
        "parameterName": "landing_page",
        "displayName": "Giriş Sayfası",
        "description": "Kullanıcının siteye ilk giriş yaptığı sayfa yolu",
        "scope": "EVENT",
    },
]


def build_page_audience(display_name: str, description: str, page_patterns: list, location_field: str = "page_location") -> dict:
    event_or_exprs = [
        {
            "eventFilter": {
                "eventName": "page_view",
                "eventParameterFilterExpression": {
                    "andGroup": {
                        "filterExpressions": [
                            {
                                "orGroup": {
                                    "filterExpressions": [
                                        {
                                            "dimensionOrMetricFilter": {
                                                "fieldName": location_field,
                                                "stringFilter": {
                                                    "matchType": "CONTAINS",
                                                    "value": pattern,
                                                    "caseSensitive": False,
                                                },
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
            }
        }
        for pattern in page_patterns
    ]
    return {
        "displayName": display_name,
        "description": description,
        "membershipDurationDays": 90,
        "exclusionDurationMode": "EXCLUDE_PERMANENTLY",
        "filterClauses": [
            {
                "clauseType": "INCLUDE",
                "simpleFilter": {
                    "scope": "AUDIENCE_FILTER_SCOPE_ACROSS_ALL_SESSIONS",
                    "filterExpression": {
                        "andGroup": {
                            "filterExpressions": [
                                {"orGroup": {"filterExpressions": event_or_exprs}}
                            ]
                        }
                    },
                },
            },
            {
                "clauseType": "EXCLUDE",
                "simpleFilter": {
                    "scope": "AUDIENCE_FILTER_SCOPE_ACROSS_ALL_SESSIONS",
                    "filterExpression": {
                        "andGroup": {
                            "filterExpressions": [
                                {
                                    "orGroup": {
                                        "filterExpressions": [
                                            {"eventFilter": {"eventName": "generate_lead"}}
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                },
            },
        ],
    }


AUDIENCE_DEFS = [
    (
        "Fiyat Hesaplayıp Form Bırakmayanlar",
        "Hesaplama aracına girip form bırakmayanlar (90 gün)",
        ["/site-yonetimi-fiyat-hesapla"],
    ),
    (
        "Site Yönetimi İnceleyenler (Adana)",
        "Site yönetimi ve ilçe sayfalarını gezenler (90 gün)",
        [
            "/site-yonetimi",
            "/cukurova-site-yonetimi",
            "/seyhan-apartman-yonetimi",
            "/saricam-site-yonetimi",
        ],
    ),
    (
        "Temizlik Hizmeti İnceleyenler (Adana)",
        "Temizlik sayfalarını gezip form bırakmayanlar (90 gün)",
        ["/temizlik", "temizli"],
    ),
]


def clean_key_event_values(headers: dict):
    url = f"https://analyticsadmin.googleapis.com/v1beta/{PROPERTY}/keyEvents"
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    items = resp.json().get("keyEvents", [])

    for item in items:
        ev_name = item.get("eventName")
        if ev_name not in TARGET_KEY_EVENTS:
            continue
        if "defaultValue" in item:
            patch_url = f"https://analyticsadmin.googleapis.com/v1beta/{item['name']}?updateMask=defaultValue"
            p = requests.patch(patch_url, headers=headers, json={}, timeout=20)
            p.raise_for_status()
            print(f"[OK] Temizlendi (1 USD varsayılan değer kaldırıldı): {ev_name}")
        else:
            print(f"[SKIP] Zaten temiz: {ev_name}")


def ensure_custom_dimensions(headers: dict):
    url = f"https://analyticsadmin.googleapis.com/v1beta/{PROPERTY}/customDimensions"
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    existing = {d.get("parameterName") for d in resp.json().get("customDimensions", [])}

    for dim in CUSTOM_DIMENSIONS:
        pname = dim["parameterName"]
        if pname in existing:
            print(f"[SKIP] Özel boyut zaten mevcut: {pname}")
            continue
        c = requests.post(url, headers=headers, json=dim, timeout=20)
        c.raise_for_status()
        print(f"[OK] Özel boyut oluşturuldu: {pname} ({dim['displayName']})")


def ensure_audiences(headers: dict):
    url = f"https://analyticsadmin.googleapis.com/v1alpha/{PROPERTY}/audiences"
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    existing = {a.get("displayName") for a in resp.json().get("audiences", [])}

    for name, desc, patterns in AUDIENCE_DEFS:
        if name in existing:
            print(f"[SKIP] Kitle zaten mevcut: {name}")
            continue
        payload = build_page_audience(name, desc, patterns, location_field="page_location")
        c = requests.post(url, headers=headers, json=payload, timeout=20)
        if c.status_code == 400 and "page_location" in c.text:
            payload = build_page_audience(name, desc, patterns, location_field="pageLocation")
            c = requests.post(url, headers=headers, json=payload, timeout=20)
        if not c.ok:
            print(f"[ERR] Kitle oluşturulamadı ({name}): HTTP {c.status_code} {c.text}")
            c.raise_for_status()
        print(f"[OK] Kitle oluşturuldu: {name}")


def check_google_signals(headers: dict):
    url = f"https://analyticsadmin.googleapis.com/v1alpha/{PROPERTY}/googleSignalsSettings"
    resp = requests.get(url, headers=headers, timeout=20)
    if resp.ok:
        state = resp.json().get("state", "UNKNOWN")
        print(f"[INFO] Google Signals durumu: {state}")
    else:
        print(f"[WARN] Google Signals okunamadı: HTTP {resp.status_code}")


def verify_final_state(headers: dict):
    print("\n=== GA4 DOĞRULAMA ÖZETİ ===")
    ke = requests.get(f"https://analyticsadmin.googleapis.com/v1beta/{PROPERTY}/keyEvents", headers=headers, timeout=20).json().get("keyEvents", [])
    print("Önemli Etkinlikler:")
    for item in ke:
        if item.get("eventName") in TARGET_KEY_EVENTS:
            print(f"  - {item['eventName']} | counting={item.get('countingMethod')} | defaultValue={item.get('defaultValue', 'YOK')}")

    cds = requests.get(f"https://analyticsadmin.googleapis.com/v1beta/{PROPERTY}/customDimensions", headers=headers, timeout=20).json().get("customDimensions", [])
    print(f"Özel Boyutlar ({len(cds)}):")
    for d in cds:
        print(f"  - {d.get('parameterName')} ({d.get('displayName')}) [{d.get('scope')}]")

    auds = requests.get(f"https://analyticsadmin.googleapis.com/v1alpha/{PROPERTY}/audiences", headers=headers, timeout=20).json().get("audiences", [])
    print(f"Kitleler ({len(auds)}):")
    for a in auds:
        print(f"  - {a.get('displayName')} ({a.get('membershipDurationDays')} gün)")


def main():
    sa, _ = report_mod.load_service_account()
    token = report_mod.get_access_token(sa, ["https://www.googleapis.com/auth/analytics.edit"])
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    clean_key_event_values(headers)
    ensure_custom_dimensions(headers)
    ensure_audiences(headers)
    check_google_signals(headers)
    verify_final_state(headers)


if __name__ == "__main__":
    main()
