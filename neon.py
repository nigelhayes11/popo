import requests

# 🔹 Zirvedesin otomatik tarama ayarları
PREFIXES = ["75d", "j5d", "k3d", "a9d"]
DOMAIN_NUM_START = 110
DOMAIN_NUM_END = 130
TLDS = ["lat", "cfd"]

# Bu path, değişebilecek
PATHS = [
    "/yayinzirve.m3u8",
    "/yayinb2.m3u8",
    "/yayinb3.m3u8",
    "/yayinb4.m3u8",
    "/yayinb5.m3u8",
    "/yayinbm1.m3u8",
    "/yayinbm2.m3u8",
    "/yayinss.m3u8",
    "/yayinss2.m3u8",
    "/yayinex1.m3u8",
    "/yayinex2.m3u8",
    "/yayinex3.m3u8",
    "/yayinex4.m3u8",
    "/yayinex5.m3u8",
    "/yayinex6.m3u8",
    "/yayinex7.m3u8",
    "/yayinex8.m3u8",
    "/yayinsmarts.m3u8",
    "/yayinsms2.m3u8",
    "/yayint1.m3u8",
    "/yayint2.m3u8",
    "/yayint3.m3u8",
    "/yayinatv.m3u8",
]

REFERRER = "https://monotv529.com/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)"

OUTPUT = "jesttv.m3u"

headers = {
    "User-Agent": USER_AGENT,
    "Referer": REFERRER
}

def find_stream(path):
    for num in range(DOMAIN_NUM_START, DOMAIN_NUM_END + 1):
        for prefix in PREFIXES:
            for tld in TLDS:
                url = f"https://{prefix}.zirvedesin{num}.{tld}{path}"
                try:
                    r = requests.get(url, headers=headers, timeout=8)
                    if r.status_code == 200 and "#EXTM3U" in r.text:
                        print("✅ BULUNDU:", url)
                        return url
                    else:
                        print("❌", url)
                except:
                    pass
    return None

# 🔹 Zirvedesin kanallarını topluyoruz
zirvedesin_channels = []
for path in PATHS:
    stream = find_stream(path)
    if stream:
        # Kanal ismini path'ten çıkarıyoruz (örn: yayinb2 → BeIN Sport 2 gibi mantık)
        name_map = {
            "yayinzirve": "BeIN Sport 1",
            "yayinb2": "BeIN Sport 2",
            "yayinb3": "BeIN Sport 3",
            "yayinb4": "BeIN Sport 4",
            "yayinb5": "BeIN Sport 5",
            "yayinbm1": "BeIN Sport MAX 1",
            "yayinbm2": "BeIN Sport MAX 2",
            "yayinss": "S Sport 1",
            "yayinss2": "S Sport 2",
            "yayinex1": "Exxen Spor 1",
            "yayinex2": "Exxen Spor 2",
            "yayinex3": "Exxen Spor 3",
            "yayinex4": "Exxen Spor 4",
            "yayinex5": "Exxen Spor 5",
            "yayinex6": "Exxen Spor 6",
            "yayinex7": "Exxen Spor 7",
            "yayinex8": "Exxen Spor 8",
            "yayinsmarts": "Spor Smart 1",
            "yayinsms2": "Spor Smart 2",
            "yayint1": "Tivibu Spor 1",
            "yayint2": "Tivibu Spor 2",
            "yayint3": "Tivibu Spor 3",
            "yayinatv": "Atv"
        }
        for key, name in name_map.items():
            if key in path:
                channel_name = name
                break
        else:
            channel_name = "Jest TV"
        zirvedesin_channels.append((channel_name, stream))

# 🔹 Tüm kanalları M3U’ya yazıyoruz
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n\n")

    # Zirvedesin / Jest TV kanalları
    for name, url in zirvedesin_channels:
        f.write(f'#EXTINF:-1 group-title="Jest TV",{name}\n')
        f.write(f'#EXTVLCOPT:http-user-agent={USER_AGENT}\n')
        f.write(f'#EXTVLCOPT:http-referrer={REFERRER}\n')
        f.write(url + "\n\n")

 

 for c in other_channels:
        f.write(f'#EXTINF:-1 tvg-name="{c["name"]}" tvg-language="Turkish" tvg-country="TR" tvg-logo="{c["logo"]}" group-title="{c["group"]}", {c["name"]}\n')
        f.write(c["url"] + "\n\n")

print("🎯 neon.m3u hazır ve tüm kanallar eklendi")


