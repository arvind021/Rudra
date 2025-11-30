import requests
from config import YOUTUBE_API_KEY, YOUTUBE_COOKIES, API_URL
from youtubesearchpython import VideosSearch
import os
from urllib.parse import quote_plus

async def search_youtube(query):
    # -------------------------------
    # Option 1: Try YouTube API (agar key valid ho)
    # -------------------------------
    if YOUTUBE_API_KEY:
        try:
            url = (
                f"https://www.googleapis.com/youtube/v3/search"
                f"?part=snippet&type=video&maxResults=1&key={YOUTUBE_API_KEY}&q={quote_plus(query)}"
            )
            resp = requests.get(url, timeout=10)
            data = resp.json()
            if "items" in data and data["items"]:
                item = data["items"][0]
                # safe access: sometimes id may be dict with videoId
                vid = item.get("id", {})
                video_id = vid.get("videoId") if isinstance(vid, dict) else vid
                title = item["snippet"]["title"]
                thumbnail = item["snippet"]["thumbnails"]["high"]["url"]
                return {
                    "video_id": video_id,
                    "title": title,
                    "thumb": thumbnail,
                    "url": f"https://www.youtube.com/watch?v={video_id}"
                }
        except Exception:
            pass  # Agar API fail ho jaye, fallback search chalega

    # -------------------------------
    # Option 1.5: Try custom Baby API (API_URL)
    # -------------------------------
    if API_URL:
        try:
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
                    if isinstance(data, dict) and ("video_id" in data or "id" in data or "url" in data):
                        video_id = data.get("video_id") or data.get("id") or data.get("videoId")
                        title = data.get("title") or data.get("name")
                        thumb = data.get("thumbnail") or data.get("thumb")
                        url = data.get("url") or data.get("link")
                        if not url and video_id:
                            url = f"https://www.youtube.com/watch?v={video_id}"
                        if video_id and title and url:
                            return {
                                "video_id": video_id,
                                "title": title,
                                "thumb": thumb,
                                "url": url
                            }
        except Exception:
            pass

    # -------------------------------
    # Option 2: yt-dlp + cookies (login based)
    # -------------------------------
    ydl_opts = {
        "format": "bestaudio",
        "quiet": True
    }
    if YOUTUBE_COOKIES and os.path.exists(YOUTUBE_COOKIES):
        ydl_opts["cookiefile"] = YOUTUBE_COOKIES

    try:
        import yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if info and "entries" in info and len(info["entries"]) > 0:
                entry = info["entries"][0]
                return {
                    "video_id": entry.get("id"),
                    "title": entry.get("title"),
                    "thumb": entry.get("thumbnail"),
                    "url": entry.get("webpage_url")
                }
    except Exception:
        pass

    # -------------------------------
    # Option 3: Fallback: youtube-search-python scraping
    # -------------------------------
    try:
        videos_search = VideosSearch(query, limit=1)
        result = videos_search.result()
        if result["result"]:
            entry = result["result"][0]
            return {
                "video_id": entry["id"],
                "title": entry["title"],
                "thumb": entry["thumbnails"][0]["url"],
                "url": entry["link"]
            }
    except Exception:
        pass

    # Agar sab fail ho jaye
    return None
