import requests
import json
import gzip
from io import BytesIO
from datetime import datetime

def get_canli_tv_m3u():
    url = "https://core-api.kablowebtv.com/api/channels"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://tvheryerde.com",
        "Origin": "https://tvheryerde.com",
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer TOKEN_BURAYA"
    }

    params = {
        "checkip": "false"
    }

    try:
        print("📡 KBL API çağrılıyor...")

        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()

        try:
            with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz:
                content = gz.read().decode("utf-8")
        except:
            content = response.content.decode("utf-8")

        data = json.loads(content)

        if not data.get("IsSucceeded"):
            print("❌ API başarısız")
            return False

        channels = data.get("Data", {}).get("AllChannels", [])
        if not channels:
            print("❌ Kanal listesi boş")
            return False

        print(f"✅ {len(channels)} kanal bulundu")

        with open("kbl.m3u", "w", encoding="utf-8") as f:
            # ZORUNLU M3U HEADER
            f.write("#EXTM3U\n")
            # Git diff görsün diye timestamp
            f.write(f"# Generated: {datetime.utcnow().isoformat()}Z\n")

            kanal_index = 1

            for channel in channels:
                name = channel.get("Name")
                stream_data = channel.get("StreamData", {})
                hls_url = stream_data.get("HlsStreamUrl")
                logo = channel.get("PrimaryLogoImageUrl", "")
                categories = channel.get("Categories", [])

                if not name or not hls_url:
                    continue

                group = categories[0].get("Name", "Genel") if categories else "Genel"
                if group == "Bilgilendirme":
                    continue

                f.write(
                    f'#EXTINF:-1 tvg-id="{kanal_index}" '
                    f'tvg-logo="{logo}" '
                    f'group-title="{group}",{name}\n'
                )
                f.write(f"{hls_url}\n")

                kanal_index += 1

        print("📺 kbl.m3u başarıyla güncellendi")
        return True

    except Exception as e:
        print(f"❌ KBL HATA: {e}")
        return False


if __name__ == "__main__":
    get_canli_tv_m3u()
