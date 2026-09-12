#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
抖音热点监控 Agent - 主入口
用途：当运行 python main.py 时，启动定时调度器，周期性采集抖音视频
"""

import asyncio
import sys
from pathlib import Path

# 将项目根目录添加到 Python 路径，以便能找到 src 模块
sys.path.insert(0, str(Path(__file__).parent))

# 导入项目的各个模块
from src.collector.douyin import DouyinCollector
from src.storage.db import Database
from src.storage.models import Video
from src.utils.logger import get_logger
from src.scheduler.tasks import TaskManager          # ✅ 新增：导入调度器

logger = get_logger(__name__)


# ============================================================
# 【保留】原有的一次性采集函数（手动运行 / 调试用）
# ============================================================
async def run_collector():
    """
    核心流程：采集 -> 存储 -> 记录日志
    一次性执行，采集完就退出（调试用）
    """
    print("\n" + "=" * 60)
    print("🎬 抖音热点监控 Agent 启动（一次性模式）")
    print("=" * 60 + "\n")

    db = Database("data/videos.db")
    logger.info("✅ 数据库连接成功")

    TARGET_USERS = [
        "MS4wLjABAAAAzzufDZVJO_X8I8YnKTd5m3YmRY2LI9CQ0VTqEqRLUY4",
    ]

    collector = DouyinCollector()

    for user_id in TARGET_USERS:
        print(f"\n📡 正在采集用户: {user_id}")
        logger.info(f"开始采集用户: {user_id}")

        try:
            videos_data = await collector.get_user_videos(user_id, limit=5)
            logger.info(f"采集到 {len(videos_data)} 条视频")

            for item in videos_data:
                video_id = item.get('url', '').split('/')[-1]
                if not video_id:
                    video_id = f"video_{hash(item.get('url', ''))}"

                video = Video(
                    id=video_id,
                    user_id=user_id,
                    title=item.get('title', '无标题'),
                    url=item.get('url', ''),
                    cover_url=item.get('cover_url', ''),
                    processed=False
                )
                db.insert_video(video)
                logger.info(f"✅ 已存储视频: {video_id}")

            print(f"✅ 用户 {user_id} 采集完成，共存储 {len(videos_data)} 条视频")

        except Exception as e:
            error_msg = f"采集用户 {user_id} 失败: {e}"
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            db.log_task(f"collect_{user_id}", "failed", error_msg)

    print("\n✅ Agent 一次性运行完成！")


# ============================================================
# ✅ 新增：常驻调度模式（定时采集，正式运行用）
# ============================================================
async def run_scheduler():
    """
    启动定时调度器，程序常驻运行
    每 2 小时自动采集一次指定账号的最新视频
    """
    print("\n" + "=" * 60)
    print("⏰ 抖音热点监控 Agent 启动（定时调度模式）")
    print("=" * 60 + "\n")

    # 配置要监控的抖音用户 ID（请替换为真实 ID）
    TARGET_USERS = [
        "MS4wLjABAAAAAGH3WlHt9Zk1TjNQ6wL2fA",
    ]

    # 创建调度器并启动
    tm = TaskManager()
    tm.schedule_monitor(TARGET_USERS)
    logger.info("✅ 定时调度器已启动，每 2 小时采集一次")
    print("✅ 定时调度器已启动，每 2 小时采集一次")
    print("💡 按 Ctrl+C 退出程序\n")

    # 保持程序常驻运行，否则 asyncio.run 会立即退出
    try:
        while True:
            await asyncio.sleep(3600)   # 每小时检查一次，避免 CPU 空转
    except KeyboardInterrupt:
        print("\n⏹️ 收到退出信号，正在清理资源......")
        tm.scheduler.shutdown()
      
        # ✅ 优雅关闭浏览器
        try:
            await tm.collector.stop()
        except Exception as e:
            logger.error(f"关闭浏览器失败: {e}")

        print("✅ 已安全退出")
        # 给 asyncio 一点时间清理
        await asyncio.sleep(1)


# ============================================================
# 【改动】主入口：改成启动调度器
# ============================================================
def main():
    """程序入口"""
    try:
        # ❌ 原来（一次性采集）：
        # asyncio.run(run_collector())

        # ✅ 现在（定时调度，常驻运行）：
        asyncio.run(run_scheduler())

        # 如果你只想调试一次性采集，把上面那行注释掉，
        # 改成下面这行：
        # asyncio.run(run_collector())

    except KeyboardInterrupt:
        print("\n\n⏹️ 用户中断，程序已停止")
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
        logger.error(f"程序异常退出: {e}")


if __name__ == "__main__":
    main()