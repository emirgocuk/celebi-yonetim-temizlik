import urllib.request
import re
import html as html_lib
import json

req = urllib.request.Request('https://celebiyonetim.com.tr/yazilar', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

m = re.search(r'data-articles="([^"]+)"', html)
if m:
    raw = html_lib.unescape(m.group(1))
    articles = json.loads(raw)
    print("Static articles count:", len(articles))
    print("First static article:", articles[0]['date'], "-", articles[0]['title'][:60])
    print("Last static article:", articles[-1]['date'], "-", articles[-1]['title'][:60])

print("parseArticleDate in html:", "parseArticleDate" in html)
print("allArticlesList.sort in html:", "allArticlesList.sort" in html)

# Check home page
req_home = urllib.request.Request('https://celebiyonetim.com.tr', headers={'User-Agent': 'Mozilla/5.0'})
html_home = urllib.request.urlopen(req_home).read().decode('utf-8')
print("Home page parseArticleDate:", "parseArticleDate" in html_home)
