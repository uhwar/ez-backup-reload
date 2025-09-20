# Ez Backup Reload - GUI Launcher
# PowerShell script to launch the Electron frontend

Write-Host "Ez Backup Reload - GUI Launcher" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is available
try {
    $nodeVersion = node --version 2>$null
    Write-Host "Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Node.js not found. Please install Node.js first." -ForegroundColor Red
    Write-Host "Download from: https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Python is available
try {
    $pythonVersion = py --version 2>$null
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found. Please install Python first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "backup_saves.py")) {
    Write-Host "Error: Please run this script from the ez-backup-reload directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Navigate to UI directory
if (-not (Test-Path "ui")) {
    Write-Host "Error: UI directory not found" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Set-Location "ui"

# Check if node_modules exists, install if not
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error installing dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "Launching Ez Backup Reload GUI..." -ForegroundColor Green
Write-Host ""

# Launch the Electron app
npm start