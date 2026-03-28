"""
ContentHub 分发执行服务
支持单平台发布、批量发布、模拟发帖
"""
import os
import logging
import time
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

import config

logger = logging.getLogger(__name__)


class DistributeService:
    """分发执行服务类"""

    # 平台发布状态码
    STATUS_CODES = {
        "pending": "待发布",
        "publishing": "发布中",
        "success": "发布成功",
        "failed": "发布失败",
        "simulated": "模拟发布成功"
    }

    def __init__(self):
        self.publish_history: List[Dict[str, Any]] = []

    def publish(self, platform: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        单平台发布

        Args:
            platform: 目标平台
            data: 发布数据 {title, content, image_path, tags}

        Returns:
            Dict: 发布结果
        """
        if platform not in config.SUPPORT_PLATFORMS:
            return {
                "status": "failed",
                "platform": platform,
                "message": f"不支持的平台: {platform}",
                "timestamp": datetime.now().isoformat()
            }

        try:
            logger.info(f"开始发布到 {platform}...")

            # 模拟发布过程
            time.sleep(0.5)

            # 调用对应的平台API（实际接入时替换为真实API）
            result = self._call_platform_api(platform, data)

            # 记录历史
            record = {
                "id": str(uuid.uuid4()),
                "platform": platform,
                "title": data.get("title", ""),
                "status": result["status"],
                "message": result.get("message", ""),
                "post_id": result.get("post_id", ""),
                "url": result.get("url", ""),
                "timestamp": datetime.now().isoformat()
            }
            self.publish_history.append(record)

            return record

        except Exception as e:
            logger.error(f"发布失败 [{platform}]: {e}")
            return {
                "status": "failed",
                "platform": platform,
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _call_platform_api(self, platform: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用平台API（模拟实现）

        Args:
            platform: 平台名称
            data: 发布数据

        Returns:
            Dict: API响应
        """
        # 模拟API响应
        post_id = f"{platform}_{int(time.time())}"

        api_responses = {
            "xiaohongshu": {
                "status": "success",
                "post_id": post_id,
                "url": f"https://www.xiaohongshu.com/explore/{post_id}",
                "message": "发布成功"
            },
            "douyin": {
                "status": "success",
                "post_id": post_id,
                "url": f"https://www.douyin.com/video/{post_id}",
                "message": "发布成功"
            },
            "wechat": {
                "status": "success",
                "post_id": post_id,
                "url": f"https://mp.weixin.qq.com/s/{post_id}",
                "message": "发布成功"
            },
            "website": {
                "status": "success",
                "post_id": post_id,
                "url": f"https://example.com/posts/{post_id}",
                "message": "发布成功"
            }
        }

        return api_responses.get(platform, {
            "status": "failed",
            "message": "未知平台"
        })

    def batch_publish(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        批量发布到多个平台

        Args:
            task_data: 任务数据
                {
                    "title": str,
                    "content": str,
                    "image_path": str,
                    "platforms": List[str],
                    "tags": List[str]
                }

        Returns:
            Dict: 批量发布结果
        """
        platforms = task_data.get("platforms", config.SUPPORT_PLATFORMS)
        results = {}
        success_count = 0
        failed_count = 0

        for platform in platforms:
            result = self.publish(platform, {
                "title": task_data.get("title", ""),
                "content": task_data.get("content", ""),
                "image_path": task_data.get("image_path", ""),
                "tags": task_data.get("tags", [])
            })
            results[platform] = result

            if result["status"] == "success":
                success_count += 1
            else:
                failed_count += 1

            # 避免请求过快
            time.sleep(0.3)

        return {
            "status": "completed",
            "total": len(platforms),
            "success": success_count,
            "failed": failed_count,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }

    def simulate_post(self, platform: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        模拟发帖（API未接入时使用）

        Args:
            platform: 目标平台
            content: 发帖内容

        Returns:
            Dict: 模拟结果
        """
        if platform not in config.SUPPORT_PLATFORMS:
            return {
                "status": "failed",
                "platform": platform,
                "message": f"不支持的平台: {platform}",
                "timestamp": datetime.now().isoformat()
            }

        logger.info(f"模拟发布到 {platform}...")

        post_id = f"sim_{platform}_{int(time.time())}"

        result = {
            "status": "simulated",
            "platform": platform,
            "post_id": post_id,
            "title": content.get("title", ""),
            "message": "模拟发布成功（API未接入）",
            "simulated_url": f"https://{platform}.example.com/simulated/{post_id}",
            "timestamp": datetime.now().isoformat()
        }

        # 记录历史
        record = {
            "id": str(uuid.uuid4()),
            "platform": platform,
            "title": content.get("title", ""),
            "status": "simulated",
            "message": result["message"],
            "post_id": post_id,
            "url": result.get("simulated_url", ""),
            "timestamp": datetime.now().isoformat()
        }
        self.publish_history.append(record)

        return result

    def get_publish_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        获取发布历史

        Args:
            limit: 返回记录数量

        Returns:
            List[Dict]: 发布历史记录
        """
        return self.publish_history[-limit:]

    def get_platform_status(self, platform: str) -> Dict[str, Any]:
        """
        获取平台状态

        Args:
            platform: 平台名称

        Returns:
            Dict: 平台状态信息
        """
        platform_history = [h for h in self.publish_history if h["platform"] == platform]

        return {
            "platform": platform,
            "total_posts": len(platform_history),
            "success_count": len([h for h in platform_history if h["status"] == "success"]),
            "failed_count": len([h for h in platform_history if h["status"] == "failed"]),
            "simulated_count": len([h for h in platform_history if h["status"] == "simulated"]),
            "last_post": platform_history[-1] if platform_history else None
        }


# 全局服务实例
distribute_service = DistributeService()
