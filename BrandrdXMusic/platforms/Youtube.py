import asyncio
import os
import json
import random
import glob
from typing import Union
from pyrogram.types import Message
from pyrogram.enums import MessageEntityType
from youtubesearchpython.__future__ import VideosSearch
from BrandrdXMusic.utils.youtube_api import search_youtube
from BrandrdXMusic.utils.database import is_on_off
from BrandrdXMusic.utils.formatters import time_to_seconds


def cookie_txt_file():
    folder_path = f"{os.getcwd()}/cookies"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the cookies folder.")
    return f"cookies/{random.choice(txt_files).split('/')[-1]}"


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool("youtube.com" in link or "youtu.be" in link)

    async def url(self, message: Message) -> Union[str, None]:
        messages = [message]
        if message.reply_to_message:
            messages.append(message.reply_to_message)

        for msg in messages:
            entities = msg.entities or msg.caption_entities
            if entities:
                for ent in entities:
                    if ent.type in (MessageEntityType.URL, MessageEntityType.TEXT_LINK):
                        return ent.url if hasattr(ent, 'url') else msg.text[ent.offset:ent.offset+ent.length]
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):

        # -----------------------------------------
        # 1) If link → extract video ID
        # -----------------------------------------
        if "youtube.com" in link or "youtu.be" in link:
            try:
                if "watch?v=" in link:
                    vid = link.split("watch?v=")[1].split("&")[0]
                elif "youtu.be/" in link:
                    vid = link.split("youtu.be/")[1].split("?")[0]
                else:
                    vid = None
            except:
                vid = None

            # Convert link → search using ID
            res = await search_youtube(vid)
        else:
            # Normal query
            res = await search_youtube(link)

        # -----------------------------------------
        # 2) If BabyAPI returns data
        # -----------------------------------------
        if res:
            title = res.get("title")
            duration_min = res.get("duration", "0:00")
            thumbnail = (res.get("thumb") or "").split("?")[0]
            vidid = res.get("video_id")
            duration_sec = int(time_to_seconds(duration_min)) if duration_min else 0

            return title, duration_min, duration_sec, thumbnail, vidid

        # -----------------------------------------
        # 3) Fallback: scrape with youtubesearchpython
        # -----------------------------------------
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            duration_sec = int(time_to_seconds(duration_min)) if duration_min else 0

        return title, duration_min, duration_sec, thumbnail, vidid

    async def track(self, link: str, videoid: Union[bool, str] = None):
        details = await self.details(link, videoid)
        title, duration_min, _, thumbnail, vidid = details
        yturl = f"{self.base}{vidid}" if vidid else link
        return {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail
        }, vidid

    async def download(self, link: str, songaudio=False, songvideo=False, video=False, format_id=None, title=None):
        loop = asyncio.get_running_loop()

        def audio_dl():
            from yt_dlp import YoutubeDL
            opts = {
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "quiet": True,
                "cookiefile": cookie_txt_file()
            }
            ydl = YoutubeDL(opts)
            info = ydl.extract_info(link, download=False)
            path = f"downloads/{info['id']}.{info['ext']}"
            if os.path.exists(path):
                return path
            ydl.download([link])
            return path

        def video_dl():
            from yt_dlp import YoutubeDL
            opts = {
                "format": "bestvideo+bestaudio",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "quiet": True,
                "cookiefile": cookie_txt_file()
            }
            ydl = YoutubeDL(opts)
            info = ydl.extract_info(link, download=False)
            path = f"downloads/{info['id']}.{info['ext']}"
            if os.path.exists(path):
                return path
            ydl.download([link])
            return path

        if songvideo or video:
            return await loop.run_in_executor(None, video_dl)
        else:
            return await loop.run_in_executor(None, audio_dl)
