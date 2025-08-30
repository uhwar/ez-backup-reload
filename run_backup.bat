@echo off
REM Game Save Backup Utility - Windows Batch Launcher
REM Double-click this file to run the backup utility

echo Game Save Backup Utility
echo ========================
echo.

REM Check if Python is available
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found. Please install Python first.
    pause
    exit /b 1
)

echo Choose an option:
echo 1. Scan for saves (no backup)
echo 2. Backup all saves
echo 3. Backup with verbose output
echo 4. Backup specific game
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Running scan-only mode...
    py backup_saves.py --scan-only --verbose
) else if "%choice%"=="2" (
    echo Running backup...
    py backup_saves.py
) else if "%choice%"=="3" (
    echo Running backup with verbose output...
    py backup_saves.py --verbose
) else if "%choice%"=="4" (
    set /p gamename="Enter game name to backup: "
    echo Running backup for "%gamename%"...
    py backup_saves.py --game "%gamename%" --verbose
) else (
    echo Invalid choice. Running default backup...
    py backup_saves.py
)

echo.
echo Operation complete!
pause