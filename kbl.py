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

        response = requests.get(url, headers=headers, params=params, timeout=
