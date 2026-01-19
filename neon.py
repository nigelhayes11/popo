import requests

DOMAIN_URL = "https://maqrizi.com/domain.php"
CHANNELS_URL = "https://maqrizi.com/channels.php"

REFERER = "https://jestyayin950.com/"
OUT_FILE = "neon.m3u"

def get_text(url):
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text.strip()

def main():
    try:
        base_domain = get_text(DOMAIN_URL).rstrip("/")
        channels_raw = get_text(CHANNELS_URL)

        # Kanal isimlerini temizle
        channels = []
        for line in channels_raw.splitlines():
            line = line.strip()
            if not line:
                continue
            # json değilse düz text kabul
            # örn: yayinzirve, mono, jesttv
            channels.append(line)

        if not channels:
            print("❌ Kanal bulunamadı")
            return

        with open(OUT_FILE, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for ch in channels:
                f.write(f'#EXTINF:-1 group-title="Neon", {ch}\n')
                f.write(f'#EXTVLCOPT:http-referrer={REFERER}\n')
                f.write(f"{base_domain}/{ch}.m3u8\n")

        print(f"✅ {OUT_FILE} üretildi | Domain: {base_domain} | Kanal: {len(channels)}")

    except Exception as e:
        print("❌ Hata:", e)

if __name__ == "__main__":
    main()
