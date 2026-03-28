"""
ContentHub 数据监控服务
获取各平台数据统计、追踪任务状态
"""
import logging
import time
import random
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MonitorService:
    """数据监控服务类"""

    def __init__(self):
        self._task_store: Dict[str, Dict[str, Any]] = {}
        self._stats_cache: Dict[str, Any] = {}
        self._cache_timeout = 60  # 缓存有效期（秒）

    def get_stats(self, platform: str) -> Dict[str, Any]:
        """
        获取平台数据统计

        Args:
            platform: 平台名称

        Returns:
            Dict: 平台统计数据
        """
        if platform not in ["xiaohongshu", "douyin", "wechat", "website", "all"]:
            logger.error(f"不支持的平台: {platform}")
            return {"error": f"不支持的平台: {platform}"}

        # 检查缓存
        cache_key = f"stats_{platform}"
        if cache_key in self._stats_cache:
            cached = self._stats_cache[cache_key]
            if time.time() - cached["timestamp"] < self._cache_timeout:
                return cached["data"]

        try:
            if platform == "all":
                # 汇总所有平台数据
                data = self._get_all_platform_stats()
            else:
                # 单平台数据（模拟）
                data = self._get_platform_stats(platform)

            # 更新缓存
            self._stats_cache[cache_key] = {
                "timestamp": time.time(),
                "data": data
            }

            return data

        except Exception as e:
            logger.error(f"获取统计数据失败 [{platform}]: {e}")
            return {"error": str(e)}

    def _get_platform_stats(self, platform: str) -> Dict[str, Any]:
        """
        获取单个平台统计数据（模拟实现）

        Args:
            platform: 平台名称

        Returns:
            Dict: 统计数据
        """
        # 模拟数据，实际应调用各平台API
        base_stats = {
            "xiaohongshu": {
                "platform": "xiaohongshu",
                "display_name": "小红书",
                "followers": 12580,
                "likes": 98650,
                "comments": 4520,
                "shares": 3210,
                "views": 456780,
                "engagement_rate": 2.35,
                "last_updated": datetime.now().isoformat()
            },
            "douyin": {
                "platform": "douyin",
                "display_name": "抖音",
                "followers": 45800,
                "likes": 325600,
                "comments": 18900,
                "shares": 25600,
                "views": 2567800,
                "engagement_rate": 1.89,
                "last_updated": datetime.now().isoformat()
            },
            "wechat": {
                "platform": "wechat",
                "display_name": "微信公众号",
                "subscribers": 8900,
                "read_count": 45600,
                "shares": 1230,
                "likes": 890,
                "avg_read_time": "3:45",
                "completion_rate": 68.5,
                "last_updated": datetime.now().isoformat()
            },
            "website": {
                "platform": "website",
                "display_name": "独立站",
                "visitors": 125600,
                "page_views": 356800,
                "avg_session_duration": "4:20",
                "bounce_rate": 42.3,
                "conversions": 1256,
                "conversion_rate": 1.0,
                "last_updated": datetime.now().isoformat()
            }
        }

        stats = base_stats.get(platform, base_stats["xiaohongshu"]).copy()

        # 添加一些随机波动模拟真实数据
        if platform == "xiaohongshu":
            stats["views"] += random.randint(-1000, 5000)
            stats["likes"] += random.randint(-100, 500)
        elif platform == "douyin":
            stats["views"] += random.randint(-5000, 20000)
            stats["likes"] += random.randint(-500, 2000)

        return stats

    def _get_all_platform_stats(self) -> Dict[str, Any]:
        """
        获取所有平台的汇总统计

        Returns:
            Dict: 汇总统计数据
        """
        platforms = ["xiaohongshu", "douyin", "wechat", "website"]
        all_stats = {p: self._get_platform_stats(p) for p in platforms}

        # 计算汇总
        total_views = sum(s.get("views", 0) for s in all_stats.values())
        total_likes = sum(s.get("likes", 0) for s in all_stats.values())
        total_followers = sum(s.get("followers", 0) for s in all_stats.values())

        return {
            "platforms": all_stats,
            "summary": {
                "total_views": total_views,
                "total_likes": total_likes,
                "total_followers": total_followers,
                "active_platforms": len(platforms),
                "last_updated": datetime.now().isoformat()
            }
        }

    def track_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        追踪任务状态

        Args:
            task_id: 任务ID

        Returns:
            Dict: 任务状态信息，不存在返回 None
        """
        return self._task_store.get(task_id)

    def update_task(self, task_id: str, status: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        更新任务状态

        Args:
            task_id: 任务ID
            status: 任务状态
            data: 额外数据
        """
        if task_id not in self._task_store:
            self._task_store[task_id] = {
                "task_id": task_id,
                "created_at": datetime.now().isoformat()
            }

        self._task_store[task_id]["status"] = status
        self._task_store[task_id]["updated_at"] = datetime.now().isoformat()

        if data:
            self._task_store[task_id].update(data)

        logger.info(f"任务状态更新: {task_id} -> {status}")

    def get_recent_tasks(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        获取最近的任务列表

        Args:
            limit: 返回数量限制

        Returns:
            List[Dict]: 任务列表
        """
        tasks = list(self._task_store.values())
        tasks.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return tasks[:limit]

    def get_task_summary(self) -> Dict[str, Any]:
        """
        获取任务统计摘要

        Returns:
            Dict: 任务统计摘要
        """
        tasks = list(self._task_store.values())

        status_counts = {}
        for task in tasks:
            status = task.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

        return {
            "total_tasks": len(tasks),
            "by_status": status_counts,
            "active_platforms": len(set(t.get("platform") for t in tasks if t.get("platform")))
        }

    def clear_old_tasks(self, days: int = 7) -> int:
        """
        清理旧任务记录

        Args:
            days: 保留天数

        Returns:
            int: 清理的任务数量
        """
        cutoff = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff.isoformat()

        to_remove = [
            task_id for task_id, task in self._task_store.items()
            if task.get("updated_at", "") < cutoff_str
        ]

        for task_id in to_remove:
            del self._task_store[task_id]

        logger.info(f"已清理 {len(to_remove)} 条旧任务记录")
        return len(to_remove)


# 全局服务实例
monitor_service = MonitorService()
