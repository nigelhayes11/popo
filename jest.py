import requests
import sys

# Son bilinen domain numarası
START_DOMAIN_NUM = 949
MAX_TRY = 20  # Kaç gün sonrası denenecek

OUTPUT_FILE = "jst.m3u"

# Kanal listesi: {cid: [Kanal Adı, Grup]}
CHANNELS = {
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

def find_active_domain(start=START_DOMAIN_NUM, max_try=MAX_TRY):
    """Active domaini otomatik bul"""
    for i in range(start, start + max_try):
        url = f"https://jestyayin{i}.com/"
        try:
            r = requests.head(url, timeout=5)
            if r.status_code == 200:
                print(f"✅ Aktif domain bulundu: {url}")
                return url
        except:
            continue
    print("⚠️ Aktif domain bulunamadı")
    return None

def create_m3u(active_domain):
    """M3U dosyasını oluştur"""
    lines = ["#EXTM3U"]
    for cid, details in CHANNELS.items():
        name = details[0]
        group = details[1]
        full_url = f"{active_domain}{cid}.m3u8"
        lines.append(f'#EXTINF:-1 group-title="{group}",{name}')
        lines.append(full_url)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✔ {OUTPUT_FILE} oluşturuldu ({len(CHANNELS)} kanal)")

def create_placeholder_m3u():
    """Placeholder M3U"""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n# Kanal listesi şu anda kullanılamıyor\n")
    print("✅ Placeholder M3U oluşturuldu")

def main():
    active_domain = find_active_domain()
    if active_domain:
        create_m3u(active_domain)
    else:
        create_placeholder_m3u()

if __name__ == "__main__":
    main()
