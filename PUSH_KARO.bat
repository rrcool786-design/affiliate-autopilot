@echo off
title GitHub Push - Affiliate Autopilot
cd /d "%~dp0"
echo.
echo ==========================================
echo   GitHub pe Push
echo ==========================================
echo.
echo Pehli baar mein browser khulega - GitHub
echo mein login karke "Authorize" dabana.
echo Uske baad hamesha ke liye yaad rakh lega.
echo.
echo ------------------------------------------
echo Step 1: GitHub ke naye changes le raha hoon...
echo ------------------------------------------
git pull --rebase origin main
if %errorlevel% neq 0 (
    echo.
    echo PULL FAIL HUA. Aage nahi badh raha.
    echo Claude ko screenshot bhej dena.
    echo.
    pause
    exit /b 1
)

echo.
echo ------------------------------------------
echo Step 2: Push kar raha hoon...
echo ------------------------------------------
git push origin main
if %errorlevel% neq 0 (
    echo.
    echo PUSH FAIL HUA.
    echo.
    echo   *** --force KABHI MAT CHALANA ***
    echo   GitHub pe roz ka website update hai,
    echo   force se sab mit jayega.
    echo.
    echo Claude ko upar ka message dikha dena.
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   HO GAYA! Changes GitHub pe live hain.
echo ==========================================
echo.
git log --oneline -3
echo.
pause
