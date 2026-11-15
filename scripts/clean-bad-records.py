import paramiko
import json

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('2.27.101.128', username='root', password='aQsu1G72f!')

# Get superuser token
auth_data = json.dumps({"identity": "emrggck@gmail.com", "password": "Awseqdll.12"})
stdin, stdout, stderr = client.exec_command(f'curl -s -X POST -H "Content-Type: application/json" -d \'{auth_data}\' http://127.0.0.1:8090/api/collections/_superusers/auth-with-password')
res = json.loads(stdout.read().decode())
token = res.get('token')
print("Auth token:", bool(token))

# 1. Clean bad articles in yazilar
stdin, stdout, stderr = client.exec_command('curl -s http://127.0.0.1:8090/api/collections/yazilar/records?perPage=100')
yazilar = json.loads(stdout.read().decode()).get('items', [])
for y in yazilar:
    if '@' in y.get('baslik', '') or 'emrggck' in y.get('baslik', '').lower() or '@' in y.get('slug', ''):
        print(f"Deleting bad article: {y['id']} - {y['baslik']}")
        client.exec_command(f'curl -s -X DELETE -H "Authorization: {token}" http://127.0.0.1:8090/api/collections/yazilar/records/{y["id"]}')

# 2. Clean bad keywords in seo_keywords
stdin, stdout, stderr = client.exec_command('curl -s http://127.0.0.1:8090/api/collections/seo_keywords/records?perPage=200')
keywords = json.loads(stdout.read().decode()).get('items', [])
for k in keywords:
    if '@' in k.get('keyword', '') or 'emrggck' in k.get('keyword', '').lower():
        print(f"Deleting bad keyword: {k['id']} - {k['keyword']}")
        client.exec_command(f'curl -s -X DELETE -H "Authorization: {token}" http://127.0.0.1:8090/api/collections/seo_keywords/records/{k["id"]}')

client.close()
print("Clean complete!")
