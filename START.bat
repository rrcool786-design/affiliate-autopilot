@echo off
title Affiliate Autopilot v3.0 - Telegram
cd /d "%~dp0"
echo.
echo ============================================
echo   AFFILIATE AUTOPILOT v3.0 - TELEGRAM
echo ============================================
echo   Channel  : @TechDealsIndia_channel
echo   Posts    : 3x/day (08:00, 13:00, 19:00)
echo   Report   : Daily at 22:00
echo ============================================
echo.
pip install openai schedule requests -q
echo.
python autopilot.py
pause
