# ContentHub - 自媒体多平台AI自动分发系统

[![版本](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/AlanGehrig/ContentHub)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-orange.svg)](https://fastapi.tiangolo.com/)

> 一次上传素材，AI自动适配全平台格式、生成封面/文案/标签，一键分发+数据监控

## 📖 项目简介

ContentHub 是一款面向自媒体创作者和企业营销团队的多平台内容分发工具。通过AI技术实现内容的一次创作、全平台适配，帮助用户节省大量重复编辑和发布的时间。

### 核心价值

- ⚡ **效率提升**: 一次上传，自动适配所有平台尺寸和格式
- 🎨 **AI赋能**: 智能生成封面、文案、标题、标签
- 📊 **数据洞察**: 统一监控各平台内容表现
- 🔄 **批量操作**: 支持批量上传和批量分发
- 🛡️ **稳定可靠**: Redis队列支持，断线自动降级

## 🌟 核心功能

### 1. 智能图像处理
- 自动裁剪适配各平台尺寸
- 智能封面生成（添加水印、色彩增强）
- 支持格式：JPEG、PNG、GIF、WebP

### 2. AI文案生成
- 平台专属风格文案改编
- 智能标题生成（爆款标题模板）
- 自动生成平台适配标签

### 3. 一键分发
- 支持平台：小红书、抖音、微信公众号、独立站
- 批量发布到多个平台
- 模拟发布模式（API未接入时使用）

### 4. 数据监控
- 各平台数据统计（粉丝、点赞、评论、阅读量等）
- 任务状态追踪
- 发布历史记录

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Redis 5.0+（可选，不安装则使用内存队列）

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/AlanGehrig/ContentHub.git
cd ContentHub
```

#### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

#### 4. 配置环境变量（可选）

创建 `.env` 文件：

```env
# AI API配置（用于AI文案生成，可选）
AI_API_KEY=your_api_key_here

# Redis配置（可选，不配置则使用内存队列）
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

#### 5. 启动服务

**Windows:**
```bash
startup.bat
```

**Linux/Mac:**
```bash
chmod +x startup.sh
./startup.sh
```

或直接运行：

```bash
python main.py
```

#### 6. 访问API文档

打开浏览器访问：http://localhost:8000/docs

## 📚 API文档

### 基础信息

- **Base URL**: `http://localhost:8000/api/v1`
- **文档地址**: http://localhost:8000/docs

### 主要接口

#### 上传素材

```
POST /api/v1/upload
Content-Type: multipart/form-data

参数:
- file: 图片文件
- title: 内容标题
- content: 内容正文
- platforms: 目标平台（逗号分隔）
```

#### 批量上传

```
POST /api/v1/upload/batch
Content-Type: multipart/form-data

参数:
- files: 图片文件列表
- title: 内容标题
- content: 内容正文
- platforms: 目标平台
```

#### 执行分发

```
GET /api/v1/run
```

#### 获取系统状态

```
GET /api/v1/status
```

#### 获取数据统计

```
GET /api/v1/stats?platform=all
```

#### 获取任务列表

```
GET /api/v1/tasks?limit=20
```

### 完整API列表

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /upload | 上传素材并创建任务 |
| POST | /upload/batch | 批量上传 |
| GET | /run | 执行分发任务 |
| GET | /status | 系统状态 |
| GET | /stats | 数据统计 |
| GET | /stats/{platform} | 指定平台统计 |
| GET | /tasks | 任务列表 |
| GET | /tasks/{task_id} | 任务详情 |
| GET | /publish/history | 发布历史 |
| POST | /publish/simulate | 模拟发布 |
| GET | /platforms | 支持的平台列表 |
| POST | /image/process | 图像处理 |
| GET | /ai/title | 生成标题 |
| GET | /ai/tags | 生成标签 |
| POST | /ai/content | 生成平台专属文案 |

## 🏗️ 技术架构

```
ContentHub/
├── main.py              # FastAPI主入口
├── config.py            # 全局配置
├── api/
│   └── routes.py        # API路由定义
├── services/
│   ├── ai_adapter.py    # AI平台适配服务
│   ├── image_process.py  # 图像处理服务
│   ├── distribute.py    # 分发执行服务
│   └── monitor.py        # 数据监控服务
├── queue/
│   └── task_queue.py    # 任务队列（Redis/内存）
├── requirements.txt     # 依赖清单
├── startup.bat          # Windows启动脚本
├── startup.sh           # Linux/Mac启动脚本
├── README.md            # 中文文档
└── README_en.md         # English documentation
```

### 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI + Uvicorn |
| 图像处理 | OpenCV + Pillow |
| 任务队列 | Redis（降级：内存队列） |
| 数据验证 | Pydantic |
| HTTP客户端 | Requests |
| 环境配置 | python-dotenv |

### 平台尺寸规格

| 平台 | 尺寸 | 比例 |
|------|------|------|
| 小红书 | 1080×1440 | 竖版 3:4 |
| 抖音 | 1080×1920 | 竖版 9:16 |
| 微信公众号 | 900×500 | 横版 |
| 独立站 | 1920×1080 | 横版 16:9 |

## 🔧 配置说明

### 平台尺寸配置 (config.py)

```python
PLATFORM_SIZES = {
    "xiaohongshu": (1080, 1440),  # 竖版 3:4
    "douyin": (1080, 1920),        # 竖版 9:16
    "wechat": (900, 500),          # 横版 头条图
    "website": (1920, 1080)        # 横版 16:9
}
```

### Redis配置

```python
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
```

当Redis不可用时，系统会自动降级为内存队列，不影响基本功能。

### AI API配置

```python
AI_API_KEY = os.getenv("AI_API_KEY", "")
```

不配置AI API Key时，系统使用模拟文案生成器。

## 📝 使用示例

### Python调用示例

```python
import requests

# 上传素材
files = {'file': open('test.jpg', 'rb')}
data = {
    'title': '我的第一条笔记',
    'content': '今天分享一个好东西...',
    'platforms': 'xiaohongshu,douyin'
}
response = requests.post(
    'http://localhost:8000/api/v1/upload',
    files=files,
    data=data
)
print(response.json())

# 获取系统状态
response = requests.get('http://localhost:8000/api/v1/status')
print(response.json())

# 获取统计数据
response = requests.get('http://localhost:8000/api/v1/stats?platform=all')
print(response.json())
```

### cURL调用示例

```bash
# 上传素材
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@test.jpg" \
  -F "title=测试标题" \
  -F "content=测试内容" \
  -F "platforms=xiaohongshu,douyin"

# 执行分发
curl -X GET "http://localhost:8000/api/v1/run"

# 获取状态
curl -X GET "http://localhost:8000/api/v1/status"
```

## ⚠️ 注意事项

1. **文件大小限制**: 默认最大50MB
2. **Redis可选**: 不安装Redis时使用内存队列
3. **模拟模式**: API未接入时使用模拟发布
4. **生产部署**: 建议使用Gunicorn + Uvicorn workers

## 🔜 后续规划

- [ ] 集成各平台真实发布API
- [ ] 添加定时发布功能
- [ ] 支持视频内容处理
- [ ] 添加内容审核功能
- [ ] 优化AI文案生成模型
- [ ] 添加数据可视化仪表盘

## 📄 许可证

MIT License

## 👤 作者

**Alan Gehrig**
- GitHub: [@AlanGehrig](https://github.com/AlanGehrig)

## 🙏 致谢

感谢所有开源项目的贡献者！

---

*如果这个项目对你有帮助，请给一个 ⭐*
