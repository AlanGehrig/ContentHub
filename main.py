"""
ContentHub - 自媒体多平台AI自动分发系统
FastAPI 主入口

一次上传素材，AI自动适配全平台格式、生成封面/文案/标签，一键分发+数据监控
"""
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import config
from api.routes import router

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info(f"🚀 {config.PROJECT_NAME} v{config.VERSION} 启动中...")
    logger.info(f"📁 上传目录: {config.UPLOAD_DIR}")

    # 确保上传目录存在
    os.makedirs(config.UPLOAD_DIR, exist_ok=True)

    # 检查Redis连接
    try:
        import redis
        client = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
            socket_connect_timeout=3
        )
        client.ping()
        logger.info("✅ Redis 连接成功")
    except Exception as e:
        logger.warning(f"⚠️  Redis 连接失败，将使用内存队列: {e}")

    logger.info("✅ 系统初始化完成")

    yield

    # 关闭时
    logger.info("👋 ContentHub 正在关闭...")


# 创建FastAPI应用
app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.VERSION,
    description="""
## ContentHub - 自媒体多平台AI自动分发系统

### 核心功能
- 📤 **素材上传**: 支持批量上传图片素材
- 🎨 **AI适配**: 自动裁剪、生成封面、适配各平台尺寸
- ✍️ **智能文案**: AI生成平台专属文案、标题、标签
- 🚀 **一键分发**: 一次操作分发到小红书、抖音、微信公众号、独立站
- 📊 **数据监控**: 实时追踪发布状态和数据统计

### 支持平台
- 小红书 (xiaohongshu) - 竖版 3:4 (1080×1440)
- 抖音 (douyin) - 竖版 9:16 (1080×1920)
- 微信公众号 (wechat) - 横版 (900×500)
- 独立站 (website) - 横版 16:9 (1920×1080)
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 配置CORS（允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api/v1", tags=["ContentHub"])


@app.get("/", tags=["Root"])
async def root():
    """
    根路径 - 系统欢迎信息
    """
    return JSONResponse({
        "name": config.PROJECT_NAME,
        "version": config.VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    })


@app.get("/health", tags=["System"])
async def health_check():
    """
    健康检查端点
    """
    from queue.task_queue import task_queue
    from services.monitor import monitor_service

    return JSONResponse({
        "status": "healthy",
        "project": config.PROJECT_NAME,
        "version": config.VERSION,
        "queue_mode": "redis" if task_queue.redis_available else "memory",
        "queue_length": task_queue.queue_len(),
        "timestamp": __import__("datetime").datetime.now().isoformat()
    })


# 直接运行入口（开发环境）
if __name__ == "__main__":
    import uvicorn

    logger.info(f"🚀 启动 ContentHub v{config.VERSION}...")
    logger.info(f"📖 API文档: http://localhost:8000/docs")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
