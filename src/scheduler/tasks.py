# src/scheduler/tasks.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
from typing import Callable
from src.utils.logger import get_logger
from src.utils.alert import send_alert

logger = get_logger(__name__)

class TaskManager:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.max_retries = 3
        self.retry_delay = [60, 300, 900]  # 1分钟, 5分钟, 15分钟
    
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
                    # 达到最大重试次数，发送告警
                    await send_alert(f"Task {task_id} failed after {self.max_retries} retries: {e}")
                    raise
    
    def schedule_monitor(self, user_ids: list):
        """每2小时监控一次指定抖音账号"""
        @self.scheduler.scheduled_job(
            trigger=CronTrigger(minute='*/120'),  # 每2小时
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