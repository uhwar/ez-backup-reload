@echo off
REM BackUp-Interface - Ez Backup Reload GUI Launcher
REM Batch script to launch the Electron frontend

title Ez Backup Reload - Interface Launcher
color 0D

echo.
echo  ==========================================
echo    Ez Backup Reload - Interface Launcher  
echo  ==========================================
echo.

REM Check if we're in the right directory
if not exist "backup_saves.py" (
    echo [ERROR] Please run this script from the ez-backup-reload directory
    echo         Missing backup_saves.py file
    echo.
    pause
    exit /b 1
)

REM Check if UI directory exists
if not exist "ui" (
    echo [ERROR] UI directory not found
    echo         The Electron frontend may not be installed
    echo.
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js first.
    echo         Download from: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

REM Check if Python is available
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python first.
    echo.
    pause
    exit /b 1
)

echo [INFO] Dependencies check passed
echo.

REM Navigate to UI directory
cd ui

REM Check if node_modules exists, install if not
if not exist "node_modules" (
    echo [INFO] Installing dependencies...
    echo.
    npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [INFO] Dependencies installed successfully
    echo.
)

echo [INFO] Launching Ez Backup Reload GUI...
echo        Close this window to exit the application
echo.

REM Launch the Electron app
npm start

REM Return to parent directory when done
cd ..

echo.
echo [INFO] Application closed
pause