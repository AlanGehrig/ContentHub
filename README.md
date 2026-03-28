# ContentHub - 自媒体多平台AI自动分发系统

<div align="center">

[![版本](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/AlanGehrig/ContentHub)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-orange.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

**一次上传素材，AI自动适配全平台格式、生成封面/文案/标签，一键分发+数据监控**

</div>

---

## 🎯 项目简介

ContentHub 是一款面向自媒体创作者、摄影师和营销团队的多平台内容分发工具。

**解决什么问题？**

| 传统方式 | ContentHub |
|---------|-----------|
| 每个平台单独编辑 | 一次上传，AI自动适配 |
| 手动裁剪尺寸 | 自动裁剪到各平台最优比例 |
| 逐个平台发布 | 一键分发到所有平台 |
| 无法追踪效果 | 统一数据监控 |

---

## ✨ 核心功能

### 📸 智能图像处理

- **自动裁剪**：AI智能识别主体，确保最重要的内容在画面中心
- **封面生成**：自动调色+锐化，生成各平台最优封面
- **批量处理**：一次处理多个平台尺寸
- **格式支持**：JPEG、PNG、GIF、WebP

### ✍️ AI文案生成

- **平台专属风格**：根据平台调性自动改编文案语气
- **爆款标题**：AI生成高点击率标题
- **智能标签**：自动生成平台适配的热门标签
- **多语言支持**：中文/英文/俄语

### 🚀 一键分发

| 平台 | 尺寸规格 | 内容风格 |
|------|---------|---------|
| 小红书 | 1080×1440（竖版3:4） | 种草/治愈/干货 |
| 抖音 | 1080×1920（竖版9:16） | 热门/短句/强吸引 |
| 微信公众号 | 900×500（横版） | 正式/深度/完整 |
| 独立站 | 1920×1080（横版16:9） | SEO友好/专业 |

### 📊 数据监控

- 发布状态实时追踪
- 各平台数据统计
- 历史发布记录

---

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Redis 6+（可选，不装则用内存队列）

### 安装

**方式一：一键安装**
```powershell
# 克隆项目
git clone https://github.com/AlanGehrig/ContentHub.git
cd ContentHub

# 安装依赖
install_dependencies.bat

# 启动服务
startup.bat
```

**方式二：手动安装**
```bash
git clone https://github.com/AlanGehrig/ContentHub.git
cd ContentHub
pip install -r requirements.txt
python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8001)"
```

### 启动

```powershell
startup.bat
```

> 默认端口：**8001**（如8000被占用会自动切换）

### 访问

| 界面 | 地址 |
|------|------|
| **前端界面** | http://localhost:8001 |
| **API文档** | http://localhost:8001/docs |
| **健康检查** | http://localhost:8001/api/v1/status |

---

## 📐 技术架构

```
ContentHub/
├── main.py                    # FastAPI 主入口
├── config.py                  # 全局配置
├── api/
│   └── routes.py              # API 路由（20+接口）
├── services/
│   ├── ai_adapter.py         # AI 文案适配
│   ├── image_process.py      # OpenCV 图像处理
│   ├── distribute.py          # 分发执行
│   └── monitor.py             # 数据监控
├── task_queue_pkg/
│   └── task_queue.py          # 任务队列（Redis+内存降级）
├── frontend/
│   └── index.html             # 前端界面
├── requirements.txt           # 依赖清单
├── startup.bat                # Windows 启动
└── startup.sh                 # Linux/Mac 启动
```

### 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI + Uvicorn |
| 图像处理 | OpenCV + Pillow |
| 任务队列 | Redis（自动降级内存） |
| 数据验证 | Pydantic |
| 环境配置 | python-dotenv |

---

## 📖 API 文档

### 核心接口

#### 上传并分发
```bash
POST /api/v1/distribute/publish
Content-Type: multipart/form-data

参数：
- image_file: 图片文件
- title: 标题
- content: 正文内容
- platforms: 平台列表（xiaohongshu,douyin,wechat,website）
```

#### 系统状态
```bash
GET /api/v1/status
```

#### 平台列表
```bash
GET /api/v1/platforms
```

#### AI 生成标题
```bash
POST /api/v1/ai/generate
{
  "title": "原始标题",
  "content": "正文内容",
  "platform": "xiaohongshu"
}
```

#### 统计数据
```bash
GET /api/v1/stats
```

### 完整接口列表

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/distribute/publish` | 上传+分发 |
| GET | `/status` | 系统状态 |
| GET | `/platforms` | 平台配置 |
| POST | `/ai/generate` | AI 文案生成 |
| POST | `/image/process` | 图像处理 |
| GET | `/stats` | 数据统计 |
| GET | `/tasks` | 任务列表 |
| GET | `/publish/history` | 发布历史 |
| POST | `/publish/simulate` | 模拟发布 |

---

## 🕹️ 使用流程

```
1. 打开前端界面
   → http://localhost:8001

2. 上传图片素材
   → 拖拽或点击上传

3. 填写内容
   → 标题 + 正文

4. 选择目标平台
   → 小红书 / 抖音 / 公众号 / 独立站

5. 点击「一键分发」
   → 系统自动：
      • 裁剪适配各平台尺寸
      • 生成平台专属文案
      • 生成最优封面
      • 加入发布队列

6. 查看分发结果
   → 实时状态 + 历史记录
```

---

## 🔧 配置

### config.py

```python
# 平台尺寸配置
PLATFORM_SIZES = {
    "xiaohongshu": (1080, 1440),
    "douyin": (1080, 1920),
    "wechat": (900, 500),
    "website": (1920, 1080)
}

# Redis（可选）
REDIS_HOST = "localhost"
REDIS_PORT = 6379
```

### 环境变量（.env）

```env
AI_API_KEY=your_api_key_here
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## ⚠️ 注意事项

1. **Redis可选**：不安装Redis时自动降级为内存队列
2. **模拟模式**：正式API未接入前，使用模拟发布
3. **端口占用**：如8000被占用，自动使用8001

---

## 🔮 后续规划

- [ ] 集成小红书/抖音真实发布API
- [ ] 视频素材自动截帧
- [ ] 定时发布功能
- [ ] 内容审核模块
- [ ] 数据可视化仪表盘
- [ ] Chrome 插件支持

---

## 📄 许可证

MIT License

---

## 👤 作者

**Alan Gehrig**  
GitHub: [@AlanGehrig](https://github.com/AlanGehrig)  
摄影作品集：[LightPlanner AI](https://github.com/AlanGehrig/lightplanner-ai)

---

*如果对你有帮助，请给一个 ⭐*
