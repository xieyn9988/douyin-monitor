# test_douyin.py
import asyncio
from playwright.async_api import async_playwright

async def test_douyin_access():
    """测试能否访问抖音页面"""
    print("🚀 正在访问抖音...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 尝试访问一个公开的抖音用户主页（替换成一个存在的用户ID）
        # 注意：抖音可能会重定向或要求登录，这是正常的
        await page.goto("https://www.douyin.com/user/MS4wLjABAAAAAGH3WlHt9Zk1TjNQ6wL2fA")
        await page.wait_for_timeout(3000)  # 等待3秒看页面加载情况
        
        # 截图保存，方便查看
        await page.screenshot(path="test_douyin_page.png")
        print("✅ 抖音页面访问完成，截图已保存为 test_douyin_page.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_douyin_access())