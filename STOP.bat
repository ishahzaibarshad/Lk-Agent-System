@echo off
title NSOL BPO System - Stopping...
color 0C

echo ========================================
echo  NSOL BPO AI Call Assistant
echo  Stopping System...
echo ========================================
echo.

echo [1/2] Stopping Python processes...
taskkill /F /IM python.exe /T 2>nul
if %errorlevel% equ 0 (
    echo [OK] Python processes stopped
) else (
    echo [INFO] No Python processes found
)

echo.
echo [2/2] Stopping Ngrok...
taskkill /F /IM ngrok.exe /T 2>nul
if %errorlevel% equ 0 (
    echo [OK] Ngrok stopped
) else (
    echo [INFO] No Ngrok processes found
)

echo.
echo ========================================
echo  System Stopped Successfully!
echo ========================================
echo.
pause
