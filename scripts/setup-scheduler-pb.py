#!/usr/bin/env python3
"""
Creates the 'otomatik_yayin_ayarlari' collection in PocketBase on VDS.
"""
import os
import json
import urllib.request
import urllib.parse

PB_URL = "http://127.0.0.1:8090"
PB_USER = "emrggck@gmail.com"
PB_PASS = "Awseqdll.12"

def main():
    # 1. Authenticate superuser
    auth_data = json.dumps({"identity": PB_USER, "password": PB_PASS}).encode("utf-8")
    req = urllib.request.Request(
        f"{PB_URL}/api/collections/_superusers/auth-with-password",
        data=auth_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        token = json.loads(resp.read().decode())["token"]
    print("[OK] Authenticated with PocketBase.")

    # 2. Check if collection exists
    headers = {"Authorization": token, "Content-Type": "application/json"}
    req = urllib.request.Request(f"{PB_URL}/api/collections", headers=headers)
    with urllib.request.urlopen(req) as resp:
        collections = json.loads(resp.read().decode())["items"]

    col_names = [c["name"] for c in collections]
    if "otomatik_yayin_ayarlari" not in col_names:
        print("[INFO] Creating collection 'otomatik_yayin_ayarlari'...")
        schema = {
            "name": "otomatik_yayin_ayarlari",
            "type": "base",
            "listRule": "",
            "viewRule": "",
            "createRule": "",
            "updateRule": "",
            "deleteRule": "",
            "fields": [
                {"name": "aktif", "type": "bool", "required": False},
                {"name": "siklik", "type": "text", "required": False},
                {"name": "hedefIlce", "type": "text", "required": False},
                {"name": "sabahSaati", "type": "text", "required": False},
                {"name": "sonCalisma", "type": "text", "required": False},
                {"name": "sonBaslik", "type": "text", "required": False},
                {"name": "sonDurum", "type": "text", "required": False},
                {"name": "toplamUretilen", "type": "number", "required": False},
                {"name": "tetikle", "type": "bool", "required": False}
            ]
        }
        create_req = urllib.request.Request(
            f"{PB_URL}/api/collections",
            data=json.dumps(schema).encode("utf-8"),
            headers=headers
        )
        with urllib.request.urlopen(create_req) as resp:
            print("[OK] Collection 'otomatik_yayin_ayarlari' created!")
    else:
        print("[OK] Collection 'otomatik_yayin_ayarlari' already exists.")

    # 3. Create or update initial settings record
    req = urllib.request.Request(f"{PB_URL}/api/collections/otomatik_yayin_ayarlari/records", headers=headers)
    with urllib.request.urlopen(req) as resp:
        existing = json.loads(resp.read().decode())["items"]

    initial_record = {
        "aktif": True,
        "siklik": "6h",
        "hedefIlce": "auto",
        "sabahSaati": "09:30",
        "sonCalisma": "2026-11-08 16:06:00",
        "sonBaslik": "Apartman Aidatını Ödemeyen Komşuya İcra Takibi Nasıl Yapılır?",
        "sonDurum": "Başarıyla yayınlandı",
        "toplamUretilen": 1,
        "tetikle": False
    }

    if not existing:
        print("[INFO] Inserting default scheduler record...")
        ins_req = urllib.request.Request(
            f"{PB_URL}/api/collections/otomatik_yayin_ayarlari/records",
            data=json.dumps(initial_record).encode("utf-8"),
            headers=headers
        )
        with urllib.request.urlopen(ins_req) as resp:
            rec = json.loads(resp.read().decode())
            print(f"[OK] Default scheduler record created with ID: {rec['id']}")
    else:
        print(f"[OK] Existing scheduler record found: {existing[0]['id']}")

if __name__ == "__main__":
    main()

