import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('2.27.101.128', 22, 'root', 'aQsu1G72f!')

_, o, _ = ssh.exec_command("curl -s 'http://127.0.0.1:8090/api/collections/yazilar/records?sort=-id'")
raw = o.read().decode()
print("RAW RESPONSE:", raw[:300])
try:
    res = json.loads(raw)
    print(f"Total articles in PB: {res.get('totalItems')}")
    if res.get('items'):
        print("Record keys:", list(res["items"][0].keys()))
    for it in res.get('items', []):
        print(f"- [ID: {it.get('id')}] {it.get('baslik')} (slug: {it.get('slug')})")
except Exception as e:
    print("JSON Parse error:", e)

ssh.close()
