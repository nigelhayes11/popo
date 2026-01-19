import requests

START = 110
END = 130

CHANNELS = [
    ("BeIN Sport 1", "yayinzirve.m3u8"),
    ("BeIN Sport 2", "yayinb2.m3u8"),
    ("BeIN Sport 3", "yayinb3.m3u8"),
    ("S Sport 1", "yayinss.m3u8"),
]

def find_active_domain():
    for i in range(START, END + 1):
        url = f"https://zirvedesin{i}.li/"
        try:
            r = requests.head(url, timeout=5, allow_redirects=True)
            if r.status_code < 400:
                print(f"✅ Aktif domain: {url}")
                return url
        except:
            pass
    return None

def main():
    domain = find_active_domain()

    with open("neon.m3u8", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")

        if not domain:
            print("⚠️ Aktif domain bulunamadı ama dosya üretildi")
            return

        for name, path in CHANNELS:
            f.write(
                f'#EXTINF:-1 tvg-name="{name}" group-title="Spor - Neon",{name}\n'
            )
            f.write("#EXTVLCOPT:http-user-agent=Mozilla/5.0\n")
            f.write(f"#EXTVLCOPT:http-referrer={domain}\n")
            f.write(domain + path + "\n")

    print("✅ neon.m3u8 hazır")

if __name__ == "__main__":
    main()
    
