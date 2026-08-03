@echo off
title GitHub Upload — Affiliate Autopilot
cd /d "%~dp0"
echo.
echo ==========================================
echo   GitHub pe Upload — 24/7 Cloud Autopilot
echo ==========================================
echo.
echo Step 1: Git initialize kar raha hoon...
git init
git add post_once.py .github/
echo.
echo Step 2: Commit...
git commit -m "Affiliate Autopilot — 10x/day Telegram posts"
echo.
echo ==========================================
echo   Ab yeh steps manually karo:
echo.
echo   1. github.com pe jaao (browser mein)
echo   2. New repository banao: affiliate-autopilot
echo   3. Wahan jo commands dikhein woh copy karo
echo      (git remote add origin ... aur git push)
echo.
echo   4. Repository Settings > Secrets > Actions
echo      Teen secrets add karo (values apni config.py se lo):
echo        GROQ_API_KEY        = [apni Groq key]
echo        TELEGRAM_BOT_TOKEN  = [apna bot token]
echo        TELEGRAM_CHANNEL_ID = @TechDealsIndia_channel
echo.
echo   5. Actions tab mein jaao — sab automatic chalega!
echo ==========================================
echo.
pause
