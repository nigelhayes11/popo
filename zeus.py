import requests
import re
import sys
KNOWN_CHANNELS = {
    1: "beIN Sports 1",
    2: "S Sport",
    3: "Spor Smart",
    4: "Tivibu Spor 1",
    5: "tabii Spor 1",
    6: "TRT Spor",
}
def main():
    try:
        print("🔍 Aktif Zeus domain aranıyor...")
        active_domain = None

        # zeus173.com sabit, ama www / https farkına karşı kontrol
        domains = [
            "https://zeus173.com/",
            "https://www.zeus173.com/"
        ]

        for url in domains:
            try:
                r = requests.head(url, timeout=5)
                if r.status_code == 200:
                    active_domain = url
                    print(f"✅ Aktif domain: {active_domain}")
                    break
            except:
                continue

        if not active_domain:
            print("⚠️ Zeus domain erişilemiyor")
            create_empty_m3u()
            return 0

        print("📡 Event ID alınıyor...")
        html = requests.get(active_domain, timeout=10).text
        m = re.search(r'event\.html\?id=([^"]+)', html)

        if not m:
            print("⚠️ Event ID bulunamadı")
            create_empty_m3u()
            return 0

        event_id = m.group(1)

        print("🔗 Base URL alınıyor...")
        event_html = requests.get(
            f"{active_domain}event.html?id={event_id}",
            timeout=10
        ).text

        b = re.search(r'baseurls\s*=\s*\[\s*"([^"]+)"', event_html)
        if not b:
            print("⚠️ Base URL bulunamadı")
            create_empty_m3u()
            return 0

        base_url = b.group(1)
        print(f"✅ Base URL: {base_url}")

        print("📺 Kanallar otomatik bulunuyor...")
        lines = ["#EXTM3U"]
        found = 0

        for i in range(1, 200):
            stream = f"{base_url}androstream{i}.m3u8"
            try:
                r = requests.head(stream, timeout=4)
                if r.status_code == 200:
                    found += 1
                    name = f"Zeus TV {found}"
                    lines.append(
                        f'#EXTINF:-1 tvg-id="zeus{found}" tvg-name="{name}" group-title="Zeus TV",{name}'
                    )
                    lines.append(stream)
                    print(f"✅ Kanal bulundu: {name}")
            except:
                continue

        if found == 0:
            print("⚠️ Hiç kanal bulunamadı")
            create_empty_m3u()
            return 0

        with open("zeus.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"🎉 zeus.m3u oluşturuldu ({found} kanal)")
        return 0

    except Exception as e:
        print(f"❌ Zeus hata: {e}")
        create_empty_m3u()
        return 0


def create_empty_m3u():
    with open("zeus.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n# Zeus kanalları şu anda bulunamadı\n")
    print("📝 Boş M3U yazıldı")


if __name__ == "__main__":
    sys.exit(main())
