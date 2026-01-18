from datetime import datetime
from pathlib import Path

OUTPUT_FILE = "nw.m3u"

def main():
    content = [
        "#EXTM3U",
        f"# Generated at {datetime.utcnow().isoformat()} UTC",
        "",
        "# --- LIVE EVENTS PLACEHOLDER ---",
        "# Şu an aktif yayın yok",
    ]

    Path(OUTPUT_FILE).write_text(
        "\n".join(content) + "\n",
        encoding="utf-8"
    )

    print(f"✅ {OUTPUT_FILE} başarıyla oluşturuldu")

if __name__ == "__main__":
    main()
