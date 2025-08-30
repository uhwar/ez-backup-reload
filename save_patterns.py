"""
Database of game save locations and patterns
Contains knowledge base of where popular games store their save files
"""

from pathlib import Path
import os

class SavePatterns:
    def __init__(self):
        self.user_profile = Path(os.environ.get('USERPROFILE', ''))
        self.appdata = Path(os.environ.get('APPDATA', ''))
        self.localappdata = Path(os.environ.get('LOCALAPPDATA', ''))
        
        # Known game save patterns
        self.game_patterns = {
            # Steam games
            "The Witcher 3": [
                self.user_profile / "Documents" / "The Witcher 3" / "gamesaves",
            ],
            "Skyrim": [
                self.user_profile / "Documents" / "My Games" / "Skyrim" / "Saves",
            ],
            "Fallout 4": [
                self.user_profile / "Documents" / "My Games" / "Fallout4" / "Saves",
            ],
            "Cyberpunk 2077": [
                self.appdata / "CD Projekt Red" / "Cyberpunk 2077" / "UserData",
            ],
            
            # Epic Games
            "Fortnite": [
                self.localappdata / "FortniteGame" / "Saved",
            ],
            
            # GOG games
            "Baldur's Gate 3": [
                self.appdata / "Larian Studios" / "Baldur's Gate 3" / "PlayerProfiles",
            ],
            
            # Indie games
            "Stardew Valley": [
                self.appdata / "StardewValley" / "Saves",
            ],
            "Terraria": [
                self.user_profile / "Documents" / "My Games" / "Terraria" / "Players",
                self.user_profile / "Documents" / "My Games" / "Terraria" / "Worlds",
            ],
        }
    
    def get_patterns_for_game(self, game_name):
        """Get save patterns for a specific game"""
        return self.game_patterns.get(game_name, [])
    
    def get_all_patterns(self):
        """Get all known game save patterns"""
        return self.game_patterns
    
    def is_likely_save_file(self, file_path):
        """Check if a file is likely a save file based on extension and name"""
        file_path = Path(file_path)
        
        # Skip obviously non-save files
        if self._is_excluded_file(file_path):
            return False
        
        # Check extension
        save_extensions = {'.sav', '.save', '.dat', '.json', '.xml', '.cfg', '.ini', 
                          '.profile', '.plr', '.wld', '.ess', '.skse', '.fos'}
        if file_path.suffix.lower() in save_extensions:
            return True
        
        # Check filename patterns
        name_lower = file_path.name.lower()
        save_keywords = ['save', 'profile', 'user', 'player', 'game', 'world', 
                        'character', 'progress', 'slot', 'checkpoint']
        
        return any(keyword in name_lower for keyword in save_keywords)
    
    def _is_excluded_file(self, file_path):
        """Check if file should be excluded from save detection"""
        name_lower = file_path.name.lower()
        
        # Exclude common non-save files
        excluded_patterns = [
            'log', 'cache', 'temp', 'crash', 'error', 'debug', 'config',
            'settings', 'preferences', 'install', 'uninstall', 'update',
            'readme', 'license', 'changelog', 'version', 'manifest'
        ]
        
        # Exclude by extension
        excluded_extensions = {
            '.exe', '.dll', '.msi', '.bat', '.cmd', '.ps1', '.sh',
            '.txt', '.md', '.html', '.css', '.js', '.py', '.cpp', '.h',
            '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg',
            '.mp3', '.wav', '.ogg', '.mp4', '.avi', '.mkv', '.zip', '.rar'
        }
        
        if file_path.suffix.lower() in excluded_extensions:
            return True
        
        return any(pattern in name_lower for pattern in excluded_patterns)