import requests
import json
import gzip
from io import BytesIO

def kbl_guncelle():
    url = "https://core-api.kablowebtv.com/api/channels"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://tvheryerde.com",
        "Origin": "https://tvheryerde.com",
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer XXXXX"  # Token buraya
    }
    params = {"checkip": "false"}

    try:
        print("📡 KBL API çağrılıyor...")
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()

        # Gzip kontrol
        try:
            with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz:
                content = gz.read().decode("utf-8")
        except:
            content = response.content.decode("utf-8")

        data = json.loads(content)
        channels = data.get("Data", {}).get("AllChannels", [])

        if not channels:
            print("⚠️ KBL: Kanal listesi boş, kbl.m3u oluşturulacak ama içerik yok.")

        # Dosya yaz
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

        print(f"✅ kbl.m3u güncellendi! ({index-1} kanal)")

    except requests.exceptions.RequestException as e:
        print(f"❌ KBL API Hata: {e}. kbl.m3u boş oluşturulacak.")
        with open("kbl.m3u", "w", encoding="utf-8") as f:
            f.write("\n")  # boş dosya oluştur

    except Exception as e:
        print(f"❌ KBL Beklenmeyen Hata: {e}. kbl.m3u boş oluşturulacak.")
        with open("kbl.m3u", "w", encoding="utf-8") as f:
            f.write("\n")  # boş dosya oluştur

if _name_ == "_main_":
    kbl_guncelle()
