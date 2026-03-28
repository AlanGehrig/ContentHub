import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = "ContentHub - 自媒体AI自动分发系统"
VERSION = "1.0.0"
BASE_DIR = r"E:\openclaw\data\ContentHub"

SUPPORT_PLATFORMS = ["xiaohongshu", "douyin", "wechat", "website"]

PLATFORM_SIZES = {
    "xiaohongshu": (1080, 1440),  # 竖版 3:4
    "douyin": (1080, 1920),        # 竖版 9:16
    "wechat": (900, 500),          # 横版 头条图
    "website": (1920, 1080)        # 横版 16:9
}

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

AI_API_KEY = os.getenv("AI_API_KEY", "")

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB
