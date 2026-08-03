@echo off
cd /d "F:\Cloud All Work\Auto pailet"
echo ==========================================
echo   Telegram Connection + Test Post
echo ==========================================
echo.
pip install requests -q
echo.
python test_telegram.py
