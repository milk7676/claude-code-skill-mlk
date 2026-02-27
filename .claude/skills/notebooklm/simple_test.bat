@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo            简单测试 - 手动验证
echo ============================================
echo.
echo 请手动在浏览器中打开以下链接：
echo.
echo https://notebooklm.google.com/notebook/256b0760-a92f-4fd0-9d84-9a1cd0ace822
echo.
echo ============================================
echo.
echo 如果你能看到你的笔记本内容，说明：
echo 1. 网络连接正常
echo 2. 认证成功
echo 3. 笔记本可访问
echo.
echo 那么我们可以直接在 Claude Code 中使用！
echo ============================================
echo.
echo 按任意键关闭窗口...
pause >nul
