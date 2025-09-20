# Game Save Backup Utility

A Python utility that automatically locates and backs up game save files from various PC games to a local "loaded saves" directory.

## Features

- Scans PC for game save files across multiple game titles and platforms
- Supports common game save locations (Steam, Epic, GOG, Documents, AppData, etc.)
- Identifies save files by common patterns and file extensions
- Backs up saves to local "loaded saves" directory organized by game
- Handles multiple game titles and save formats
- Non-destructive operations - never modifies original saves

## Quick Start

### 🚀 Easy GUI Launch (Windows)
```batch
# Double-click or run from command line:
BackUp-Interface.bat
```

OR

```powershell
# Right-click and "Run with PowerShell":
.\launch_gui.ps1
```

## Setup Instructions

### First-Time Setup for GUI

1. **Install Node.js** (if not already installed)
   - Download from: https://nodejs.org/
   - Version 16+ required

2. **Install Python** (if not already installed)
   - Download from: https://python.org/
   - Version 3.x required

3. **Clone this repository**
   ```bash
   git clone https://github.com/uhwar/ez-backup-reload
   cd ez-backup-reload
   ```

4. **Install Electron dependencies**
   ```bash
   cd ui
   npm install
   ```

5. **Launch the GUI**
   ```bash
   # Option 1: Use launcher scripts (Windows)
   cd ..
   BackUp-Interface.bat
   
   # Option 2: Direct launch
   cd ui
   npm start
   ```

## Usage

### Electron GUI (Recommended)

The GUI provides a modern interface with:
- **Obsidian-inspired dark theme** with deep greys and purple accents
- **Frameless window** with custom controls
- **Four main tabs**: Scan, Backup, View Backups, View Logs
- **Real-time progress** tracking and status updates
- **Game filtering** capabilities
- **Monochrome emoji** design with JetBrains Mono font

**Launch Options:**
```bash
# Method 1: Batch script (easiest)
BackUp-Interface.bat

# Method 2: PowerShell script
.\launch_gui.ps1

# Method 3: Manual
cd ui
npm start
```

### Command Line Interface

#### Basic Usage
```bash
python backup_saves.py
```

### Scan Only (No Backup)
```bash
python backup_saves.py --scan-only
```

### Verbose Output
```bash
python backup_saves.py --verbose
```

### Backup Specific Game
```bash
python backup_saves.py --game "Skyrim"
```

## Directory Structure

```
backup_saves.py          # Main script - terminal launchable
game_scanner.py          # Core scanning logic for finding saves
save_patterns.py         # Database of game save locations and patterns
backup_manager.py        # Handles copying and organizing backups
config.py               # Configuration settings
ui/                     # Electron frontend application
  main.js               # Electron main process
  preload.js            # Secure context bridge
  index.html            # UI structure
  styles.css            # Obsidian-inspired dark theme
  renderer.js           # Frontend logic
  package.json          # Node.js dependencies
loaded saves/           # Local backup storage directory
  [Game Name]/          # Organized by game
    YYYY-MM-DD_HH-MM-SS/  # Timestamped backup folders
logs/                   # Backup operation logs
tests/                  # Unit tests
docs/                   # Documentation and game save research
```

## Supported Games

The utility includes patterns for popular games including:
- The Witcher 3: Wild Hunt
- Skyrim / Skyrim Special Edition
- Fallout 4
- Cyberpunk 2077
- Stardew Valley
- Terraria
- And many more...

## Requirements

### For GUI (Electron)
- Node.js 16+ and npm
- Python 3.x (for backend operations)

### For CLI only
- Python 3.x
- Standard library only (no external dependencies)

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m unittest tests.test_backup
```

## Troubleshooting

### GUI won't launch
- **Node.js not found**: Install Node.js from https://nodejs.org/
- **Python not found**: Install Python from https://python.org/
- **Dependencies missing**: Run `npm install` in the `ui/` directory
- **Permission errors**: Run PowerShell as Administrator

### Common Issues
- **"electron not found"**: Delete `ui/node_modules/` and run `npm install` again
- **White screen**: Dependencies may be corrupted, try reinstalling with `npm install`
- **Python script fails**: Ensure Python is in your PATH and accessible via `py` command

### Getting Help
- Check the [Issues](https://github.com/uhwar/ez-backup-reload/issues) page
- Run with `--verbose` flag for detailed output
- Check the `logs/` directory for backup operation details
