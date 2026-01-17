import requests
import sys

# Aralık: 949'dan başlayıp denenecek
DOMAIN_START = 949
DOMAIN_END = 1500

# Kanal listesi: {m3u8 sonu: [Kanal adı, Grup]}
channel_ids = {
    "yayinzirve": ["beIN Sports 1 A", "JEST TV"],
    "yayininat":  ["beIN Sports 1 B", "JEST TV"],
    "yayin1":     ["beIN Sports 1 C", "JEST TV"],
    "yayinb2":    ["beIN Sports 2", "JEST TV"],
    "yayinb3":    ["beIN Sports 3", "JEST TV"],
    "yayinb4":    ["beIN Sports 4", "JEST TV"],
    "yayinb5":    ["beIN Sports 5", "JEST TV"],
    "yayinbm1":   ["beIN Sports 1 Max", "JEST TV"],
    "yayinbm2":   ["beIN Sports 2 Max", "JEST TV"],
    "yayinss":    ["S Sports 1", "JEST TV"],
    "yayinss2":   ["S Sports 2", "JEST TV"],
    "yayint1":    ["Tivibu Sports 1", "JEST TV"],
    "yayint2":    ["Tivibu Sports 2", "JEST TV"],
    "yayint3":    ["Tivibu Sports 3", "JEST TV"],
    "yayint4":    ["Tivibu Sports 4", "JEST TV"],
    "yayinsmarts":["Smart Sports", "JEST TV"],
    "yayinsms2":  ["Smart Sports 2", "JEST TV"],
    "yayineu1":   ["Euro Sport 1", "JEST TV"],
    "yayineu2":   ["Euro Sport 2", "JEST TV"],
    "yayinex1":   ["Tâbii 1", "JEST TV"],
    "yayinex2":   ["Tâbii 2", "JEST TV"],
    "yayinex3":   ["Tâbii 3", "JEST TV"],
    "yayinex4":   ["Tâbii 4", "JEST TV"],
    "yayinex5":   ["Tâbii 5", "JEST TV"],
    "yayinex6":   ["Tâbii 6", "JEST TV"],
    "yayinex7":   ["Tâbii 7", "JEST TV"],
    "yayinex8":   ["Tâbii 8", "JEST TV"]
}

OUTPUT_FILE = "jst.m3u"

def find_active_domain():
    for i in range(DOMAIN_START, DOMAIN_END):
        domain = f"https://jestyayin{i}.com/"
        try:
            r = requests.head(domain, timeout=5)
            if r.status_code == 200:
                print(f"✅ Aktif domain bulundu: {domain}")
                return domain
        except:
            continue
    print("⚠️  Aktif domain bulunamadı")
    return None

def create_m3u(domain):
    lines = ["#EXTM3U"]
    for cid, details in channel_ids.items():
        name, group = details
        lines.append(f'#EXTINF:-1 group-title="{group}",{name}')
        lines.append(f'{domain}{cid}.m3u8')
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ {OUTPUT_FILE} başarıyla oluşturuldu ({len(channel_ids)} kanal)")

def create_empty_m3u():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n# Kanal listesi şu anda kullanılamıyor")
    print(f"✅ Placeholder {OUTPUT_FILE} oluşturuldu")

def main():
    domain = find_active_domain()
    if domain:
        create_m3u(domain)
    else:
        create_empty_m3u()

if __name__ == "__main__":
    sys.exit(main())
