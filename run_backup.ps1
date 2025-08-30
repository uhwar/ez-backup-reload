# Game Save Backup Utility - PowerShell Launcher
# Right-click and "Run with PowerShell" or run from PowerShell terminal

Write-Host "Game Save Backup Utility" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

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
Write-Host "Choose an option:" -ForegroundColor Yellow
Write-Host "1. Scan for saves (no backup)"
Write-Host "2. Backup all saves"
Write-Host "3. Backup with verbose output"
Write-Host "4. Backup specific game"
Write-Host "5. View existing backups"
Write-Host ""

$choice = Read-Host "Enter your choice (1-5)"

switch ($choice) {
    "1" {
        Write-Host "Running scan-only mode..." -ForegroundColor Green
        py backup_saves.py --scan-only --verbose
    }
    "2" {
        Write-Host "Running backup..." -ForegroundColor Green
        py backup_saves.py
    }
    "3" {
        Write-Host "Running backup with verbose output..." -ForegroundColor Green
        py backup_saves.py --verbose
    }
    "4" {
        $gameName = Read-Host "Enter game name to backup"
        Write-Host "Running backup for '$gameName'..." -ForegroundColor Green
        py backup_saves.py --game "$gameName" --verbose
    }
    "5" {
        Write-Host "Checking for existing backups..." -ForegroundColor Green
        if (Test-Path "loaded saves") {
            Get-ChildItem "loaded saves" -Directory | ForEach-Object {
                $gameBackups = Get-ChildItem $_.FullName -Directory
                Write-Host "$($_.Name): $($gameBackups.Count) backup(s)" -ForegroundColor Cyan
                $gameBackups | ForEach-Object {
                    Write-Host "  - $($_.Name)" -ForegroundColor Gray
                }
            }
        } else {
            Write-Host "No backups found yet." -ForegroundColor Yellow
        }
    }
    default {
        Write-Host "Invalid choice. Running default backup..." -ForegroundColor Yellow
        py backup_saves.py
    }
}

Write-Host ""
Write-Host "Operation complete!" -ForegroundColor Green
Read-Host "Press Enter to exit"