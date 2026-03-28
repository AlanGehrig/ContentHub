"""
ContentHub API 路由模块
提供素材上传、任务分发、状态查询等接口
"""
import os
import logging
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import config
from services.image_process import image_service
from services.ai_adapter import ai_service
from services.distribute import distribute_service
from services.monitor import monitor_service
from queue.task_queue import task_queue

logger = logging.getLogger(__name__)

router = APIRouter()


# ============== Pydantic 模型 ==============

class TaskCreateRequest(BaseModel):
    """任务创建请求"""
    title: str
    content: str
    platforms: List[str]
    tags: Optional[List[str]] = None


class TaskResponse(BaseModel):
    """任务响应"""
    task_id: str
    status: str
    message: str


class PlatformPublishRequest(BaseModel):
    """平台发布请求"""
    platform: str
    title: str
    content: str
    image_path: Optional[str] = None
    tags: Optional[List[str]] = None


class StatsResponse(BaseModel):
    """统计响应"""
    platform: str
    data: dict


# ============== 路由定义 ==============

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    title: str = Form(...),
    content: str = Form(""),
    platforms: str = Form("")  # 逗号分隔的平台列表
):
    """
    上传素材并创建分发任务

    Args:
        file: 上传的文件（图片）
        title: 内容标题
        content: 内容正文
        platforms: 目标平台（逗号分隔）

    Returns:
        JSON: 任务创建结果
    """
    try:
        # 验证文件类型
        allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"不支持的文件类型: {file.content_type}")

        # 保存上传文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(config.UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            content_bytes = await file.read()
            if len(content_bytes) > config.MAX_UPLOAD_SIZE:
                raise HTTPException(status_code=400, detail="文件大小超过50MB限制")
            f.write(content_bytes)

        # 解析平台列表
        platform_list = [p.strip() for p in platforms.split(",") if p.strip()] if platforms else config.SUPPORT_PLATFORMS

        # 创建任务
        task_data = {
            "title": title,
            "content": content,
            "image_path": file_path,
            "platforms": platform_list
        }

        # 添加到队列
        task_id = task_queue.add_task(task_data)

        # 更新任务状态
        monitor_service.update_task(task_id, "pending", {
            "title": title,
            "platforms": platform_list,
            "image_path": file_path
        })

        logger.info(f"任务创建成功: {task_id}")

        return JSONResponse({
            "code": 200,
            "message": "上传成功，任务已创建",
            "data": {
                "task_id": task_id,
                "file_path": file_path,
                "platforms": platform_list
            }
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"上传失败: {e}")
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")


@router.post("/upload/batch")
async def upload_batch(
    files: List[UploadFile] = File(...),
    title: str = Form(...),
    content: str = Form(""),
    platforms: str = Form("")
):
    """
    批量上传素材

    Args:
        files: 上传的文件列表
        title: 内容标题
        content: 内容正文
        platforms: 目标平台

    Returns:
        JSON: 批量上传结果
    """
    try:
        platform_list = [p.strip() for p in platforms.split(",") if p.strip()] if platforms else config.SUPPORT_PLATFORMS
        results = []

        for file in files:
            if file.content_type not in ["image/jpeg", "image/png", "image/gif", "image/webp"]:
                results.append({
                    "filename": file.filename,
                    "status": "failed",
                    "message": f"不支持的文件类型: {file.content_type}"
                })
                continue

            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{file.filename}"
                file_path = os.path.join(config.UPLOAD_DIR, filename)

                with open(file_path, "wb") as f:
                    content_bytes = await file.read()
                    if len(content_bytes) > config.MAX_UPLOAD_SIZE:
                        results.append({
                            "filename": file.filename,
                            "status": "failed",
                            "message": "文件大小超过限制"
                        })
                        continue
                    f.write(content_bytes)

                task_data = {
                    "title": title,
                    "content": content,
                    "image_path": file_path,
                    "platforms": platform_list
                }

                task_id = task_queue.add_task(task_data)
                monitor_service.update_task(task_id, "pending", {
                    "title": title,
                    "platforms": platform_list,
                    "image_path": file_path
                })

                results.append({
                    "filename": file.filename,
                    "status": "success",
                    "task_id": task_id,
                    "file_path": file_path
                })

            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "status": "failed",
                    "message": str(e)
                })

        return JSONResponse({
            "code": 200,
            "message": f"批量上传完成，成功 {sum(1 for r in results if r['status']=='success')} 个",
            "data": {
                "total": len(files),
                "success": sum(1 for r in results if r['status'] == 'success'),
                "failed": sum(1 for r in results if r['status'] == 'failed'),
                "results": results
            }
        })

    except Exception as e:
        logger.error(f"批量上传失败: {e}")
        raise HTTPException(status_code=500, detail=f"批量上传失败: {str(e)}")


@router.get("/run")
async def run_distribution():
    """
    执行分发任务
    从队列获取任务并分发到各平台

    Returns:
        JSON: 分发执行结果
    """
    try:
        task = task_queue.get_task()

        if not task:
            return JSONResponse({
                "code": 404,
                "message": "队列中没有待执行的任务",
                "data": None
            })

        task_id = task.get("task_id", "unknown")
        monitor_service.update_task(task_id, "publishing")

        # 执行批量发布
        result = distribute_service.batch_publish(task)

        # 更新任务状态
        monitor_service.update_task(task_id, "completed", {
            "result": result
        })

        return JSONResponse({
            "code": 200,
            "message": "分发执行完成",
            "data": {
                "task_id": task_id,
                "result": result
            }
        })

    except Exception as e:
        logger.error(f"分发执行失败: {e}")
        raise HTTPException(status_code=500, detail=f"分发执行失败: {str(e)}")


@router.get("/status")
async def get_status():
    """
    获取系统状态

    Returns:
        JSON: 系统状态信息
    """
    try:
        queue_length = task_queue.queue_len()
        task_summary = monitor_service.get_task_summary()

        # 获取队列中的任务预览
        pending_tasks = task_queue.peek_tasks(5)

        return JSONResponse({
            "code": 200,
            "message": "系统运行正常",
            "data": {
                "status": "running",
                "queue_length": queue_length,
                "redis_mode": task_queue.redis_available,
                "task_summary": task_summary,
                "pending_tasks": pending_tasks,
                "timestamp": datetime.now().isoformat()
            }
        })

    except Exception as e:
        logger.error(f"获取状态失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取状态失败: {str(e)}")


@router.get("/stats")
async def get_stats(platform: str = Query("all", description="平台名称: xiaohongshu/douyin/wechat/website/all")):
    """
    获取数据统计

    Args:
        platform: 平台名称

    Returns:
        JSON: 平台统计数据
    """
    try:
        stats = monitor_service.get_stats(platform)
        return JSONResponse({
            "code": 200,
            "message": "获取成功",
            "data": stats
        })

    except Exception as e:
        logger.error(f"获取统计失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取统计失败: {str(e)}")


@router.get("/stats/{platform}")
async def get_platform_stats(platform: str):
    """
    获取指定平台统计（路径参数版本）

    Args:
        platform: 平台名称

    Returns:
        JSON: 平台统计数据
    """
    return await get_stats(platform=platform)


@router.get("/tasks")
async def get_tasks(limit: int = Query(20, ge=1, le=100)):
    """
    获取任务列表

    Args:
        limit: 返回数量限制

    Returns:
        JSON: 任务列表
    """
    try:
        tasks = monitor_service.get_recent_tasks(limit)
        return JSONResponse({
            "code": 200,
            "message": "获取成功",
            "data": {
                "total": len(tasks),
                "tasks": tasks
            }
        })

    except Exception as e:
        logger.error(f"获取任务列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取任务列表失败: {str(e)}")


