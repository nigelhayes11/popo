import requests
import re
import time

START_URL = "https://zeustv173.com/"
OUTPUT_FILE = "zeustv173.m3u"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Mobile Safari/537.36",
    "Accept": "/",
    "Accept-Language": "tr-TR,tr;q=0.9",
    "Connection": "keep-alive",
}

def get_base_domain():
    try:
        r = requests.get(START_URL, headers=HEADERS, timeout=10)
        return r.url.rstrip("/")
    except:
        return START_URL.rstrip("/")

def get_channel_m3u8(channel_id, base_domain):
    try:
        matches_url = f"{base_domain}/matches?id={channel_id}"
        r = requests.get(matches_url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return None

        fetch_match = re.search(r'fetch\(\s*[\'"]([^\'"]+)', r.text)
        if not fetch_match:
            return None

        fetch_url = fetch_match.group(1)
        if "{id}" in fetch_url:
            fetch_url = fetch_url.replace("{id}", str(channel_id))
        elif not fetch_url.endswith(str(channel_id)):
            fetch_url = fetch_url + str(channel_id)

        h = HEADERS.copy()
        h["Referer"] = matches_url
        h["Origin"] = base_domain

        r2 = requests.get(fetch_url, headers=h, timeout=10)
        if r2.status_code != 200:
            return None

        m3u8_match = re.search(r'(https?:\/\/[^\'"]+\.m3u8)', r2.text)
        if m3u8_match:
            return m3u8_match.group(1).replace("\\", "")

        return None
    except:
        return None

def generate_channels(start=1, end=200):
    channels = []
    for i in range(start, end + 1):
        channels.append({
            "id": str(i),
            "name": f"Zeus TV {i}",
            "group": "zeus tv"
        })
    return channels

def main():
    print("🚀 zeustv173 M3U bot başlatıldı")

    base_domain = get_base_domain()
    channels = generate_channels(1, 200)
    working = []

    for i, ch in enumerate(channels, 1):
        print(f"{i:03d} | {ch['name']} kontrol ediliyor...", end=" ")
        url = get_channel_m3u8(ch["id"], base_domain)
        if url:
            print("✓")
            ch["url"] = url
            working.append(ch)
        else:
            print("✗")
        time.sleep(0.3)

    if not working:
        print("❌ Hiç çalışan kanal bulunamadı")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in working:
            f.write(
                f'#EXTINF:-1 tvg-id="{ch["id"]}" '
                f'tvg-name="{ch["name"]}" '
                f'group-title="{ch["group"]}",{ch["name"]}\n'
            )
            f.write(f'#EXTVLCOPT:http-referrer={base_domain}\n')
            f.write(f'#EXTVLCOPT:http-user-agent={HEADERS["User-Agent"]}\n')
            f.write(ch["url"] + "\n")

    print(f"\n✅ {OUTPUT_FILE} oluşturuldu ({len(working)} kanal)")

if _name_ == "_main_":
    main()
