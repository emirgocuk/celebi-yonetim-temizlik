import paramiko
import json
import re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('2.27.101.128', 22, 'root', 'aQsu1G72f!')

def clean_title(title):
    t = title
    t = re.sub(r'Adana\s+Adana\s+Geneli\s+Genelinde', 'Adana Genelinde', t, flags=re.IGNORECASE)
    t = re.sub(r'Adana\s+Geneli\s+Genelinde', 'Adana Genelinde', t, flags=re.IGNORECASE)
    t = re.sub(r'Adana\s+Çukurova\s+Genelinde\s+Adana\s+Çukurova', 'Adana Çukurova Genelinde', t, flags=re.IGNORECASE)
    t = re.sub(r'Adana\s+Seyhan\s+Genelinde\s+Adana\s+Seyhan', 'Adana Seyhan Genelinde', t, flags=re.IGNORECASE)
    t = re.sub(r'Adana\s+Genelinde\s+Adana\s+', 'Adana Genelinde ', t, flags=re.IGNORECASE)
    return t.strip()

def detect_category(title, summary=''):
    t = title.lower()
    if any(k in t for k in ['temizlik', 'merdiven', 'tadilat', 'inşaat', 'hijyen', 'ofis']):
        return 'Temizlik'
    return 'Site Yönetimi'

def clean_date(date_str):
    if not date_str:
        return '8 Kasım 2026'
    months = {
        'january': 'Ocak', 'february': 'Şubat', 'march': 'Mart', 'april': 'Nisan',
        'may': 'Mayıs', 'june': 'Haziran', 'july': 'Temmuz', 'august': 'Ağustos',
        'september': 'Eylül', 'october': 'Ekim', 'november': 'Kasım', 'december': 'Aralık'
    }
    res = date_str
    for en, tr in months.items():
        res = re.sub(en, tr, res, flags=re.IGNORECASE)
    # Remove leading zeros like 09 -> 9
    res = re.sub(r'^0(\d)', r'\1', res)
    return res

_, o, _ = ssh.exec_command('curl -s "http://127.0.0.1:8090/api/collections/yazilar/records?page=1&perPage=50"')
raw = o.read().decode()
data = json.loads(raw)

print(f"Total articles found: {len(data.get('items', []))}")
updates_count = 0

for art in data.get('items', []):
    art_id = art['id']
    old_title = art.get('baslik', '')
    new_title = clean_title(old_title)
    
    old_cat = art.get('kategori', '')
    new_cat = detect_category(new_title, art.get('ozet', ''))
    
    old_date = art.get('tarih', '')
    new_date = clean_date(old_date)
    
    changed = (old_title != new_title) or (old_cat != new_cat) or (old_date != new_date)
    if changed:
        updates_count += 1
        print(f"\n[Updating ID: {art_id}]")
        payload = {}
        if old_title != new_title:
            print(f"  Title: '{old_title}' -> '{new_title}'")
            payload['baslik'] = new_title
            payload['seoTitle'] = new_title.replace(': Yasal Mevzuat ve Uygulama Rehberi', '') + ' | Çelebi Yönetim'
        if old_cat != new_cat:
            print(f"  Cat:   '{old_cat}' -> '{new_cat}'")
            payload['kategori'] = new_cat
        if old_date != new_date:
            print(f"  Date:  '{old_date}' -> '{new_date}'")
            payload['tarih'] = new_date

        payload_json = json.dumps(payload).replace("'", "'\\''")
        cmd = f"curl -s -X PATCH 'http://127.0.0.1:8090/api/collections/yazilar/records/{art_id}' -H 'Content-Type: application/json' -d '{payload_json}'"
        _, uo, _ = ssh.exec_command(cmd)
        resp = uo.read().decode()
        if '"id"' in resp:
            print("  -> Success!")
        else:
            print("  -> Error updating:", resp[:200])

print(f"\nCompleted! Total updated articles: {updates_count}")
ssh.close()
