import re
import os
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID", None))
API_HASH = getenv("API_HASH", None)

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN", None)

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", None)
MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME", None)
PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE", None)

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 900))

# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID", None))

# Get this value from @BRANDRD_ROBOT on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", "7408008545"))

# Define SUDO_USERS as a list
SUDO_USERS = [7408008545]  # Add more user IDs as needed

## Fill these variables if you're deploying on heroku.
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/arvind021/Rudra")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", None)

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/RU_DRA_098")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/RU_DRA_098")

AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))
AUTO_GCAST = os.getenv("AUTO_GCAST")
AUTO_GCAST_MSG = getenv("AUTO_GCAST_MSG", "")

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "bcfe26b0ebc3428882a0b5fb3e872473")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "907c6a054c214005aeae1fd752273cc4")

SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "50"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "25"))

SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "180"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "2000"))

# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))

# Pyrogram String sessions
STRING1 = getenv("STRING_SESSION",  None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

# ============================================================
#  BABYAPI MODE: DIRECT URL PLAYBACK (NO YOUTUBE API KEY)
# ============================================================

# Main API URL
API_URL = getenv("API_URL", "https://BabyAPI.Pro")

# Disable YouTube API key completely
YOUTUBE_API_KEY = None

# Disable YouTube cookies completely
YOUTUBE_COOKIES = None
YOUTUBE_COOKIES_FILE_CONTENT = None

# ============================================================

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

START_IMG_URL = getenv(
    "START_IMG_URL", "https://graph.org/file/f0e790de4d84d5b4dab72-bc4dcadff42362281c.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://graph.org/file/f0e790de4d84d5b4dab72-bc4dcadff42362281c.jpg"
)
PLAYLIST_IMG_URL = "https://graph.org/file/f0e790de4d84d5b4dab72-bc4dcadff42362281c.jpg"
STATS_IMG_URL = "https://graph.org/file/f0e790de4d84d5b4dab72-bc4dcadff42362281c.jpg"
TELEGRAM_AUDIO_URL = "https://graph.org/file/f0e790de4d84d5b4dab72-bc4dcadff42362281c.jpg"
TELEGRAM_VIDEO_URL = "https://graph.org/file/f0e790de4d84d5b4dab72-bc4dcadff42362281c.jpg"
STREAM_IMG_URL = "https://graph.org/file/f0e790de4d84d5b4dab72-bc4dcadff42362281c.jpg"
SOUNCLOUD_IMG_URL = "https://graph.org/file/f0e790de4d84d5b4dab72-bc4dcadff42362281c.jpg"
YOUTUBE_IMG_URL = "https://graph.org/file/f0e790de4d84d5b4dab72-bc4dcadff42362281c.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://graph.org/file/f0e790de4d84d5b4dab72-bc4dcadff42362281c.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://graph.org/file/f0e790de4d84d5b4dab72-bc4dcadff42362281c.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://graph.org/file/f0e790de4d84d5b4dab72-bc4dcadff42362281c.jpg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. It must start with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. It must start with https://"
        )
