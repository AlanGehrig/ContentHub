# ContentHub - 自媒体本地图像处理工具

<div align="center">

[![版本](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/AlanGehrig/ContentHub)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-orange.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

**本地图像批量处理工具 - 智能裁剪、封面生成、AI文案辅助**

</div>

---

## 🎯 是什么

ContentHub 是一款本地图像处理工具，帮助你：

| 功能 | 说明 |
|------|------|
| 📐 **智能裁剪** | 一次上传，自动裁剪到各平台最优尺寸 |
| 🎨 **封面生成** | 自动调色+锐化，生成高质量封面 |
| ✍️ **AI 文案辅助** | 生成平台适配的标题和标签（模拟模式） |
| 📊 **任务队列** | Redis 或内存队列，支持批量处理 |

---

## ⚠️ 重要说明

**本工具是本地图像处理工具，不是发布平台。**

| 能做到 | 不能做到 |
|--------|---------|
| ✅ 本地图像裁剪 | ❌ 发布到小红书/抖音/公众号 |
| ✅ 封面生成 | ❌ 真实账号授权 |
| ✅ 文案生成（模拟） | ❌ 平台官方 API |
| ✅ 批量处理 | ❌ 真实发布 |

**为什么？**
- 小红书、抖音、微信公众号 **没有公开的内容发布 API**
- 真实发布需要平台官方 OAuth 认证，个人开发者几乎无法申请
- 本工具专注于 **本地处理**，把重复工作自动化

---

## ✨ 核心功能

### 📸 智能图像处理

| 平台 | 尺寸 | 比例 |
|------|------|------|
| 小红书 | 1080×1440 | 竖版 3:4 |
| 抖音 | 1080×1920 | 竖版 9:16 |
| 微信公众号 | 900×500 | 横版 |
| 独立站 | 1920×1080 | 横版 16:9 |

### 🎨 封面生成

- 自动提亮 + 锐化
- 适合电商、产品、人像等场景

### ✍️ AI 文案辅助

- 生成平台风格标题
- 生成热门标签
- 模拟文案（无真实 AI 时使用）

---

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Redis 6+（可选，不装则用内存队列）

### 安装

```powershell
# 克隆项目
git clone https://github.com/AlanGehrig/ContentHub.git
cd ContentHub

# 安装依赖
install_dependencies.bat

# 启动服务
startup.bat
```

### 访问

| 界面 | 地址 |
|------|------|
| **前端界面** | http://localhost:8001 |
| **API文档** | http://localhost:8001/docs |

---

## 📐 技术架构

```
ContentHub/
├── main.py                    # FastAPI 主入口
├── config.py                  # 全局配置
├── api/
│   └── routes.py              # API 路由
├── services/
│   ├── ai_adapter.py          # AI 文案适配
│   ├── image_process.py       # OpenCV 图像处理
│   ├── distribute.py          # 分发执行
│   └── monitor.py             # 数据监控
├── task_queue_pkg/
│   └── task_queue.py          # 任务队列
├── frontend/
│   └── index.html             # 前端界面
├── requirements.txt
├── startup.bat
└── startup.sh
```

---

## 📖 API 文档

### 核心接口

```bash
# 上传并处理
POST /api/v1/distribute/publish
Content-Type: multipart/form-data

# 系统状态
GET /api/v1/status

# 平台列表
GET /api/v1/platforms

# AI 生成
POST /api/v1/ai/generate
```

### 完整接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/distribute/publish` | 上传+处理+分发 |
| GET | `/status` | 系统状态 |
| GET | `/platforms` | 平台配置 |
| POST | `/ai/generate` | AI 文案生成 |
| POST | `/image/process` | 图像处理 |
| GET | `/stats` | 数据统计 |
| GET | `/tasks` | 任务列表 |

完整文档：http://localhost:8001/docs

---

## 🔧 配置

复制 `.env.example` 为 `.env`：

```env
# AI API（可选）
AI_API_KEY=

# Redis（可选，不填则用内存队列）
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## 🔮 后续规划

- [ ] 浏览器自动化（Selenium/Playwright）实现真实平台发布
- [ ] 定时发布功能
- [ ] 素材管理界面
- [ ] 数据可视化仪表盘

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 👤 作者

**Alan Gehrig**  
GitHub: [@AlanGehrig](https://github.com/AlanGehrig)  
摄影作品集：[LightPlanner AI](https://github.com/AlanGehrig/lightplanner-ai)
