@echo off
title Copying Affiliate Autopilot Files to F: Drive...
echo ============================================
echo  Affiliate Autopilot — F Drive mein Copy
echo ============================================
echo.

set "DEST=F:\Cloud All Work\auto polet"

echo Destination: %DEST%
echo.

REM Create destination folder if it doesn't exist
if not exist "%DEST%" (
    echo Folder nahi mila — bana raha hoon...
    mkdir "%DEST%"
)

echo Files copy ho rahi hain...
echo.

copy /Y "%~dp0autopilot.py"                  "%DEST%\autopilot.py"
copy /Y "%~dp0config.py"                     "%DEST%\config.py"
copy /Y "%~dp0START.bat"                     "%DEST%\START.bat"
copy /Y "%~dp0SETUP_GUIDE.md"                "%DEST%\SETUP_GUIDE.md"
copy /Y "%~dp0affiliate_content_generator.py" "%DEST%\affiliate_content_generator.py"
copy /Y "%~dp0affiliate_landing_page.html"   "%DEST%\affiliate_landing_page.html"

echo.
echo ============================================
echo  DONE! Sabhi files copy ho gayi:
echo  F:\Cloud All Work\auto polet\
echo ============================================
echo.
echo Ab START.bat double-click karo wahan se!
echo.
pause
