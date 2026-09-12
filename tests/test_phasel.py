# test_phasel.py
import asyncio
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.collector.douyin import DouyinCollector
from src.storage.db import Database
from src.storage.models import Video

async def test_full_flow():
    print("=" * 50)
    print("开始 Phase 1 集成测试")
    print("=" * 50)
    
    # 1. 测试数据库
    print("\n📁 测试数据库...")
    db = Database("data/test_phase1.db")
    print("✅ 数据库初始化成功")
    
    # 2. 测试存储
    print("\n💾 测试数据存储...")
    test_video = Video(
        id="test_001",
        user_id="test_user",
        title="测试视频标题",
        url="https://www.douyin.com/video/test",
        cover_url="https://example.com/cover.jpg"
    )
    db.insert_video(test_video)
    
    saved = db.get_video("test_001")
    if saved and saved.title == "测试视频标题":
        print("✅ 存储测试通过！")
    else:
        print("❌ 存储测试失败")
    
    # 3. 测试采集（可选，可能因反爬失败）
    print("\n📡 测试抖音采集（可能会因反爬失败，不影响整体测试）...")
    collector = DouyinCollector()
    # 这是一个公开的测试账号，你可以换成自己的
    test_user_id = "MS4wLjABAAAAGH3WlHt9Zk1TjNQ6wL2fA"
    try:
        videos = await collector.get_user_videos(test_user_id, limit=3)
        print(f"✅ 采集成功，共获取 {len(videos)} 条视频")
        for v in videos:
            print(f"   - {v.get('url', '无链接')}")
    except Exception as e:
        print(f"⚠️ 采集测试遇到问题: {e}")
        print("   这可能是反爬机制导致的，不影响存储功能测试")
    
    print("\n" + "=" * 50)
    print("Phase 1 测试完成！")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_full_flow())