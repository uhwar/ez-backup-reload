# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Game Save Backup Utility that automatically scans for and backs up PC game save files. The system consists of:
- **Python backend** - Core scanning and backup logic
- **Electron frontend** - Modern GUI interface with Obsidian-inspired dark theme

The utility intelligently locates save files across different gaming platforms (Steam, Epic, GOG) and organizes backups in a "loaded saves" directory with timestamp-based folders.

## Core Architecture

The codebase follows a modular design with clear separation of concerns:

- **`backup_saves.py`** - Main entry point and CLI interface
- **`game_scanner.py`** - Core scanning engine that finds save files using both known patterns and heuristic detection
- **`save_patterns.py`** - Knowledge base of specific game save locations and file patterns
- **`backup_manager.py`** - Handles copying, organizing, and logging backup operations
- **`config.py`** - Centralized configuration including scan locations, exclusion lists, and directory structure

### Backend Architecture
The Python backend operates in two phases:
1. **Known Pattern Matching**: Scans predefined locations for recognized games
2. **Heuristic Discovery**: Searches common locations for unknown games using file extension and naming patterns

### Frontend Architecture  
The Electron frontend (`ui/` directory) provides a modern GUI:
- **`main.js`** - Main process with secure IPC handlers that spawn Python processes
- **`preload.js`** - Context bridge exposing limited APIs to renderer
- **`index.html`** + **`styles.css`** + **`renderer.js`** - Obsidian-inspired dark UI
- **IPC Communication** - Secure message passing between processes without exposing Node.js APIs

## Common Development Commands

### Running the Python CLI
```bash
# Basic backup (all games)
python backup_saves.py

# Scan only (no backup)
python backup_saves.py --scan-only

# Verbose output
python backup_saves.py --verbose

# Backup specific game
python backup_saves.py --game "Skyrim"
```

### Running the Electron GUI
```bash
# Install dependencies (first time)
cd ui
npm install

# Start the GUI application
npm start

# Development mode with DevTools
set NODE_ENV=development && npm start
```


### Windows Convenience Scripts
```bash
# Interactive PowerShell menu
.\run_backup.ps1

# Quick verbose backup
.\quick_backup.bat
```

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m unittest tests.test_backup

# Run tests with verbose output
python -m unittest tests.test_backup -v
```

### Development Workflow
```bash
# Test changes without actual backup
python backup_saves.py --scan-only --verbose

# Run single game test
python backup_saves.py --game "TestGame" --verbose
```

## Key Design Patterns

### Game Detection Strategy
The scanner employs a multi-layered approach:
1. **Explicit patterns** from `save_patterns.py` for known games
2. **Heuristic detection** using file extensions (`.sav`, `.save`, `.dat`, etc.)
3. **Exclusion filtering** to avoid non-game applications and online-only games
4. **Confidence scoring** based on file count and naming patterns

### Directory Structure Preservation
The backup system preserves relative path structure within game folders, using `_get_relative_save_path()` to maintain meaningful directory hierarchies in backups.

### Logging and Metadata
All backup operations generate JSON logs in the `logs/` directory containing:
- Timestamp and operation metadata
- File-by-file backup details
- Error tracking
- Source and destination paths

## Configuration Areas

### Adding New Games
Update `save_patterns.py` with new game entries:
```python
self.game_patterns = {
    "New Game": [
        self.user_profile / "Documents" / "NewGame" / "Saves",
        self.appdata / "NewGameStudio" / "NewGame" / "SaveData"
    ],
}
```

### Exclusion Lists
Modify `config.py` for:
- **`excluded_apps`**: Non-game applications to skip
- **`excluded_online_games`**: Online/MMO games with server-side saves
- **`gaming_platforms`**: Known gaming platforms to always include

### File Pattern Recognition
Extend `save_patterns.py` methods:
- **`is_likely_save_file()`**: File extension and naming pattern detection
- **`_is_excluded_file()`**: Files to exclude from save detection

## Environment Considerations

This project is designed for Windows environments and uses Windows-specific paths:
- `%USERPROFILE%` for Documents folder
- `%APPDATA%` and `%LOCALAPPDATA%` for application data
- PowerShell scripts for Windows automation

The utility handles Windows permission errors gracefully and includes Windows-specific gaming platform detection.

## Testing Strategy

Tests focus on core backup functionality using temporary directories and mocked file systems. When adding new features:
1. Create test save files in temporary locations
2. Mock the `Config` object for isolated testing
3. Verify directory structure preservation
4. Test error handling for permission issues

## File Organization

The backup output follows this structure:
```
loaded saves/
  [Game Name]/
    YYYY-MM-DD_HH-MM-SS/
      [preserved save file structure]
```

This timestamp-based approach allows multiple backup versions while maintaining clear organization by game title.