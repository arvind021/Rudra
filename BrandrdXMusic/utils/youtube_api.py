import requests
from urllib.parse import quote_plus

# BabyAPI Direct Search URL (no key needed)
API_URL = "https://babyapi.pro/api/search?query="


async def search_youtube(query):
    """Search YouTube using BabyAPI.Pro (No YouTube API Required)."""
    
    if not API_URL:
        return None

    # Final API Endpoint
    final_url = f"{API_URL}{quote_plus(query)}"

    try:
        response = requests.get(final_url, timeout=10)
    except Exception:
        return None

    if not response or not response.ok:
        return None

    # Parse JSON
    try:
        data = response.json()
    except Exception:
        return None

    # Extract result list
    items = None

    if isinstance(data, dict):
        for key in ("results", "data", "items", "songs"):
            if key in data and isinstance(data[key], list):
                items = data[key]
                break

    # If BabyAPI returns a list directly
    if isinstance(data, list):
        items = data

    if not items:
        return None

    # Choose first search result
    item = items[0]

    # Extract values from various possible key names
    video_id = (
        item.get("video_id")
        or item.get("id")
        or item.get("videoId")
        or item.get("vid")
    )

    title = item.get("title") or item.get("name")
    thumb = item.get("thumbnail") or item.get("thumb")

    url = (
        item.get("url")
        or item.get("link")
        or item.get("webpage_url")
        or (f"https://www.youtube.com/watch?v={video_id}" if video_id else None)
    )

    if not video_id or not title:
        return None

    return {
        "video_id": video_id,
        "title": title,
        "thumb": thumb,
        "url": url
    }
