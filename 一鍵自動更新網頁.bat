@echo off
chcp 65001 >nul
echo =========================================
echo       ⚾ 二沼為您準備的一鍵更新腳本 ⚾
echo =========================================
echo.

:: 切換到專案的絕對路徑
cd /d "c:\Users\Admir\Desktop\Project\Hurricane Knight"

echo [1/3] 正在將新檔案加入版本控制 (git add)...
git add .

echo [2/3] 正在提交變更 (git commit)...
:: 取得當前日期時間作為 commit 訊息
set cur_date=%date:~0,10% %time:~0,8%
git commit -m "Auto-update website: %cur_date%"

echo [3/3] 正在上傳至 GitHub (git push)...
git push origin main

echo.
echo =========================================
echo  ✅ 網頁已成功推播至 GitHub！
echo  請等待約 1~3 分鐘，GitHub Pages 就會自動更新囉！
echo =========================================
pause
