@echo off
title Amazon Product Auto-Updater
cd /d "%~dp0"
echo.
echo ==========================================
echo   Amazon India - Product Auto-Updater
echo   Bestsellers fetch karke config update
echo ==========================================
echo.
pip install requests beautifulsoup4 -q
echo.
python product_updater.py
echo.
pause
