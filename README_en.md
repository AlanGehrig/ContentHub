# ContentHub - Multi-Platform AI Content Distribution System

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/AlanGehrig/ContentHub)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-orange.svg)](https://fastapi.tiangolo.com/)

> Upload once, automatically adapt to all platforms, generate covers/copy/tags, one-click distribute + data monitoring

## 📖 Introduction

ContentHub is a multi-platform content distribution tool for content creators and marketing teams. Using AI technology, it enables one-time content creation with automatic platform adaptation, saving users significant time on repetitive editing and publishing.

### Core Value

- ⚡ **Efficiency**: Upload once, automatically adapt to all platform sizes and formats
- 🎨 **AI-Powered**: Smart cover generation, copy writing, titles, and tags
- 📊 **Data Insights**: Unified monitoring of content performance across platforms
- 🔄 **Batch Operations**: Support batch upload and distribution
- 🛡️ **Reliable**: Redis queue support with automatic fallback

## 🌟 Features

### 1. Smart Image Processing
- Auto-cropping to fit platform sizes
- Smart cover generation (watermark, color enhancement)
- Supported formats: JPEG, PNG, GIF, WebP

### 2. AI Copy Generation
- Platform-specific style adaptation
- Smart title generation (viral title templates)
- Auto-generated platform-specific tags

### 3. One-Click Distribution
- Supported platforms: Xiaohongshu, Douyin, WeChat Official Account, Website
- Batch publish to multiple platforms
- Simulation mode (for when APIs are not connected)

### 4. Data Monitoring
- Platform statistics (followers, likes, comments, views, etc.)
- Task status tracking
- Publishing history

## 🚀 Quick Start

### Requirements

- Python 3.8+
- Redis 5.0+ (optional, falls back to in-memory queue)

### Installation

#### 1. Clone the project

```bash
git clone https://github.com/AlanGehrig/ContentHub.git
cd ContentHub
```

#### 2. Create virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure environment variables (optional)

Create a `.env` file:

```env
# AI API config (for AI copy generation, optional)
AI_API_KEY=your_api_key_here

# Redis config (optional, falls back to in-memory queue)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

#### 5. Start the service

**Windows:**
```bash
startup.bat
```

**Linux/Mac:**
```bash
chmod +x startup.sh
./startup.sh
```

Or run directly:

```bash
python main.py
```

#### 6. Access API documentation

Open browser: http://localhost:8000/docs

## 📚 API Documentation

### Basic Info

- **Base URL**: `http://localhost:8000/api/v1`
- **Docs**: http://localhost:8000/docs

### Main Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /upload | Upload material and create task |
| POST | /upload/batch | Batch upload |
| GET | /run | Execute distribution task |
| GET | /status | System status |
| GET | /stats | Data statistics |
| GET | /tasks | Task list |
| POST | /publish/simulate | Simulate publish |
| GET | /platforms | Supported platforms |
| POST | /image/process | Image processing |
| GET | /ai/title | Generate title |
| GET | /ai/tags | Generate tags |
| POST | /ai/content | Generate platform-specific copy |

## 🏗️ Architecture

```
ContentHub/
├── main.py              # FastAPI main entry
├── config.py            # Global configuration
├── api/
│   └── routes.py        # API routes
├── services/
│   ├── ai_adapter.py    # AI platform adapter
│   ├── image_process.py  # Image processing
│   ├── distribute.py     # Distribution service
│   └── monitor.py        # Data monitoring
├── queue/
│   └── task_queue.py    # Task queue (Redis/in-memory)
├── requirements.txt     # Dependencies
├── startup.bat          # Windows startup script
├── startup.sh          # Linux/Mac startup script
├── README.md            # Chinese documentation
└── README_en.md         # English documentation
```

### Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI + Uvicorn |
| Image Processing | OpenCV + Pillow |
| Task Queue | Redis (fallback: in-memory) |
| Validation | Pydantic |
| HTTP Client | Requests |
| Config | python-dotenv |

### Platform Size Specs

| Platform | Size | Ratio |
|----------|------|-------|
| Xiaohongshu | 1080×1440 | Portrait 3:4 |
| Douyin | 1080×1920 | Portrait 9:16 |
| WeChat | 900×500 | Landscape |
| Website | 1920×1080 | Landscape 16:9 |

## 🔧 Configuration

### Platform Sizes (config.py)

```python
PLATFORM_SIZES = {
    "xiaohongshu": (1080, 1440),  # Portrait 3:4
    "douyin": (1080, 1920),        # Portrait 9:16
    "wechat": (900, 500),          # Landscape
    "website": (1920, 1080)        # Landscape 16:9
}
```

### Redis Config

```python
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
```

When Redis is unavailable, the system automatically falls back to in-memory queue.

### AI API Config

```python
AI_API_KEY = os.getenv("AI_API_KEY", "")
```

Without AI API Key, the system uses a mock copy generator.

## 📝 Usage Examples

### Python Example

```python
import requests

# Upload material
files = {'file': open('test.jpg', 'rb')}
data = {
    'title': 'My First Post',
    'content': 'Sharing something great today...',
    'platforms': 'xiaohongshu,douyin'
}
response = requests.post(
    'http://localhost:8000/api/v1/upload',
    files=files,
    data=data
)
print(response.json())
```

### cURL Example

```bash
# Upload
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@test.jpg" \
  -F "title=Test Title" \
  -F "content=Test Content" \
  -F "platforms=xiaohongshu,douyin"

# Run distribution
curl -X GET "http://localhost:8000/api/v1/run"

# Get status
curl -X GET "http://localhost:8000/api/v1/status"
```

## ⚠️ Notes

1. **File Size Limit**: Default max 50MB
2. **Redis Optional**: Uses in-memory queue without Redis
3. **Simulation Mode**: For when APIs are not connected
4. **Production**: Recommend using Gunicorn + Uvicorn workers

## 🔜 Roadmap

- [ ] Integrate real platform publishing APIs
- [ ] Add scheduled publishing
- [ ] Support video content processing
- [ ] Add content moderation
- [ ] Optimize AI copy generation
- [ ] Add data visualization dashboard

## 📄 License

MIT License

## 👤 Author

**Alan Gehrig**
- GitHub: [@AlanGehrig](https://github.com/AlanGehrig)

---

*If this project is helpful, please give a ⭐*
