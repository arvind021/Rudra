import requests
from config import YOUTUBE_API_KEY, YOUTUBE_COOKIES
from youtubesearchpython import VideosSearch
import os

async def search_youtube(query):
    # -------------------------------
    # Option 1: Try YouTube API (agar key valid ho)
    # -------------------------------
    if YOUTUBE_API_KEY:
        try:
            url = (
                f"https://www.googleapis.com/youtube/v3/search"
                f"?part=snippet&type=video&maxResults=1&key={YOUTUBE_API_KEY}&q={query}"
            )
            resp = requests.get(url)
            data = resp.json()
            if "items" in data and data["items"]:
                item = data["items"][0]
                video_id = item["id"]["videoId"]
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
