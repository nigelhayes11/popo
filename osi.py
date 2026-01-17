import requests
import re

# Sabit path listesi ve kanal isimleri
CHANNELS = [
    ("/beinspor_1_tr/main.m3u8", "beIN Sports 1"),
    ("/beinspor_2_tr/main.m3u8", "beIN Sports 2"),
    ("/beinspor_3_tr/main.m3u8", "beIN Sports 3"),
    ("/beinspor_4_tr/main.m3u8", "beIN Sports 4"),
    ("/beinspor_5_tr/main.m3u8", "beIN Sports 5"),
]

# Tahmini domain listesi (güncel domain bu listeden bulunacak)
POSSIBLE_DOMAINS = [
    "https://cdcom.cfd",
    "https://cdcdn.cfd",
    "https://cdn123.cfd",
    # gerekirse yeni domain ekle
]

OUTPUT_FILE = "osi.m3u"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*"
}

def find_working_domain(channel_path):
    """Domain değişse bile çalışan domaini bul"""
    for domain in POSSIBLE_DOMAINS:
        url = domain + channel_path
        try:
            r = requests.get(url, headers=HEADERS, stream=True, timeout=5)
            if r.status_code == 200:
                return domain
        except:
            continue
    return None

def main():
    lines = ["#EXTM3U"]
    found_count = 0

    for path, name in CHANNELS:
        domain = find_working_domain(path)
        if domain:
            full_url = domain + path
            lines.append(f'#EXTINF:-1 group-title="PİKO",{name}')
            lines.append(full_url)
            found_count += 1
            print(f"✔ Kanal bulundu: {name} -> {full_url}")
        else:
            lines.append(f'#EXTINF:-1 group-title="Sports",{name} (kanal yok)')
            lines.append("# Kanal bulunamadı")
            print(f"⚠️ Kanal yok: {name}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n✅ {OUTPUT_FILE} güncellendi ({found_count} kanal)")

if __name__ == "__main__":
    main()
