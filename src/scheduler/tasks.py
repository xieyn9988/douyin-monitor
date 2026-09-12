# src/scheduler/tasks.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
from typing import Callable

from src.utils.logger import get_logger
from src.utils.alert import send_feishu_alert as send_alert
from src.storage.db import Database
from src.collector.douyin import DouyinCollector

logger = get_logger(__name__)


class TaskManager:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.max_retries = 3
        self.retry_delay = [60, 300, 900]  # 1分钟, 5分钟, 15分钟
        self.db = Database("data/videos.db")
        self.collector = DouyinCollector()      # ✅ 全局只创建一次 collector
        self._initial_task = None      # ✅ 保存首次任务的引用


    async def execute_with_retry(self, task_id: str, func: Callable, *args, **kwargs):
        """带指数退避的重试执行器"""
        for attempt in range(self.max_retries + 1):
            try:
                logger.info(f"Task {task_id} attempt {attempt + 1}")
                result = await func(*args, **kwargs)
                await self._log_task(task_id, 'success')
                return result
            except Exception as e:
                await self._log_task(task_id, 'failed', str(e))
                if attempt < self.max_retries:
                    delay = self.retry_delay[attempt]
                    logger.warning(f"Task {task_id} failed, retry in {delay}s")
                    await asyncio.sleep(delay)
                else:
                    send_alert(f"Task {task_id} failed after {self.max_retries} retries: {e}")
                    raise

    def schedule_monitor(self, user_ids: list):
        """每2小时监控一次指定抖音账号"""
        @self.scheduler.scheduled_job(
            trigger=CronTrigger(hour='*/2'),   # ⚠️ 测试用，正式改成 hour='*/2'
            id='monitor_douyin_users'
        )
        async def job():
            for user_id in user_ids:
                await self.execute_with_retry(
                    f'douyin_collect_{user_id}',
                    self._collect_user_videos,
                    user_id
                )

        self.scheduler.start()

        # ✅ 启动时立刻跑一次
        self._initial_task = asyncio.create_task(job())
        logger.info("⚡ 已触发首次采集任务（程序启动立即执行）")


    # ---------------- 采集方法（复用 self.collector）----------------
    async def _collect_user_videos(self, user_id: str):
        """采集指定抖音用户的视频，并写入数据库"""
        logger.info(f"开始采集用户: {user_id}")

        # ✅ 直接复用全局 collector，不再每次 new 新的
        videos_data = await self.collector.get_user_videos(user_id, limit=5)

        from src.storage.models import Video
        for item in videos_data:
            video_id = item.get('url', '').split('/')[-1] or f"video_{hash(item.get('url', ''))}"
            video = Video(
                id=video_id,
                user_id=user_id,
                title=item.get('title', '无标题'),
                url=item.get('url', ''),
                cover_url=item.get('cover_url', ''),
                processed=False
            )
            self.db.insert_video(video)

        logger.info(f"用户 {user_id} 采集完成，共 {len(videos_data)} 条")
        return videos_data

    # ---------------- 任务日志 ----------------
    async def _log_task(self, task_id: str, status: str, error_msg: str = ""):
        """记录任务执行日志到数据库"""
        try:
            self.db.log_task(task_id, status, error_msg)
        except Exception as e:
            logger.error(f"写入任务日志失败: {e}")