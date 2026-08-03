@echo off
title Commit 10x Upgrade to GitHub
cd /d "%~dp0"
color 0A

echo.
echo ╔══════════════════════════════════════════╗
echo ║   10x Website Upgrade — GitHub Push     ║
echo ╚══════════════════════════════════════════╝
echo.

:: Check git is available
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git not found! Download from: https://git-scm.com/download/win
    pause
    exit /b
)

echo [1/4] Generating latest website...
python generate_website.py
echo.

echo [2/4] Staging all changed files...
git add -A
echo.

echo [3/4] Committing...
git commit -m "10x Upgrade: 156 products, smart search, autocomplete, sort/filter, WhatsApp share — %date%"
echo.

echo [4/4] Pushing to GitHub...
git push origin main
echo.

echo ╔══════════════════════════════════════════╗
echo ║   ✅ DONE! Changes live in ~2 minutes   ║
echo ║   Site: rrcool786-design.github.io/     ║
echo ║         affiliate-autopilot/            ║
echo ╚══════════════════════════════════════════╝
echo.
pause
