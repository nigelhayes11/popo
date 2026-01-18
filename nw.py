import requests
import re
from urllib.parse import urljoin

BASE_URL = "https://streamhub.pro/"
OUTPUT = "nw.m3u"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html"
}

def get_events():
    r = requests.get(urljoin(BASE_URL, "events"), headers=HEADERS, timeout=15)
    r.raise_for_status()
    html = r.text

    events = []

    # event bloklarını yakala
    blocks = re.findall(r'<div class="section-event".*?</div>\s*</div>', html, re.S)

    for block in blocks:
        # Takımlar
        teams = re.search(r'<div class="event-competitors">(.*?)</div>', block, re.S)
        title = teams.group(1).strip() if teams else "Live Event"
        title = re.sub(r'\s+', ' ', title).replace("vs.", "vs")

        # Link
        link_m = re.search(r'href="([^"]+)"', block)
        if not link_m:
            continue
        link = urljoin(BASE_URL, link_m.group(1))

        # Canlı mı?
        live = "LIVE" in block.upper()

        events.append({
            "title": title,
            "url": link,
            "live": live
        })

    return events

def write_m3u(events):
    lines = ["#EXTM3U"]

    for ev in events:
        group = "Canlı Maçlar" if ev["live"] else "Yaklaşan Maçlar"
        lines.append(f'#EXTINF:-1 group-title="{group}",{ev["title"]}')
        lines.append(ev["url"])

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ {OUTPUT} oluşturuldu ({len(events)} maç)")

def main():
    events = get_events()
    if not events:
        print("⚠️ Maç bulunamadı ama dosya yine de oluşturuldu")

    write_m3u(events)

if __name__ == "__main__":
    main()
