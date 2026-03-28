"""
ContentHub 任务队列模块
支持 Redis 队列，Redis 不可用时自动降级为内存队列
"""
import json
import logging
import uuid
from typing import Any, Dict, Optional, List
from datetime import datetime

import config

logger = logging.getLogger(__name__)


class TaskQueue:
    """
    任务队列类
    - 优先使用 Redis 作为队列后端
    - Redis 不可用时自动降级为内存队列
    """

    def __init__(self):
        self.redis_available = False
        self._redis_client = None
        self._memory_queue: List[Dict[str, Any]] = []
        self._try_connect_redis()

    def _try_connect_redis(self):
        """尝试连接 Redis，失败时降级为内存队列"""
        try:
            import redis
            self._redis_client = redis.Redis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                db=config.REDIS_DB,
                decode_responses=True,
                socket_connect_timeout=3
            )
            self._redis_client.ping()
            self.redis_available = True
            logger.info("TaskQueue 初始化完成：使用 Redis 后端")
        except Exception as e:
            self.redis_available = False
            self._redis_client = None
            logger.warning(f"Redis 连接失败，降级为内存队列: {e}")

    def _ensure_connection(self):
        """确保 Redis 连接可用，不可用则降级"""
        if self.redis_available and self._redis_client is not None:
            try:
                self._redis_client.ping()
            except Exception:
                self.redis_available = False
                self._redis_client = None
                logger.warning("Redis 连接丢失，降级为内存队列")

    def add_task(self, task_data: Dict[str, Any]) -> str:
        """
        添加任务到队列

        Args:
            task_data: 任务数据字典

        Returns:
            str: 任务ID
        """
        # 生成任务ID
        task_id = str(uuid.uuid4())
        task_data["task_id"] = task_id
        task_data["created_at"] = datetime.now().isoformat()
        task_data["status"] = "pending"

        self._ensure_connection()

        if self.redis_available and self._redis_client:
            try:
                self._redis_client.rpush("contenthub:tasks", json.dumps(task_data, ensure_ascii=False))
                logger.info(f"任务已添加 [Redis]: {task_id}")
            except Exception as e:
                logger.error(f"Redis 添加任务失败: {e}")
                self._memory_queue.append(task_data)
                logger.info(f"任务已添加 [Memory]: {task_id}")
        else:
            self._memory_queue.append(task_data)
            logger.info(f"任务已添加 [Memory]: {task_id}")

        return task_id

    def get_task(self) -> Optional[Dict[str, Any]]:
        """
        从队列获取任务（先进先出）

        Returns:
            Optional[Dict]: 任务数据字典，无任务时返回 None
        """
        self._ensure_connection()

        if self.redis_available and self._redis_client:
            try:
                data = self._redis_client.lpop("contenthub:tasks")
                if data:
                    task = json.loads(data)
                    logger.info(f"任务已取出 [Redis]: {task.get('task_id')}")
                    return task
            except Exception as e:
                logger.error(f"Redis 获取任务失败: {e}")

        # 内存队列
        if self._memory_queue:
            task = self._memory_queue.pop(0)
            logger.info(f"任务已取出 [Memory]: {task.get('task_id')}")
            return task

        return None

    def queue_len(self) -> int:
        """
        获取队列长度

        Returns:
            int: 队列中的任务数量
        """
        self._ensure_connection()

        if self.redis_available and self._redis_client:
            try:
                length = self._redis_client.llen("contenthub:tasks")
                return length
            except Exception as e:
                logger.error(f"Redis 获取队列长度失败: {e}")

        return len(self._memory_queue)

    def peek_tasks(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        查看队列中的任务（不取出）

        Args:
            count: 查看的任务数量

        Returns:
            List[Dict]: 任务列表
        """
        self._ensure_connection()

        if self.redis_available and self._redis_client:
            try:
                items = self._redis_client.lrange("contenthub:tasks", 0, count - 1)
                return [json.loads(item) for item in items]
            except Exception as e:
                logger.error(f"Redis 查看任务失败: {e}")

        return self._memory_queue[:count]

    def update_task_status(self, task_id: str, status: str, extra_data: Optional[Dict] = None) -> bool:
        """
        更新任务状态（仅内存队列支持，Redis 需要外部存储）

        Args:
            task_id: 任务ID
            status: 新状态
            extra_data: 额外数据

        Returns:
            bool: 是否更新成功
        """
        self._ensure_connection()

        if self.redis_available and self._redis_client:
            # Redis 模式下，需要外部状态存储，这里仅记录日志
            logger.info(f"任务状态更新 [Redis]: {task_id} -> {status}")
            return True

        # 内存队列模式
        for task in self._memory_queue:
            if task.get("task_id") == task_id:
                task["status"] = status
                if extra_data:
                    task.update(extra_data)
                logger.info(f"任务状态更新 [Memory]: {task_id} -> {status}")
                return True

        return False


# 全局队列实例
task_queue = TaskQueue()
