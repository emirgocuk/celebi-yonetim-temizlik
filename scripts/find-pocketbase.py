import urllib.request
import re

urls = ['https://pocketbase.io/docs/', 'https://pocketbase.io/']
for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            matches = [m for m in re.findall(r'href=["\']([^"\']+)["\']', html) if 'download' in m or 'pocketbase' in m or '.zip' in m]
            print(f"URL {u} matches:", matches)
    except Exception as e:
        print(f"Err {u}:", e)
