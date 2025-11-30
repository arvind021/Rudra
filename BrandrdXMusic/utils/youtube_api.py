import requests
from config import API_URL
from urllib.parse import quote_plus

async def search_youtube(query):
    if not API_URL:
        return None

    base = API_URL.rstrip('/')
    tried_urls = [
        f"{base}/search?q={quote_plus(query)}",
        f"{base}/search?query={quote_plus(query)}",
        f"{base}/search/{quote_plus(query)}",
        f"{base}/?q={quote_plus(query)}",
    ]

    for api_call in tried_urls:
        try:
            resp = requests.get(api_call, timeout=10)
        except Exception:
            resp = None
        if resp and resp.ok:
            try:
                data = resp.json()
            except Exception:
                continue

            items = None
            if isinstance(data, dict):
                for k in ("results", "data", "items", "songs", "tracks"):
                    if k in data and isinstance(data[k], list):
                        items = data[k]
                        break
            elif isinstance(data, list):
                items = data

            if items and len(items) > 0:
                it = items[0]
                video_id = it.get("video_id") or it.get("id") or it.get("videoId") or it.get("vid")
                title = it.get("title") or it.get("name")
                thumb = it.get("thumbnail") or it.get("thumb") or it.get("thumbnailUrl")
                url = it.get("url") or it.get("link") or it.get("webpage_url")
                if not url and video_id:
                    url = f"https://www.youtube.com/watch?v={video_id}"
                if video_id and title and url:
                    return {
                        "video_id": video_id,
                        "title": title,
                        "thumb": thumb,
                        "url": url
                    }

    return None
