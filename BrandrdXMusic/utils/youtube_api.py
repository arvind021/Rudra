import requests
from config import YOUTUBE_API_KEY

async def search_youtube(query):
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&type=video&maxResults=1&key={YOUTUBE_API_KEY}&q={query}"
    )
    resp = requests.get(url)
    data = resp.json()
    if "items" not in data or not data["items"]:
        return None
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
