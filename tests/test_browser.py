# test_browser.py
import asyncio
from playwright.async_api import async_playwright

async def test_browser_launch():
    """测试 Playwright 能否正常启动浏览器"""
    print("🚀 正在启动浏览器...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.baidu.com")
        title = await page.title()
        print(f"✅ 页面标题: {title}")
        await browser.close()
    print("✅ 浏览器测试通过！")

if __name__ == "__main__":
    asyncio.run(test_browser_launch())