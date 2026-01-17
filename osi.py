import requests

# Kanal listesi: (path, isim)
CHANNELS = [
    ("/beinspor_1_tr/main.m3u8", "beIN Sports 1"),
    ("/beinspor_2_tr/main.m3u8", "beIN Sports 2"),
    ("/beinspor_3_tr/main.m3u8", "beIN Sports 3"),
    ("/beinspor_4_tr/main.m3u8", "beIN Sports 4"),
    ("/beinspor_5_tr/main.m3u8", "beIN Sports 5"),
]

# Ön domain listesi: değişebileceğini düşündüğün domainleri ekle
POSSIBLE_DOMAINS = [
    "https://cdcom.cfd",
    "https://cdcdn.cfd",
    "https://cdcom2.cfd",
]

OUTPUT_FILE = "osi.m3u"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*"
}

def find_base_domain():
    """Çalışan domaini bul"""
    for domain in POSSIBLE_DOMAINS:
        for path, _ in CHANNELS:
            url = domain + path
            try:
                r = requests.head(url, headers=HEADERS, timeout=5)
                if r.status_code == 200:
                    print(f"🔗 Güncel domain bulundu: {domain}")
                    return domain
            except:
                continue
    print("⚠️ Hiçbir domain çalışmadı, ilk domain kullanılacak")
    return POSSIBLE_DOMAINS[0]

def main():
    base_domain = find_base_domain()
    lines = ["#EXTM3U"]
    found_count = 0

    for path, name in CHANNELS:
        full_url = base_domain + path
        try:
            r = requests.head(full_url, headers=HEADERS, timeout=5)
            if r.status_code == 200:
                lines.append(f'#EXTINF:-1 group-title="piko",{name}')
                lines.append(full_url)
                found_count += 1
                print(f"✔ Kanal bulundu: {name}")
            else:
                print(f"⚠️ Kanal yok: {name}")
        except Exception as e:
            print(f"⚠️ Hata: {name} -> {e}")

    if found_count == 0:
        lines.append("# Hiç kanal bulunamadı")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n✅ {OUTPUT_FILE} güncellendi ({found_count} kanal)")

if __name__ == "__main__":
    main()
