import requests
import json
import gzip
from io import BytesIO

def main():
    url = "https://core-api.kablowebtv.com/api/channels"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://tvheryerde.com",
        "Origin": "https://tvheryerde.com",
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer XXXXX"
    }

    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()

        try:
            with gzip.GzipFile(fileobj=BytesIO(r.content)) as gz:
                content = gz.read().decode("utf-8")
        except:
            content = r.text

        data = json.loads(content)
        channels = data.get("Data", {}).get("AllChannels", [])

        if not channels:
            print("⚠️ kbl: kanal yok")
            return

        with open("kbl.m3u", "w", encoding="utf-8") as f:
            f.write("\n")
            i = 1
            for ch in channels:
                name = ch.get("Name")
                hls = ch.get("StreamData", {}).get("HlsStreamUrl")
                logo = ch.get("PrimaryLogoImageUrl", "")
                cats = ch.get("Categories", [])
                group = cats[0].get("Name", "Genel") if cats else "Genel"

                if not name or not hls or group == "Bilgilendirme":
                    continue

                f.write(f'#EXTINF:-1 tvg-id="{i}" tvg-logo="{logo}" group-title="{group}",{name}\n')
                f.write(f"{hls}\n")
                i += 1

        print("✅ kbl.m3u üretildi")

    except Exception as e:
        print("⚠️ kbl hata ama geçiliyor:", e)

if _name_ == "_main_":
    main()
