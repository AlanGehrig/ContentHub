# ContentHub - Local Image Processing Tool

<div align="center">

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/AlanGehrig/ContentHub)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-orange.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

**Local batch image processing - smart cropping, cover generation, AI caption assistance**

</div>

---

## 🎯 What is ContentHub?

ContentHub is a **local image processing tool** that helps you:

| Feature | Description |
|---------|-------------|
| 📐 **Smart Cropping** | Upload once, auto-crop to all platform sizes |
| 🎨 **Cover Generation** | Auto color correction + sharpening |
| ✍️ **AI Caption Assist** | Generate platform-adapted titles and tags (mock mode) |
| 📊 **Task Queue** | Redis or in-memory queue, batch processing supported |

---

## ⚠️ Important

**This is a LOCAL image processing tool, NOT a publishing platform.**

| Can Do | Cannot Do |
|--------|----------|
| ✅ Local image cropping | ❌ Post to Xiaohongshu/TikTok/WeChat |
| ✅ Cover generation | ❌ Real account authorization |
| ✅ Caption generation (mock) | ❌ Official platform APIs |
| ✅ Batch processing | ❌ Real publishing |

**Why?**
- Xiaohongshu, Douyin, and WeChat Official Accounts **do not have public content posting APIs**
- Real publishing requires official OAuth authentication, almost impossible for individual developers
- This tool focuses on **local processing** and automates repetitive work

---

## ✨ Features

### 📸 Smart Image Processing

| Platform | Dimensions | Ratio |
|----------|------------|-------|
| Xiaohongshu | 1080×1440 | 3:4 |
| Douyin | 1080×1920 | 9:16 |
| WeChat | 900×500 | Banner |
| Website | 1920×1080 | 16:9 |

### 🎨 Cover Generation

- Auto brightness + sharpening
- Suitable for e-commerce, product, portrait scenarios

### ✍️ AI Caption Assist

- Platform-style title generation
- Trending hashtag generation
- Mock captions (when no real AI is configured)

---

## 🚀 Quick Start

### Requirements

- Python 3.9+
- Redis 6+ (optional, falls back to in-memory queue)

### Installation

```powershell
git clone https://github.com/AlanGehrig/ContentHub.git
cd ContentHub
install_dependencies.bat
startup.bat
```

### Access

| Interface | URL |
|-----------|-----|
| **Frontend** | http://localhost:8001 |
| **API Docs** | http://localhost:8001/docs |

---

## 📖 API Reference

```bash
# Upload & Process
POST /api/v1/distribute/publish

# System Status
GET /api/v1/status

# Platform List
GET /api/v1/platforms

# AI Generate
POST /api/v1/ai/generate
```

Full docs: http://localhost:8001/docs

---

## 🔧 Configuration

Copy `.env.example` to `.env`:

```env
# AI API (optional)
AI_API_KEY=

# Redis (optional)
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 👤 Author

**Alan Gehrig**  
GitHub: [@AlanGehrig](https://github.com/AlanGehrig)  
Photography Portfolio: [LightPlanner AI](https://github.com/AlanGehrig/lightplanner-ai)
