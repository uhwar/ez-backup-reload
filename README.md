# Game Save Backup Utility

A Python utility that automatically locates and backs up game save files from various PC games to a local "loaded saves" directory.

## Features

- Scans PC for game save files across multiple game titles and platforms
- Supports common game save locations (Steam, Epic, GOG, Documents, AppData, etc.)
- Identifies save files by common patterns and file extensions
- Backs up saves to local "loaded saves" directory organized by game
- Handles multiple game titles and save formats
- Non-destructive operations - never modifies original saves

## Usage

### Electron GUI (Recommended)
```bash
# Navigate to UI directory and install dependencies (first time only)
cd ui
npm install

# Launch the GUI application
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