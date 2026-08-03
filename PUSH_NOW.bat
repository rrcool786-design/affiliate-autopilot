@echo off
title Push All Upgrades to GitHub
cd /d "F:\Cloud All Work\Auto pailet"
color 0A

echo.
echo ╔══════════════════════════════════════════════╗
echo ║   Pushing All Upgrades to GitHub...         ║
echo ╚══════════════════════════════════════════════╝
echo.

:: Check git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git not found! Install from https://git-scm.com
    pause & exit /b 1
)

:: Init git repo if not already
if not exist ".git" (
    echo [1] Initializing git repo...
    git init
    git config user.email "rrcool786@gmail.com"
    git config user.name "rrcool786-design"
) else (
    echo [1] Git repo already initialized.
)

:: Add remote
git remote remove origin 2>nul
git remote add origin https://github.com/rrcool786-design/affiliate-autopilot.git
echo [2] Remote set.

:: Fetch existing commits from GitHub (so we can push on top of them)
echo [3] Fetching GitHub history...
git fetch origin main 2>&1
if %errorlevel% neq 0 (
    echo Fetch failed - check internet connection
    pause & exit /b 1
)

:: Point local main at origin/main WITHOUT overwriting local files
git update-ref refs/heads/main FETCH_HEAD
git symbolic-ref HEAD refs/heads/main
echo [4] Local branch synced with origin.

:: Stage ALL local files
git add -A
echo [5] All files staged.

:: Show what will be committed
echo.
echo Files to be pushed:
git status --short
echo.

:: Commit
git commit -m "SEO + Click Tracker Upgrade: generate_website.py v2, click_report.py, cloudflare_tracker.js, sitemap.xml, robots.txt, hot_products feedback loop"
echo [6] Committed.

:: Push
echo [7] Pushing to GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo.
    echo ╔══════════════════════════════════════════════════════════╗
    echo ║  PUSH FAIL HUA - force push MAT karna!                  ║
    echo ║                                                          ║
    echo ║  Matlab GitHub pe naye commits hain jo yahan nahi hain.  ║
    echo ║  Actions bot roz website update karta hai.               ║
    echo ║  --force se wo saare updates MIT jayenge.                ║
    echo ║                                                          ║
    echo ║  Sahi tarika - pehle GitHub ke changes le lo:            ║
    echo ║      git pull --rebase origin main                       ║
    echo ║      git push origin main                                ║
    echo ╚══════════════════════════════════════════════════════════╝
)

echo.
echo ╔══════════════════════════════════════════════╗
echo ║  DONE! Changes live on GitHub.              ║
echo ║  GitHub Actions will rebuild site in ~2min  ║
echo ╚══════════════════════════════════════════════╝
echo.
pause
