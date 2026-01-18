import requests
from pathlib import Path

INPUT_M3U = "liveevents.m3u8"
OUTPUT_M3U = "liveeventsfilter.m3u8"

TIMEOUT = 10
VALID_CONTENT_TYPES = {
    "application/vnd.apple.mpegurl",
    "application/x-mpegURL",
    "video/mp4",
    "audio/mpeg",
    "video/ts",
    "video/x-flv",
}

def is_stream_playable(url, headers=None):
    headers = headers or {}
    try:
        r = requests.head(url, headers=headers, timeout=TIMEOUT, allow_redirects=True)
        if r.status_code < 400:
            ct = r.headers.get("Content-Type", "").split(";")[0]
            if ct in VALID_CONTENT_TYPES:
                return True
    except:
        pass

    try:
        r = requests.get(url, headers=headers, timeout=TIMEOUT, stream=True)
        if r.status_code < 400:
            ct = r.headers.get("Content-Type", "").split(";")[0]
            return ct in VALID_CONTENT_TYPES
    except:
        pass

    return False


def main():
    if not Path(INPUT_M3U).exists():
        print("❌ liveevents.m3u8 yok")
        return

    with open(INPUT_M3U, "r", encoding="utf-8") as f:
        lines = [l.rstrip() for l in f]

    output = ["#EXTM3U"]
    tags = []
    vlcopts = []

    for line in lines:
        if line.startswith("#EXTINF"):
            tags = [line]
            vlcopts = []
        elif line.startswith("#EXTVLCOPT"):
            vlcopts.append(line)
        elif line and not line.startswith("#"):
            headers = {}
            for opt in vlcopts:
                kv = opt.replace("#EXTVLCOPT:", "").split("=", 1)
                if len(kv) == 2:
                    k, v = kv
                    if k.lower() == "http-referrer":
                        headers["Referer"] = v
                    elif k.lower() == "http-origin":
                        headers["Origin"] = v
                    elif k.lower() == "http-user-agent":
                        headers["User-Agent"] = v

            print("Checking:", line)
            if is_stream_playable(line, headers):
                print("  ✓ OK")
                output.extend(tags)
                output.extend(vlcopts)
                output.append(line)
            else:
                print("  ✗ FAIL")

            tags = []
            vlcopts = []

    with open(OUTPUT_M3U, "w", encoding="utf-8") as f:
        f.write("\n".join(output) + "\n")

    print(f"\n✅ Oluşturuldu: {OUTPUT_M3U}")


if __name__ == "__main__":
    main()
