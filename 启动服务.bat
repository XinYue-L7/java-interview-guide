@echo off
chcp 65001 >nul
title Java面试宝典 - 本地服务
cd /d D:\AiWordSpace
echo ============================================
echo   Java面试宝典  本地服务启动中...
echo ============================================
echo.
echo   本机访问：http://localhost:9876/
echo   局域网访问：http://本机IP:9876/
echo.
echo   按 Ctrl+C 可停止服务
echo ============================================
echo.
python -m http.server 9876 --directory D:\AiWordSpace --bind 0.0.0.0
pause