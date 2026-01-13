import requests
import json
import gzip
from io import BytesIO

def main():
    url = "https://core-api.kablowebtv.com/api/channels"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Referer": "https://tvheryerde.com",
        "Origin": "https://tvheryerde.com",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer XXXXX"  # token'ı buraya koy
    }

    params = {"checkip": "false"}

    try:
        print("📡 CanliTV API'den veri alınıyor...")
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()

        try:
            with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz:
                content = gz.read().decode('utf-8')
        except:
            content = response.content.decode('utf-8')

        data = json.loads(content)
        channels = data.get('Data', {}).get('AllChannels', [])

        if not channels:
            print("⚠️ KBL: Kanal yok")
            return

        with open("kbl.m3u", "w", encoding="utf-8") as f:
            f.write("\n")
            index = 1
            for ch in channels:
                name = ch.get("Name")
                hls = ch.get("StreamData", {}).get("HlsStreamUrl")
                logo = ch.get("PrimaryLogoImageUrl", "")
                cats = ch.get("Categories", [])
                group = cats[0].get("Name", "Genel") if cats else "Genel"

                if not name or not hls or group == "Bilgilendirme":
                    continue

                f.write(f'#EXTINF:-1 tvg-id="{index}" tvg-logo="{logo}" group-title="{group}",{name}\n')
                f.write(f"{hls}\n")
                index += 1

        print(f"📺 kbl.m3u dosyası oluşturuldu! ({index-1} kanal)")

    except Exception as e:
        print("⚠️ KBL Hata ama geçiliyor:", e)

if __name__ == "__main__":
    main()
