import requests
import re

# Ana siteyi buraya yaz
SOURCE_SITE = "https://www.buzzhoy.com/"
OUTPUT_FILE = "mj.m3u"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*"
}

# Kanal listesi: (sabit path, kanal adı)
CHANNELS = [
    ("/live/bein-sports-1.m3u8", "beIN Sports 1"),
    ("/live/bein-sports-2.m3u8", "beIN Sports 2"),
    ("/live/bein-sports-3.m3u8", "beIN Sports 3"),
    ("/live/bein-sports-4.m3u8", "beIN Sports 4"),
    ("/live/bein-sports-5.m3u8", "beIN Sports 5"),
    # Yeni kanal eklemek için buraya (path, name) ekle
]

def find_base_domain():
    """Ana siteyi aç ve güncel domaini çek"""
    try:
        r = requests.get(SOURCE_SITE, headers=HEADERS, timeout=10)
        html = r.text

        # main.m3u8 geçen ilk domaini al
        match = re.search(r'https?://[^"\']+/', html)
        if match:
            domain = match.group(0).rstrip("/")
            print(f"🔗 Güncel domain bulundu: {domain}")
            return domain
    except Exception as e:
        print(f"⚠️ Domain çekme hatası: {e}")
    return None

def main():
    base_domain = find_base_domain()
    lines = ["#EXTM3U"]

    if not base_domain:
        lines.append("# Güncel domain bulunamadı")
    else:
        for path, name in CHANNELS:
            full_url = base_domain + path
            lines.append(f'#EXTINF:-1 group-title="Sports",{name}')
            lines.append(full_url)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✔ {OUTPUT_FILE} güncellendi ({len(CHANNELS)} kanal)")

if __name__ == "__main__":
    main()
