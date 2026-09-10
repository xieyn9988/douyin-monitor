#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
抖音热点监控 Agent - 主入口
用途：当运行 python main.py 时，启动一个完整的采集-处理-存储流程
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

# 初始化日志记录器
logger = get_logger(__name__)


async def run_collector():
    """
    核心流程：采集 -> 存储 -> 记录日志
    这是整个 Agent 最核心的"采集-存储"链路
    """
    print("\n" + "=" * 60)
    print("🎬 抖音热点监控 Agent 启动")
    print("=" * 60 + "\n")

    # 1. 初始化数据库
    logger.info("📁 正在连接数据库...")
    db = Database("data/videos.db")
    logger.info("✅ 数据库连接成功")

    # 2. 配置要监控的抖音用户 ID
    # 注意：这里的 user_id 是抖音用户的唯一标识，需要替换成实际要监控的账号
    # 可以从抖音分享链接中获取，例如：https://www.douyin.com/user/MS4wLjABAAAA...
    TARGET_USERS = [
        "MS4wLjABAAAAAGH3WlHt9Zk1TjNQ6wL2fA",  # 示例用户1（请替换为真实ID）
        # "MS4wLjABAAAA...",  # 可以添加多个用户，每行一个
    ]

    # 3. 创建采集器
    collector = DouyinCollector()

    # 4. 遍历每个用户，进行采集
    for user_id in TARGET_USERS:
        print(f"\n📡 正在采集用户: {user_id}")
        logger.info(f"开始采集用户: {user_id}")

        try:
            # 调用采集模块，获取视频列表
            videos_data = await collector.get_user_videos(user_id, limit=5)
            logger.info(f"采集到 {len(videos_data)} 条视频")

            # 5. 将采集到的数据存入数据库
            for item in videos_data:
                # 从采集结果中提取视频ID（从URL中解析）
                video_id = item.get('url', '').split('/')[-1]
                if not video_id:
                    video_id = f"video_{hash(item.get('url', ''))}"

                # 创建 Video 对象
                video = Video(
                    id=video_id,
                    user_id=user_id,
                    title=item.get('title', '无标题'),
                    url=item.get('url', ''),
                    cover_url=item.get('cover_url', ''),
                    processed=False
                )

                # 存入数据库
                db.insert_video(video)
                logger.info(f"✅ 已存储视频: {video_id}")

            print(f"✅ 用户 {user_id} 采集完成，共存储 {len(videos_data)} 条视频")

        except Exception as e:
            # 如果某个用户采集失败，记录错误但不中断程序
            error_msg = f"采集用户 {user_id} 失败: {e}"
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            # 记录到任务日志
            db.log_task(f"collect_{user_id}", "failed", error_msg)

    # 6. 打印最终统计
    print("\n" + "=" * 60)
    print("📊 本次运行统计")
    print("=" * 60)
    all_videos = db.get_all_videos(limit=10)
    print(f"📦 数据库中现有视频总数: {len(all_videos)} 条")
    print("\n📋 最新 5 条记录:")
    for idx, v in enumerate(all_videos[:5], 1):
        print(f"  {idx}. {v.get('title', '无标题')[:30]}... ({v.get('created_at', '')})")
    
    print("\n✅ Agent 运行完成！")
    print("=" * 60)


def main():
    """程序入口"""
    try:
        asyncio.run(run_collector())
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户中断，程序已停止")
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
        logger.error(f"程序异常退出: {e}")


if __name__ == "__main__":
    main()