@router.get("/tasks/{task_id}")
async def get_task_detail(task_id: str):
    """
    获取任务详情

    Args:
        task_id: 任务ID

    Returns:
        JSON: 任务详情
    """
    try:
        task = monitor_service.track_task(task_id)

        if not task:
            raise HTTPException(status_code=404, detail=f"任务不存在: {task_id}")

        return JSONResponse({
            "code": 200,
            "message": "获取成功",
            "data": task
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取任务详情失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取任务详情失败: {str(e)}")


@router.get("/publish/history")
async def get_publish_history(limit: int = Query(50, ge=1, le=200)):
    """
    获取发布历史

    Args:
        limit: 返回数量限制

    Returns:
        JSON: 发布历史记录
    """
    try:
        history = distribute_service.get_publish_history(limit)
        return JSONResponse({
            "code": 200,
            "message": "获取成功",
            "data": {
                "total": len(history),
                "history": history
            }
        })

    except Exception as e:
        logger.error(f"获取发布历史失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取发布历史失败: {str(e)}")


@router.post("/publish/simulate")
async def simulate_publish(request: PlatformPublishRequest):
    """
    模拟发布（API未接入时使用）

    Args:
        request: 发布请求

    Returns:
        JSON: 模拟发布结果
    """
    try:
        result = distribute_service.simulate_post(request.platform, {
            "title": request.title,
            "content": request.content,
            "image_path": request.image_path,
            "tags": request.tags
        })

        return JSONResponse({
            "code": 200,
            "message": "模拟发布完成",
            "data": result
        })

    except Exception as e:
        logger.error(f"模拟发布失败: {e}")
        raise HTTPException(status_code=500, detail=f"模拟发布失败: {str(e)}")


@router.get("/platforms")
async def get_platforms():
    """
    获取支持的平台列表

    Returns:
        JSON: 平台列表
    """
    platforms_info = []
    for p in config.SUPPORT_PLATFORMS:
        style = ai_service.get_platform_style(p)
        platforms_info.append({
            "id": p,
            "name": style.get("tone", "").split("、")[0] if style else p,
            "style": style,
            "size": config.PLATFORM_SIZES.get(p)
        })

    return JSONResponse({
        "code": 200,
        "message": "获取成功",
        "data": {
            "platforms": platforms_info,
            "default": config.SUPPORT_PLATFORMS
        }
    })


@router.post("/image/process")
async def process_image(
    file: UploadFile = File(...),
    platform: str = Form(...),
    mode: str = Form("adapt")  # adapt: 尺寸适配, cover: 封面生成
):
    """
    图像处理接口

    Args:
        file: 上传的图片
        platform: 目标平台
        mode: 处理模式 (adapt/cover)

    Returns:
        JSON: 处理结果
    """
    try:
        if platform not in config.PLATFORM_SIZES:
            raise HTTPException(status_code=400, detail=f"不支持的平台: {platform}")

        # 保存临时文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(config.UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            content_bytes = await file.read()
            if len(content_bytes) > config.MAX_UPLOAD_SIZE:
                raise HTTPException(status_code=400, detail="文件大小超过限制")
            f.write(content_bytes)

        # 处理图像
        if mode == "cover":
            result_path = image_service.auto_cover(file_path, platform)
        else:
            result_path = image_service.auto_adapt_size(file_path, platform)

        if not result_path:
            raise HTTPException(status_code=500, detail="图像处理失败")

        return JSONResponse({
            "code": 200,
            "message": "处理成功",
            "data": {
                "original_path": file_path,
                "processed_path": result_path,
                "platform": platform,
                "mode": mode
            }
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"图像处理失败: {e}")
        raise HTTPException(status_code=500, detail=f"图像处理失败: {str(e)}")


@router.get("/ai/title")
async def generate_title(
    original: str = Query(..., description="原始标题"),
    platform: str = Query(..., description="目标平台")
):
    """
    生成平台专属标题

    Args:
        original: 原始标题
        platform: 目标平台

    Returns:
        JSON: 生成的标题
    """
    try:
        title = ai_service.generate_title(original, platform)
        return JSONResponse({
            "code": 200,
            "message": "生成成功",
            "data": {
                "original": original,
                "generated": title,
                "platform": platform
            }
        })

    except Exception as e:
        logger.error(f"标题生成失败: {e}")
        raise HTTPException(status_code=500, detail=f"标题生成失败: {str(e)}")


@router.get("/ai/tags")
async def generate_tags(
    platform: str = Query(..., description="目标平台"),
    count: int = Query(5, ge=1, le=20, description="标签数量")
):
    """
    生成平台专属标签

    Args:
        platform: 目标平台
        count: 标签数量

    Returns:
        JSON: 生成的标签列表
    """
    try:
        tags = ai_service.generate_tags(platform, count)
        return JSONResponse({
            "code": 200,
            "message": "生成成功",
            "data": {
                "platform": platform,
                "tags": tags
            }
        })

    except Exception as e:
        logger.error(f"标签生成失败: {e}")
        raise HTTPException(status_code=500, detail=f"标签生成失败: {str(e)}")


@router.post("/ai/content")
async def generate_content(request: TaskCreateRequest):
    """
    生成平台专属文案

    Args:
        request: 文案生成请求

    Returns:
        JSON: 生成的文案
    """
    try:
        results = {}
        for platform in request.platforms:
            content = ai_service.generate_content(
                request.title,
                request.content,
                platform
            )
            results[platform] = content

        return JSONResponse({
            "code": 200,
            "message": "生成成功",
            "data": {
                "title": request.title,
                "platforms": request.platforms,
                "contents": results
            }
        })

    except Exception as e:
        logger.error(f"文案生成失败: {e}")
        raise HTTPException(status_code=500, detail=f"文案生成失败: {str(e)}")
