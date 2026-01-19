import requests

REFERER = "https://jestyayin950.com/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"

headers = {
    "Referer": REFERER,
    "User-Agent": USER_AGENT,
    "Origin": REFERER.rstrip("/")
}

def bul_ve_kaydet():
    for i in range(110, 131):
        url = f"https://75d.zirvedesin{i}.lat/yayinzirve.m3u8"
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200 and "#EXTM3U" in r.text:
                print(f"✅ BULUNDU: {url}")

                with open("neon.m3u8", "w", encoding="utf-8") as f:
                    f.write(r.text)

                print("📺 neon.m3u8 oluşturuldu")
                return
            else:
                print(f"❌ {i} boş veya geçersiz")
        except Exception as e:
            print(f"⚠️ {i} hata: {e}")

    print("❌ Aktif domain bulunamadı")

if __name__ == "__main__":
    bul_ve_kaydet()
