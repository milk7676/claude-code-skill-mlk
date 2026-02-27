#!/usr/bin/env python3
import sys
import time
sys.path.insert(0, 'scripts')

from patchright.sync_api import sync_playwright

def test_browser():
    print("🌐 测试浏览器启动和网络连接...")
    print("=" * 50)

    with sync_playwright() as p:
        try:
            print("1️⃣ 启动 Chrome 浏览器...")
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            print("✅ 浏览器启动成功")

            print("\n2️⃣ 访问 Google 主页...")
            page.goto("https://www.google.com", timeout=30000)
            print("✅ Google 主页加载成功")

            print("\n3️⃣ 访问 NotebookLM...")
            try:
                page.goto("https://notebooklm.google.com", timeout=60000)
                current_url = page.url
                print(f"✅ NotebookLM 加载成功")
                print(f"   当前 URL: {current_url}")

                # 等待 5 秒让用户看到
                print("\n⏸️  等待 5 秒，请观察浏览器页面...")
                time.sleep(5)

            except Exception as e:
                print(f"❌ NotebookLM 加载失败: {e}")

            browser.close()
            print("\n✅ 测试完成")

        except Exception as e:
            print(f"❌ 错误: {e}")

if __name__ == "__main__":
    test_browser()
