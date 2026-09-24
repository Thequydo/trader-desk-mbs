@echo off
title DAY CODE TRADER DESK LEN GITHUB / VERCEL
cd /d "%~dp0"
echo ========================================================
echo   HUONG DAN DAY CODE LEN GITHUB DE DEPLOY VERCEL
echo ========================================================
echo.
echo 1. Hay tao 1 repository moi tren GitHub: https://github.com/new
echo 2. Copy duong link repo (VD: https://github.com/tenban/trader-desk.git)
echo.
set /p REPO_URL="Dan duong link GitHub cua ban vao day roi go Enter: "

if "%REPO_URL%"=="" (
    echo [!] Ban chua nhap link GitHub!
    pause
    exit /b
)

git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
git branch -M main
echo.
echo [*] Dang day code len GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo [OK] DA DAY CODE LEN GITHUB THANH CONG!
    echo.
    echo Bay gio ban chi can vao https://vercel.com/new
    echo Chon repo nay va bam DEPLOY la co ngay link web cong khai!
    echo ========================================================
) else (
    echo.
    echo [!] Co loi khi push len GitHub. Vui long kiem tra dang nhap git hoac link repo.
)
pause
