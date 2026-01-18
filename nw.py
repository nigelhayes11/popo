import requests
from selectolax.parser import HTMLParser
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

    html = HTMLParser(r.text)
    events = []

    for ev in html.css(".section-event"):
        title = "Live Event"

        teams = ev.css_first(".event-competitors")
        if teams:
            title = teams.text(strip=True).replace("vs.", "vs")

        link_node = ev.css_first("a")
        if not link_node:
            continue

        link = urljoin(BASE_URL, link_node.attributes.get("href"))

        status_node = ev.css_first(".event-countdown")
        status = status_node.text(strip=True).lower() if status_node else ""

        events.append({
            "title": title,
            "url": link,
            "live": "live" in status
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
        print("⚠️ Maç bulunamadı ama dosya yine de oluşturulacak")

    write_m3u(events)

if __name__ == "__main__":
    main()
