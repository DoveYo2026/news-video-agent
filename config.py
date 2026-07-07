"""
Configuration settings for News Video Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

# News API
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
NEWS_API_URL = os.getenv("NEWS_API_URL", "https://newsapi.org/v2")
NEWS_KEYWORDS = [
    "technology",
    "business",
    "science",
    "health",
    "politics",
    "entertainment"
]

# Google Cloud TTS
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
TTS_LANGUAGE_CODE = os.getenv("TTS_LANGUAGE_CODE", "en-GB")
TTS_VOICE_GENDER = os.getenv("TTS_VOICE_GENDER", "FEMALE")
TTS_VOICE_NAME = "en-GB-Standard-B"  # British female voice
TTS_SPEECH_RATE = 1.0
TTS_PITCH = 0.0

# Video Settings
VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", "1080"))
VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", "1920"))
VIDEO_FPS = int(os.getenv("VIDEO_FPS", "30"))
VIDEO_DURATION_MIN = int(os.getenv("VIDEO_DURATION_MIN", "15"))
VIDEO_DURATION_MAX = int(os.getenv("VIDEO_DURATION_MAX", "30"))
VIDEO_BITRATE = os.getenv("VIDEO_BITRATE", "5000k")
VIDEO_FORMAT = "vertical"  # 9:16 aspect ratio for TikTok/WeChat

# Text-to-Speech Settings
TTS_SPEED = 1.1  # Slightly faster for short videos
TTS_VOLUME = 0.9

# Visual Design
FONT_TITLE_SIZE = 60
FONT_BODY_SIZE = 40
FONT_SOURCE_SIZE = 24
FONT_FAMILY = "Arial"
BG_COLOR = (255, 255, 255)  # White background
TEXT_COLOR = (0, 0, 0)  # Black text
ACCENT_COLOR = (0, 102, 204)  # Blue accent
SOURCE_COLOR = (128, 128, 128)  # Gray for source

# Paths
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output/videos")
TEMP_DIR = os.getenv("TEMP_DIR", "./temp")
LOG_DIR = "./logs"

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Social Media Upload
TIKTOK_ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN", "")
TIKTOK_REFRESH_TOKEN = os.getenv("TIKTOK_REFRESH_TOKEN", "")
TIKTOK_VIDEO_TITLE_PREFIX = "📰 Breaking News: "
TIKTOK_HASHTAGS = ["#news", "#breakingnews", "#shorts", "#newstoday"]

WECHAT_ACCESS_TOKEN = os.getenv("WECHAT_ACCESS_TOKEN", "")
WECHAT_MEDIA_ID = os.getenv("WECHAT_MEDIA_ID", "")

# Scheduling
SCHEDULE_TIME = os.getenv("SCHEDULE_TIME", "09:00")
VIDEOS_PER_DAY = int(os.getenv("VIDEOS_PER_DAY", "3"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
