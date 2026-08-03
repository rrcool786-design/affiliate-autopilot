@echo off
title Affiliate Autopilot v3.0 - FULL AUTO - Telegram
cd /d "%~dp0"
echo.
echo ============================================
echo   AFFILIATE AUTOPILOT v3.0 - FULL AUTO
echo ============================================
echo   Channel  : @TechDealsIndia_channel
echo   Posts    : 10x/day automatic
echo   Report   : Daily at 22:00
echo ============================================
echo.
pip install openai schedule requests -q
echo.
echo 2 | python autopilot.py
pause
