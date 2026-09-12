# src/collector/douyin.py
from playwright.async_api import async_playwright
import asyncio
import random

from src.utils.logger import get_logger

logger = get_logger(__name__)


class DouyinCollector:
    def __init__(self):
        self.user_agents = [
            # ... 你原来的 UA 列表 ...
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        ]
        # 浏览器相关对象（生命周期贯穿整个 collector）
        self.playwright = None
        self.browser = None
        self.context = None

    async def start(self):
        """启动浏览器（只调用一次）"""
        if self.context is not None:
            return  # 已经启动过

        logger.info("🚀 正在启动 Playwright 浏览器...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            user_agent=random.choice(self.user_agents),
            viewport={"width": 1920, "height": 1080},
        )
        logger.info("✅ 浏览器启动完成")

    async def stop(self):
        """关闭浏览器（只调用一次）"""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            logger.info("✅ 浏览器已关闭")
        except Exception as e:
            logger.error(f"关闭浏览器时出错: {e}")

    async def get_user_videos(self, user_id: str, limit: int = 10):
        """采集指定用户的最新视频（复用已启动的浏览器）"""
        # 兜底：如果还没启动，就先启动
        if self.context is None:
            await self.start()

        # ✅ 每次采集创建一个新 page，用完关 page，不关 context/browser
        page = await self.context.new_page()

        try:
            # 1. 访问用户主页
            logger.info(f"🌐 访问用户主页: {user_id}")
            await page.goto(
                f"https://www.douyin.com/user/{user_id}",
                timeout=30000,
                wait_until="domcontentloaded",
            )
            await page.wait_for_timeout(random.randint(2000, 4000))

            # ✅ 加这一行：截图
            await page.screenshot(path="docs/debug_page.png", full_page=True)

            # 2. 滚动加载更多
            for _ in range(3):
                await page.mouse.wheel(0, 800)
                await page.wait_for_timeout(1500)

            # 3. 提取视频链接和基本信息
            videos = await page.evaluate(
                """
                () => {
                    const items = document.querySelectorAll('[data-e2e="user-post-item"]');
                    return Array.from(items).slice(0, 10).map(el => ({
                        url: el.querySelector('a')?.href,
                        title: el.querySelector('[data-e2e="video-title"]')?.innerText,
                        cover_url: el.querySelector('img')?.src
                    }));
                }
                """
            )

            logger.info(f"✅ 采集到 {len(videos)} 条视频（用户 {user_id}）")
            return videos or []

        finally:
            # ✅ 只关 page，保留 context/browser 供下次复用
            await page.close()