import requests
import re

# Siteyi kontrol edeceğimiz ana sayfa
SOURCE_SITE = "https://cdcom.cfd"
OUTPUT_FILE = "osi.m3u"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*"
}

# Kanal listesi: (CDCOM tarzı path, kanal adı)
CHANNELS = [
    ("/beinspor_1_tr/main.m3u8", "beIN Sports 1"),
    ("/beinspor_2_tr/main.m3u8", "beIN Sports 2"),
    ("/beinspor_3_tr/main.m3u8", "beIN Sports 3"),
    ("/beinspor_4_tr/main.m3u8", "beIN Sports 4"),
    ("/beinspor_5_tr/main.m3u8", "beIN Sports 5"),
]

def find_base_domain():
    """Ana domaini HTML’den bul"""
    try:
        r = requests.get(SOURCE_SITE, headers=HEADERS, timeout=10)
        html = r.text

        # HTML’de geçen ilk domaini al (örnek regex)
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
