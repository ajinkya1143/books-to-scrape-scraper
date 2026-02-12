import requests
from config import HEADERS


def get_html(url: str) -> str | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as err:
        print(f"[FETCH ERROR] {url} -> {err}")
        return None
