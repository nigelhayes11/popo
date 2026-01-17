import requests

# Domain aralığı (949 ve sonrası)
DOMAIN_START = 949
DOMAIN_END = 1500

# Çıktı dosyası
OUTPUT_FILE = "jst.m3u"

# Sabit kanal listesi
CHANNELS = {
    "yayinzirve": "beIN Sports 1 A",
    "yayininat": "beIN Sports 1 B",
    "yayin1": "beIN Sports 1 C",
    "yayinb2": "beIN Sports 2",
    "yayinb3": "beIN Sports 3",
    "yayinb4": "beIN Sports 4",
    "yayinb5": "beIN Sports 5",
    "yayinbm1": "beIN Sports 1 Max",
    "yayinbm2": "beIN Sports 2 Max",
    "yayinss": "S Sports 1",
    "yayinss2": "S Sports 2",
    "yayint1": "Tivibu Sports 1",
    "yayint2": "Tivibu Sports 2",
    "yayint3": "Tivibu Sports 3",
    "yayint4": "Tivibu Sports 4",
    "yayinsmarts": "Smart Sports",
    "yayinsms2": "Smart Sports 2",
    "yayineu1": "Euro Sport 1",
    "yayineu2": "Euro Sport 2",
    "yayinex1": "Tâbii 1",
    "yayinex2": "Tâbii 2",
    "yayinex3": "Tâbii 3",
    "yayinex4": "Tâbii 4",
    "yayinex5": "Tâbii 5",
    "yayinex6": "Tâbii 6",
    "yayinex7": "Tâbii 7",
    "yayinex8": "Tâbii 8"
}

def find_active_domain():
    for i in range(DOMAIN_START, DOMAIN_END):
        url = f"https://jestyayin{i}.com/"
        try:
            r = requests.head(url, timeout=5)
            if r.status_code == 200:
                print(f"✅ Aktif domain bulundu: {url}")
                return url
        except:
            continue
    return None

def create_m3u(domain):
    lines = ["#EXTM3U"]
    for path, name in CHANNELS.items():
        lines.append(f'#EXTINF:-1 group-title="Jest TV",{name}')
        lines.append(f'{domain}/{path}.m3u8')
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ {OUTPUT_FILE} başarıyla oluşturuldu ({len(CHANNELS)} kanal)")

def create_placeholder():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n# Kanal listesi şu anda kullanılamıyor\n")
    print("⚠️ Placeholder M3U dosyası oluşturuldu")

def main():
    domain = find_active_domain()
    if domain:
        create_m3u(domain)
    else:
        print("⚠️ Aktif domain bulunamadı.")
        create_placeholder()

if __name__ == "__main__":
    main()
