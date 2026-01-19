import requests
import re

URLS = [
    "https://monotv529.com",
    "http://monotv529.com"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

KEYWORDS = [
    "bein",
    "s sport",
    "tivibu",
    "sport"
]

def fetch_site():
    for url in URLS:
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 200:
                print(f"✅ Site alındı: {url}")
                return r.text
        except:
            pass
    return None

html = fetch_site()
if not html:
    print("❌ Siteye ulaşılamadı")
    exit(1)

# m3u8 linklerini çek
m3u8_links = re.findall(r'https?://[^\s"\']+\.m3u8', html)

channels = []
for link in m3u8_links:
    lower = link.lower()
    if any(k in lower for k in KEYWORDS):
        channels.append(link)

channels = list(dict.fromkeys(channels))  # duplicate temizle

with open("neonspor.m3u8", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for i, url in enumerate(channels, 1):
        name = f"NeonSpor {i}"
        f.write(f'#EXTINF:-1 group-title="Neon Spor",{name}\n')
        f.write("#EXTVLCOPT:http-user-agent=Mozilla/5.0\n")
        f.write("#EXTVLCOPT:http-referrer=https://monotv529.com/\n")
        f.write(url + "\n")

print(f"✅ neonspor.m3u8 üretildi ({len(channels)} kanal)")
