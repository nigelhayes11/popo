import requests

# 🔹 Zirvedesin otomatik tarama ayarları
PREFIXES = ["75d", "j5d", "k3d", "a9d"]
DOMAIN_NUM_START = 110
DOMAIN_NUM_END = 130
TLDS = ["lat", "cfd"]

# Bu path, değişebilecek
PATHS = [
    "/yayinzirve.m3u8",
    "/yayinb2.m3u8",
    "/yayinb3.m3u8",
    "/yayinb4.m3u8",
    "/yayinb5.m3u8",
    "/yayinbm1.m3u8",
    "/yayinbm2.m3u8",
    "/yayinss.m3u8",
    "/yayinss2.m3u8",
    "/yayinex1.m3u8",
    "/yayinex2.m3u8",
    "/yayinex3.m3u8",
    "/yayinex4.m3u8",
    "/yayinex5.m3u8",
    "/yayinex6.m3u8",
    "/yayinex7.m3u8",
    "/yayinex8.m3u8",
    "/yayinsmarts.m3u8",
    "/yayinsms2.m3u8",
    "/yayint1.m3u8",
    "/yayint2.m3u8",
    "/yayint3.m3u8",
    "/yayinatv.m3u8",
]

REFERRER = "https://monotv529.com/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)"

OUTPUT = "jesttv.m3u"

headers = {
    "User-Agent": USER_AGENT,
    "Referer": REFERRER
}

def find_stream(path):
    for num in range(DOMAIN_NUM_START, DOMAIN_NUM_END + 1):
        for prefix in PREFIXES:
            for tld in TLDS:
                url = f"https://{prefix}.zirvedesin{num}.{tld}{path}"
                try:
                    r = requests.get(url, headers=headers, timeout=8)
                    if r.status_code == 200 and "#EXTM3U" in r.text:
                        print("✅ BULUNDU:", url)
                        return url
                    else:
                        print("❌", url)
                except:
                    pass
    return None

# 🔹 Zirvedesin kanallarını topluyoruz
zirvedesin_channels = []
for path in PATHS:
    stream = find_stream(path)
    if stream:
        # Kanal ismini path'ten çıkarıyoruz (örn: yayinb2 → BeIN Sport 2 gibi mantık)
        name_map = {
            "yayinzirve": "BeIN Sport 1",
            "yayinb2": "BeIN Sport 2",
            "yayinb3": "BeIN Sport 3",
            "yayinb4": "BeIN Sport 4",
            "yayinb5": "BeIN Sport 5",
            "yayinbm1": "BeIN Sport MAX 1",
            "yayinbm2": "BeIN Sport MAX 2",
            "yayinss": "S Sport 1",
            "yayinss2": "S Sport 2",
            "yayinex1": "Exxen Spor 1",
            "yayinex2": "Exxen Spor 2",
            "yayinex3": "Exxen Spor 3",
            "yayinex4": "Exxen Spor 4",
            "yayinex5": "Exxen Spor 5",
            "yayinex6": "Exxen Spor 6",
            "yayinex7": "Exxen Spor 7",
            "yayinex8": "Exxen Spor 8",
            "yayinsmarts": "Spor Smart 1",
            "yayinsms2": "Spor Smart 2",
            "yayint1": "Tivibu Spor 1",
            "yayint2": "Tivibu Spor 2",
            "yayint3": "Tivibu Spor 3",
            "yayinatv": "Atv"
        }
        for key, name in name_map.items():
            if key in path:
                channel_name = name
                break
        else:
            channel_name = "Jest TV"
        zirvedesin_channels.append((channel_name, stream))

# 🔹 Tüm kanalları M3U’ya yazıyoruz
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n\n")

    # Zirvedesin / Jest TV kanalları
    for name, url in zirvedesin_channels:
        f.write(f'#EXTINF:-1 group-title="Jest TV",{name}\n')
        f.write(f'#EXTVLCOPT:http-user-agent={USER_AGENT}\n')
        f.write(f'#EXTVLCOPT:http-referrer={REFERRER}\n')
        f.write(url + "\n\n")

    # 🔹 Diğer sabit kanallar (senin attığın full listeyi buraya ekliyoruz)
    other_channels = [
        {
            "name": "TRT 1",
            "url": "https://tv-trt1.medya.trt.com.tr/master.m3u8",
            "logo": "https://cms-rotf-api.tabii.com/r/int/w500/23846_1-0-465-262.jpeg",
            "group": "Diğerleri"
        },
        {
            "name": "TRT SPOR",
            "url": "https://tv-trtspor1.medya.trt.com.tr/master.m3u8",
            "logo": "https://cms-rotf-api.tabii.com/r/int/w500/40480_0-0-465-261.jpeg",
            "group": "Diğerleri"
        },
        {
            "name": "TRT Spor Yıldız",
            "url": "https://trt.daioncdn.net/trtspor-yildiz/master.m3u8?app=web&platform=trtspor",
            "logo": "https://cms-tabii-public-image.tabii.com/int/w500/23855_1-0-465-262.jpeg",
            "group": "Diğerleri"
        },
        {
            "name": "TV 8",
            "url": "https://tv8.daioncdn.net/tv8/tv8.m3u8?app=7ddc255a-ef47-4e81-ab14-c0e5f2949788&ce=3",
            "logo": "https://www.campaigntr.com/wp-content/uploads/2014/09/tv8-logo.png",
            "group": "Diğerleri"
        },
        {
            "name": "TV 8.5",
            "url": "https://tv8.daioncdn.net/tv8bucuk/tv8bucuk.m3u8?app=bf58ab52-4865-4c81-b223-26b41009801e&ce=3",
            "logo": "https://www.tvyayinakisi.com/wp-content/uploads/2021/01/tv8.5.jpg",
            "group": "Diğerleri"
        },
        {
            "name": "A Spor",
            "url": "https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/aspor/aspor.m3u8",
            "logo": "https://bursasporxcom.teimg.com/crop/1280x720/bursasporx-com/uploads/2024/10/imaj-aspor.jpg",
            "group": "Diğerleri"
        },
        {
            "name": "HTSpor",
            "url": "https://ciner.daioncdn.net/ht-spor/ht-spor.m3u8?app=web",
            "logo": "https://www.htspor.com/images/manifest/social-share-logo.png",
            "group": "Diğerleri"
        },
        {
            "name": "Show TV",
            "url": "https://ciner.daioncdn.net/showtv/showtv.m3u8?app=4bc856ef-4c68-4a94-bc87-37dfaaa66558&ce=3",
            "logo": "https://mo.ciner.com.tr/video/2023/06/15/ver1726038663/8E1C90B3C04F89681637C4909149450C_640x360.jpg",
            "group": "Diğerleri"
        },
    ]

    for c in other_channels:
        f.write(f'#EXTINF:-1 tvg-name="{c["name"]}" tvg-language="Turkish" tvg-country="TR" tvg-logo="{c["logo"]}" group-title="{c["group"]}", {c["name"]}\n')
        f.write(c["url"] + "\n\n")

print("🎯 jesttv.m3u hazır ve tüm kanallar eklendi")
