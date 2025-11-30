import requests
from config import API_URL
from urllib.parse import quote_plus
import re


def extract_video_id(url):
    """Extract YouTube video ID from URL."""
    patterns = [
        r"youtube\.com/watch\?v=([^&#]+)",
        r"youtube\.com/shorts/([^&#]+)",
        r"youtu\.be/([^&#]+)"
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


async def search_youtube(query):
    if not API_URL:
        return None

    base = API_URL.rstrip("/")

    # ----- If YouTube URL → Extract video ID -----
    vid = extract_video_id(query)
    if vid:
        query = vid  # convert link → ID

    # ------------ TRY API URLs ------------
    tried_urls = [
        f"{base}/search?q={quote_plus(query)}",
        f"{base}/search?query={quote_plus(query)}",
        f"{base}/video?id={quote_plus(query)}",
        f"{base}/search/{quote_plus(query)}",
    ]

    for api_call in tried_urls:
        try:
            resp = requests.get(api_call, timeout=10)
        except:
            resp = None

        if resp and resp.ok:
            try:
                data = resp.json()
            except:
                continue

            # ----- Extract list of items -----
            items = None

            if isinstance(data, dict):
                for k in ("results", "data", "items", "songs", "tracks"):
                    if k in data and isinstance(data[k], list):
                        items = data[k]
                        break

                # Some APIs return single result
                if not items and "title" in data:
                    items = [data]

            elif isinstance(data, list):
                items = data

            if not items:
                continue

            it = items[0]

            video_id = it.get("video_id") or it.get("id") or it.get("videoId") or it.get("vid")
            title = it.get("title") or it.get("name")
            thumb = it.get("thumbnail") or it.get("thumb") or it.get("thumbnailUrl")
            url = it.get("url") or f"https://www.youtube.com/watch?v={video_id}"

            # ----- Duration Fix -----
            duration = it.get("duration") or it.get("length") or it.get("time") or "0:00"

            if video_id and title:
                return {
                    "video_id": video_id,
                    "title": title,
                    "thumb": thumb,
                    "url": url,
                    "duration": duration
                }

    return None
