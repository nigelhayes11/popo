import requests

BASE = "https://zeus173.com/live/"
OUTPUT = "zeus.m3u"

KNOWN_M3U8 = {
    "bein-sports-1.m3u8": "beIN Sports 1",
    "bein-sports-2.m3u8": "beIN Sports 2",
    "bein-sports-3.m3u8": "beIN Sports 3",
    "bein-sports-4.m3u8": "beIN Sports 4",
    "bein-sports-5.m3u8": "beIN Sports 5",
    "s-sport.m3u8": "S Sport",
    "s-sport-2.m3u8": "S Sport 2",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Referer": "https://zeus173.com/",
    "Accept": "*/*",
    "Connection": "keep-alive",
}

def main():
    lines = ["#EXTM3U"]
    found = 0

    for fname, name in KNOWN_M3U8.items():
        url = BASE + fname
        try:
            r = requests.get(url, headers=HEADERS, timeout=8, stream=True)
            if r.status_code == 200:
                lines.append(f'#EXTINF:-1 group-title="Zeus",{name}')
                lines.append(url)
                found += 1
        except Exception as e:
            continue

    if found == 0:
        lines.append("# Kanal bulunamadı")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✔ zeus.m3u oluşturuldu ({found} kanal)")

if __name__ == "__main__":
    main()
