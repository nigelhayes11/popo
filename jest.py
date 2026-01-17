import requests
import re
import sys

def main():
    try:
        # Domain aralığı (25–99)
        active_domain = None
        print("🔍 Aktif domain aranıyor...")
        
        for i in range(1204, 2000):
            url = f"https://jestyayın{i}.com/"
            try:
                r = requests.head(url, timeout=5)
                if r.status_code == 200:
                    active_domain = url
                    print(f"✅ Aktif domain bulundu: {active_domain}")
                    break
            except Exception as e:
                continue
        
        if not active_domain:
            print("⚠️  Aktif domain bulunamadı. Boş M3U dosyası oluşturuluyor...")
            create_empty_m3u()
            return 0
        
        # İlk kanal ID'si al
        print("📡 Kanal ID'si alınıyor...")
        try:
            html = requests.get(active_domain, timeout=10).text
            m = re.search(r'<iframe[^>]+id="customIframe"[^>]+src="/channel.html\?id=([^"]+)"', html)
            
            if not m:
                print("⚠️  Kanal ID bulunamadı. Boş M3U dosyası oluşturuluyor...")
                create_empty_m3u()
                return 0
            
            first_id = m.group(1)
            print(f"✅ Kanal ID bulundu: {first_id}")
            
        except Exception as e:
            print(f"⚠️  HTML alınırken hata: {str(e)}")
            create_empty_m3u()
            return 0
        
        # Base URL çek
        print("🔗 Base URL alınıyor...")
        try:
            event_source = requests.get(active_domain + "channel.html?id=" + first_id, timeout=10).text
            b = re.search(r'B_URL\s*=\s*["\']([^"\']+)["\']', event_source)
            
            if not b:
                print("⚠️  Base URL bulunamadı. Boş M3U dosyası oluşturuluyor...")
                create_empty_m3u()
                return 0
            
            base_url = b.group(1)
            print(f"✅ Base URL bulundu: {base_url}")
            
        except Exception as e:
            print(f"⚠️  Event source alınırken hata: {str(e)}")
            create_empty_m3u()
            return 0
        
        # Kanal listesi
        channel_ids = {
            "yayinzirve": ["beIN Sports 1 A", "JEST TV"],
            "yayininat":  ["beIN Sports 1 B", "JEST TV"],
            "yayin1":     ["beIN Sports 1 C️", "JEST TV"],
            "yayinb2":    ["beIN Sports 2", "JEST TV"],
            "yayinb3":    ["beIN Sports 3", "JEST TV"],
            "yayinb4":    ["beIN Sports 4", "JEST TV"],
            "yayinb5":    ["beIN Sports 5", "JEST TV"],
            "yayinbm1":   ["beIN Sports 1 Max", "JEST TV"],
            "yayinbm2":   ["beIN Sports 2 Max", "JEST TV"],
            "yayinss":    ["S Sports 1", "JEST TV"],
            "yayinss2":   ["S Sports 2", "JEST TV"],
            "yayint1":    ["Tivibu Sports 1", "JEST TV"],
            "yayint2":    ["Tivibu Sports 2", "JEST TV"],
            "yayint3":    ["Tivibu Sports 3", "JEST TV"],
            "yayint4":    ["Tivibu Sports 4", "JEST TV"],
            "yayinsmarts":["Smart Sports", "JEST TV"],
            "yayinsms2":  ["Smart Sports 2", "JEST TV"],
            "yayineu1":  ["Euro Sport 1", "JEST TV"],
            "yayineu2":  ["Euro Sport 2", "JEST TV"],
            "yayinex1":   ["Tâbii 1", "JEST TV"],
            "yayinex2":   ["Tâbii 2", "JEST TV"],
            "yayinex3":   ["Tâbii 3", "JEST TV"],
            "yayinex4":   ["Tâbii 4", "JEST TV"],
            "yayinex5":   ["Tâbii 5", "JEST TV"],
            "yayinex6":   ["Tâbii 6", "JEST TV"],
            "yayinex7":   ["Tâbii 7", "JEST TV"],
            "yayinex8":   ["Tâbii 8", "JEST TV"]
        }
        
        # M3U dosyası oluştur
        print("📝 M3U dosyası oluşturuluyor...")
        lines = ["\n"]
        for cid, details in channel_ids.items():
            name = details[0]  # Listenin ilk elemanı: Kanal Adı (Örn: beIN Sports 1 A)
            title = details[1] # Listenin ikinci elemanı: Grup (Örn: JEST TV)
            
            # EXTM3U satırını oluştur
            lines.append(f'#EXTINF:-1 group-title="JEST TV" ,{name}')
            lines.append(f'#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)')
            lines.append(f'#EXTVLCOPT:http-referrer={active_domain}')
            
            # URL satırını oluştur (Sözlük anahtarı olan 'cid' kullanılıyor)
            full_url = f"{base_url}{cid}.m3u8"
            lines.append(full_url)
        
        with open("jst.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        print(f"✅ jst.m3u başarıyla oluşturuldu ({len(channel_ids)} kanal)")
        return 0
        
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {str(e)}")
        print("⚠️  Boş M3U dosyası oluşturuluyor...")
        create_empty_m3u()
        return 0

def create_empty_m3u():
    """Hata durumunda boş/placeholder M3U dosyası oluştur"""
    try:
        with open("jst.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            f.write("# Kanal listesi şu anda kullanılamıyor\n")
        print("✅ Placeholder M3U dosyası oluşturuldu")
    except Exception as e:
        print(f"❌ M3U dosyası oluşturulamadı: {str(e)}")

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)











