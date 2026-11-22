#!/usr/bin/env python3
"""
PocketBase üzerinde 'bildirim_ayarlari' koleksiyonunu (superuser-only) kurar,
pb_hooks dosyalarını /var/www/pocketbase/pb_hooks/ içine yükler ve PocketBase'i yeniden başlatır.
"""
import json
import os
import time
import paramiko

SERVER_IP = "2.27.101.128"
USERNAME = "root"
PASSWORD = "aQsu1G72f!"

REMOTE_SETUP = r'''
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
print("[OK] PocketBase superuser auth succeeded.")

cols = req_json(f"{PB_URL}/api/collections?perPage=100", headers=auth_headers).get("items", [])
col_names = {c["name"] for c in cols}

if "bildirim_ayarlari" not in col_names:
    schema = {
        "name": "bildirim_ayarlari",
        "type": "base",
        "listRule": None,
        "viewRule": None,
        "createRule": None,
        "updateRule": None,
        "deleteRule": None,
        "fields": [
            {"name": "aktif", "type": "bool"},
            {"name": "aliciMailler", "type": "text"},
            {"name": "ntfyTopic", "type": "text"},
            {"name": "telegramBotToken", "type": "text"},
            {"name": "telegramChatId", "type": "text"},
        ],
    }
    req_json(f"{PB_URL}/api/collections", method="POST", data=schema, headers=auth_headers)
    print("[OK] Created superuser-only collection 'bildirim_ayarlari'.")
else:
    print("[OK] Collection 'bildirim_ayarlari' already exists.")

existing = req_json(f"{PB_URL}/api/collections/bildirim_ayarlari/records?perPage=5", headers=auth_headers).get("items", [])
if not existing:
    seed = {
        "aktif": True,
        "aliciMailler": "",
        "ntfyTopic": "",
        "telegramBotToken": "",
        "telegramChatId": "",
    }
    rec = req_json(f"{PB_URL}/api/collections/bildirim_ayarlari/records", method="POST", data=seed, headers=auth_headers)
    print(f"[OK] Seeded default 'bildirim_ayarlari' record: {rec.get('id')}")
else:
    print(f"[OK] Existing 'bildirim_ayarlari' record: {existing[0].get('id')}")
'''


def main():
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    hooks_dir = os.path.join(scripts_dir, "pb_hooks")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, port=22, username=USERNAME, password=PASSWORD, timeout=15)

    # 1. Create collection & seed record
    stdin, stdout, stderr = ssh.exec_command("python3 -")
    stdin.write(REMOTE_SETUP)
    stdin.channel.shutdown_write()
    print(stdout.read().decode("utf-8", errors="replace"))
    err = stderr.read().decode("utf-8", errors="replace").strip()
    rc = stdout.channel.recv_exit_status()
    if err:
        print("SETUP STDERR:", err)
    if rc != 0:
        ssh.close()
        raise SystemExit(rc)

    # 2. Upload pb_hooks/*.js to /var/www/pocketbase/pb_hooks/
    ssh.exec_command("mkdir -p /var/www/pocketbase/pb_hooks")[1].channel.recv_exit_status()
    sftp = ssh.open_sftp()
    for fname in sorted(os.listdir(hooks_dir)):
        if fname.endswith(".js"):
            local_p = os.path.join(hooks_dir, fname)
            remote_p = f"/var/www/pocketbase/pb_hooks/{fname}"
            sftp.put(local_p, remote_p)
            print(f"[OK] Uploaded {fname} -> {remote_p}")
    sftp.close()

    # 3. Restart PocketBase and verify status + error log
    _, out2, err2 = ssh.exec_command(
        "systemctl restart pocketbase && sleep 2 && systemctl is-active pocketbase && "
        "echo '=== PB ERROR LOG TAIL ===' && tail -n 15 /var/log/pocketbase.error.log 2>/dev/null || true"
    )
    print(out2.read().decode("utf-8", errors="replace"))
    e2 = err2.read().decode("utf-8", errors="replace").strip()
    if e2:
        print("RESTART STDERR:", e2)

    ssh.close()


if __name__ == "__main__":
    main()
