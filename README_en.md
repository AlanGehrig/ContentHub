# ContentHub - Multi-Platform AI Content Distribution System

<div align="center">

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/AlanGehrig/ContentHub)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-orange.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

**Upload once. Auto-adapt to all platforms. One-click publish with AI-generated captions, covers, and tags.**

</div>

---

## 🎯 What is ContentHub?

ContentHub is an AI-powered multi-platform content distribution tool for content creators, photographers, and marketing teams.

**The Problem:**

| Traditional | ContentHub |
|-------------|-----------|
| Edit manually for each platform | Upload once, AI auto-adapts |
| Crop images by hand | Smart center-crop with AI |
| Publish one by one | One-click to all platforms |
| No performance tracking | Unified analytics |

---

## ✨ Features

### 📸 Smart Image Processing

- **Auto Cropping**: AI identifies the subject, keeps it centered
- **Cover Generation**: Auto color correction + sharpening
- **Batch Processing**: One image → all platform sizes
- **Formats**: JPEG, PNG, GIF, WebP

### ✍️ AI Caption Generation

- **Platform-Native Style**: Auto-adapted tone per platform
- **Viral Titles**: AI-generated high CTR titles
- **Smart Tags**: Platform-specific trending hashtags
- **Multi-language**: Chinese / English / Russian

### 🚀 One-Click Publish

| Platform | Dimensions | Style |
|----------|-------------|-------|
| Xiaohongshu | 1080×1440 (3:4) | Lifestyle/Tutorial |
| Douyin | 1080×1920 (9:16) | Viral/Short-form |
| WeChat | 900×500 (Banner) | Professional/Deep |
| Website | 1920×1080 (16:9) | SEO-optimized |

### 📊 Analytics

- Real-time publish status
- Cross-platform statistics
- Publishing history

---

## 🚀 Quick Start

### Requirements

- Python 3.9+
- Redis 6+ (optional, falls back to in-memory queue)

### Installation

```bash
git clone https://github.com/AlanGehrig/ContentHub.git
cd ContentHub

# Install dependencies
pip install -r requirements.txt

# Start server
python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8001)"
```

### Access

| Interface | URL |
|-----------|-----|
| **Frontend** | http://localhost:8001 |
| **API Docs** | http://localhost:8001/docs |
| **Health Check** | http://localhost:8001/api/v1/status |

---

## 📐 Architecture

```
ContentHub/
├── main.py                    # FastAPI entry point
├── config.py                  # Global config
├── api/
│   └── routes.py              # 20+ API routes
├── services/
│   ├── ai_adapter.py          # AI caption adapter
│   ├── image_process.py       # OpenCV image processing
│   ├── distribute.py          # Distribution engine
│   └── monitor.py             # Analytics
├── task_queue_pkg/
│   └── task_queue.py          # Task queue (Redis + memory fallback)
├── frontend/
│   └── index.html             # Web interface
├── requirements.txt
├── startup.bat                # Windows launcher
└── startup.sh                 # Linux/Mac launcher
```

---

## 📖 API Reference

### Core Endpoints

#### Upload & Publish
```bash
POST /api/v1/distribute/publish
Content-Type: multipart/form-data

Params:
- image_file: Image file
- title: Title
- content: Body text
- platforms: xiaohongshu,douyin,wechat,website
```

#### System Status
```bash
GET /api/v1/status
```

#### Platform List
```bash
GET /api/v1/platforms
```

#### AI Generate
```bash
POST /api/v1/ai/generate
{
  "title": "Original title",
  "content": "Body content",
  "platform": "xiaohongshu"
}
```

---

## 🔧 Configuration

### config.py

```python
PLATFORM_SIZES = {
    "xiaohongshu": (1080, 1440),
    "douyin": (1080, 1920),
    "wechat": (900, 500),
    "website": (1920, 1080)
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
```

### Environment (.env)

```env
AI_API_KEY=your_api_key_here
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## ⚠️ Notes

1. **Redis is optional**: Falls back to in-memory queue if unavailable
2. **Simulated mode**: Uses mock publishing until real APIs are integrated
3. **Port 8001**: Default port (8000 fallback if occupied)

---

## 🔮 Roadmap

- [ ] Real Xiaohongshu/Douyin API integration
- [ ] Video frame extraction
- [ ] Scheduled publishing
- [ ] Content moderation
- [ ] Analytics dashboard
- [ ] Chrome extension

---

## 📄 License

MIT License

---

## 👤 Author

**Alan Gehrig**  
GitHub: [@AlanGehrig](https://github.com/AlanGehrig)  
Photography Portfolio: [LightPlanner AI](https://github.com/AlanGehrig/lightplanner-ai)

---

*If this project helps you, please give it a ⭐*
