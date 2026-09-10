# src/collector/douyin.py
from playwright.async_api import async_playwright
import asyncio
import random

class DouyinCollector:
    def __init__(self):
        self.user_agents = [...]  # 轮换UA
    
    async def get_user_videos(self, user_id: str, limit: int = 10):
        """采集指定用户的最新视频"""
        async with async_playwright() as p:
            # 1. 启动浏览器（使用stealth模式避免检测）
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=random.choice(self.user_agents),
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            # 2. 访问用户主页
            await page.goto(f'https://www.douyin.com/user/{user_id}')
            await page.wait_for_timeout(random.randint(2000, 4000))
            
            # 3. 滚动加载更多
            for _ in range(3):
                await page.mouse.wheel(0, 800)
                await page.wait_for_timeout(1500)
            
            # 4. 提取视频链接和基本信息
            videos = await page.evaluate('''
                () => {
                    const items = document.querySelectorAll('[data-e2e="user-post-item"]');
                    return Array.from(items).slice(0, 10).map(el => ({
                        url: el.querySelector('a')?.href,
                        title: el.querySelector('[data-e2e="video-title"]')?.innerText,
                        cover: el.querySelector('img')?.src
                    }));
                }
            ''')
            
            await browser.close()
            return videos