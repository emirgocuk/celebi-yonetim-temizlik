#!/usr/bin/env python3
"""
Creates 'teklif_talepleri' and 'reklam_ayarlari' collections in PocketBase on VDS.
Runs via SSH (Paramiko) against PocketBase at http://127.0.0.1:8090 on the server.
"""
import json
import paramiko

SERVER_IP = "2.27.101.128"
USERNAME = "root"
PASSWORD = "aQsu1G72f!"

PB_USER = "emrggck@gmail.com"
PB_PASS = "Awseqdll.12"

REMOTE_SCRIPT = r'''
import json
import urllib.request

PB_URL = "http://127.0.0.1:8090"
PB_USER = "emrggck@gmail.com"
PB_PASS = "Awseqdll.12"

def req_json(url, method="GET", data=None, headers=None):
    hdrs = {"Content-Type": "application/json"}
    if headers:
        hdrs.update(headers)
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}

auth = req_json(
    f"{PB_URL}/api/collections/_superusers/auth-with-password",
    method="POST",
    data={"identity": PB_USER, "password": PB_PASS},
)
token = auth["token"]
auth_headers = {"Authorization": token}
print("[OK] Authenticated with PocketBase.")

cols = req_json(f"{PB_URL}/api/collections?perPage=100", headers=auth_headers).get("items", [])
col_names = {c["name"] for c in cols}

def text_field(name, required=False):
    return {"name": name, "type": "text", "required": required}

if "teklif_talepleri" not in col_names:
    schema = {
        "name": "teklif_talepleri",
        "type": "base",
        "listRule": "",
        "viewRule": "",
        "createRule": "",
        "updateRule": "",
        "deleteRule": "",
        "fields": [
            text_field("fullName", required=True),
            text_field("phone", required=True),
            text_field("serviceType"),
            text_field("buildingUnits"),
            text_field("message"),
            text_field("status"),
            text_field("channel"),
            text_field("landingPage"),
            text_field("utmSource"),
            text_field("utmMedium"),
            text_field("utmCampaign"),
            text_field("utmTerm"),
            text_field("gclid"),
            text_field("fbclid"),
            text_field("referrer"),
        ],
    }
    req_json(f"{PB_URL}/api/collections", method="POST", data=schema, headers=auth_headers)
    print("[OK] Created collection 'teklif_talepleri'.")
else:
    print("[OK] Collection 'teklif_talepleri' already exists.")

if "reklam_ayarlari" not in col_names:
    schema = {
        "name": "reklam_ayarlari",
        "type": "base",
        "listRule": "",
        "viewRule": "",
        "createRule": "",
        "updateRule": "",
        "deleteRule": "",
        "fields": [
            text_field("ga4Id"),
            text_field("gadsId"),
            text_field("gadsConvLead"),
            text_field("gadsConvWhatsapp"),
            text_field("gadsConvCall"),
            text_field("metaPixelId"),
        ],
    }
    req_json(f"{PB_URL}/api/collections", method="POST", data=schema, headers=auth_headers)
    print("[OK] Created collection 'reklam_ayarlari'.")
else:
    print("[OK] Collection 'reklam_ayarlari' already exists.")

existing_cfg = req_json(f"{PB_URL}/api/collections/reklam_ayarlari/records?perPage=10", headers=auth_headers).get("items", [])
if not existing_cfg:
    seed = {
        "ga4Id": "",
        "gadsId": "",
        "gadsConvLead": "",
        "gadsConvWhatsapp": "",
        "gadsConvCall": "",
        "metaPixelId": "",
    }
    rec = req_json(f"{PB_URL}/api/collections/reklam_ayarlari/records", method="POST", data=seed, headers=auth_headers)
    print(f"[OK] Seeded default 'reklam_ayarlari' record: {rec.get('id')}")
else:
    print(f"[OK] Existing 'reklam_ayarlari' record found: {existing_cfg[0].get('id')}")

cols_after = req_json(f"{PB_URL}/api/collections?perPage=100", headers=auth_headers).get("items", [])
for c in cols_after:
    if not c["name"].startswith("_"):
        fnames = [f["name"] for f in c.get("fields", []) if f.get("name") not in ("id",)]
        print(f"  -> {c['name']}: {fnames}")
'''


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, port=22, username=USERNAME, password=PASSWORD, timeout=15)
    stdin, stdout, stderr = ssh.exec_command("python3 -", get_pty=False)
    stdin.write(REMOTE_SCRIPT)
    stdin.channel.shutdown_write()
    out = stdout.read().decode("utf-8")
    err = stderr.read().decode("utf-8")
    rc = stdout.channel.recv_exit_status()
    ssh.close()
    print(out)
    if err:
        print("STDERR:", err)
    if rc != 0:
        raise SystemExit(rc)


if __name__ == "__main__":
    main()
