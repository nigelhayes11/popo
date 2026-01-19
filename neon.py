import requests

PREFIXES = ["75d", "j5d", "k3d", "a9d"]
DOMAIN_NUM_START = 110
DOMAIN_NUM_END = 130
TLDS = ["lat", "cfd"]

PATH = "/yayinzirve.m3u8"

REFERRER = "https://monotv524.com/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)"

OUTPUT = "neon.m3u"

headers = {
    "User-Agent": USER_AGENT,
    "Referer": REFERRER
}

def find_stream():
    for num in range(DOMAIN_NUM_START, DOMAIN_NUM_END + 1):
        for prefix in PREFIXES:
            for tld in TLDS:
                url = f"https://{prefix}.zirvedesin{num}.{tld}{PATH}"
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

stream = find_stream()

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    if stream:
        f.write('#EXTINF:-1 group-title="Neon Spor",Neon Spor\n')
        f.write(f'#EXTVLCOPT:http-user-agent={USER_AGENT}\n')
        f.write(f'#EXTVLCOPT:http-referrer={REFERRER}\n')
        f.write(stream + "\n")
    else:
        f.write("# Stream bulunamadı\n")

print("🎯 neon.m3u hazır")
