"""
Core scanning logic for finding game save files
"""

import os
from pathlib import Path
from save_patterns import SavePatterns

class GameScanner:
    def __init__(self, config, verbose=False):
        self.config = config
        self.verbose = verbose
        self.save_patterns = SavePatterns()
    
    def scan_for_saves(self, game_filter=None):
        """Scan system for game save files"""
        found_saves = {}
        
        # First, scan known game patterns
        if self.verbose:
            print("Scanning known game save locations...")
        
        for game_name, patterns in self.save_patterns.get_all_patterns().items():
            if game_filter and game_filter.lower() not in game_name.lower():
                continue
                
            game_saves = []
            for pattern_path in patterns:
                if pattern_path.exists():
                    saves = self._scan_directory(pattern_path)
                    game_saves.extend(saves)
            
            if game_saves:
                found_saves[game_name] = game_saves
                if self.verbose:
                    print(f"  Found {len(game_saves)} saves for {game_name}")
        
        # Then, scan common locations for unknown games
        if self.verbose:
            print("Scanning common save locations...")
        
        for location in self.config.scan_locations:
            if location.exists():
                unknown_saves = self._scan_for_unknown_games(location, found_saves.keys())
                found_saves.update(unknown_saves)
        
        return found_saves
    
    def _scan_directory(self, directory):
        """Scan a directory for save files"""
        saves = []
        try:
            for item in directory.rglob('*'):
                if item.is_file() and self._is_save_file(item):
                    saves.append(item)
        except (PermissionError, OSError) as e:
            if self.verbose:
                print(f"  Warning: Cannot access {directory}: {e}")
        
        return saves
    
    def _scan_for_unknown_games(self, base_path, known_games):
        """Scan for games not in our known patterns"""
        unknown_saves = {}
        
        try:
            for item in base_path.iterdir():
                if not item.is_dir():
                    continue
                
                # Skip if we already know about this game
                if any(known_game.lower() in item.name.lower() for known_game in known_games):
                    continue
                
                # Skip excluded applications
                if self._is_excluded_app(item.name):
                    continue
                
                # Look for save-like folders or files
                potential_saves = []
                for subitem in item.rglob('*'):
                    if subitem.is_file() and self._is_save_file(subitem):
                        potential_saves.append(subitem)
                    elif subitem.is_dir() and self._is_save_folder(subitem):
                        # Scan inside save folders
                        for save_file in subitem.rglob('*'):
                            if save_file.is_file() and self._is_save_file(save_file):
                                potential_saves.append(save_file)
                
                # Only include if it meets our criteria for being a game
                if self._is_likely_game(item.name, potential_saves):
                    game_name = item.name
                    unknown_saves[game_name] = potential_saves
                    if self.verbose:
                        print(f"  Found {len(potential_saves)} potential saves for {game_name}")
        
        except (PermissionError, OSError) as e:
            if self.verbose:
                print(f"  Warning: Cannot access {base_path}: {e}")
        
        return unknown_saves
    
    def _is_save_file(self, file_path):
        """Check if a file is likely a save file"""
        return self.save_patterns.is_likely_save_file(file_path)
    
    def _is_save_folder(self, folder_path):
        """Check if a folder is likely to contain saves"""
        folder_name = folder_path.name.lower()
        return any(save_name in folder_name for save_name in self.config.save_folder_names)
    
    def _is_excluded_app(self, app_name):
        """Check if this is a known non-game application or online game"""
        app_lower = app_name.lower()
        
        # Check against excluded apps list
        if app_lower in self.config.excluded_apps:
            return True
        
        # Check for partial matches with excluded apps
        for excluded in self.config.excluded_apps:
            if excluded in app_lower or app_lower in excluded:
                return True
        
        # Check against online games/MMOs list
        if app_lower in self.config.excluded_online_games:
            return True
        
        # Check for partial matches with online games
        for excluded_game in self.config.excluded_online_games:
            if excluded_game in app_lower or app_lower in excluded_game:
                return True
        
        return False
    
    def _is_likely_game(self, app_name, potential_saves):
        """Determine if this is likely a game based on name and save patterns"""
        app_lower = app_name.lower()
        
        # If it's a known gaming platform, keep it
        for platform in self.config.gaming_platforms:
            if platform in app_lower:
                return True
        
        # Must have minimum number of save files
        if len(potential_saves) < self.config.min_save_files:
            return False
        
        # Look for game-like indicators in the name
        game_indicators = [
            'game', 'simulator', 'quest', 'world', 'craft', 'wars', 'legends',
            'online', 'rpg', 'mmo', 'adventure', 'fantasy', 'racing', 'sports',
            'strategy', 'action', 'shooter', 'puzzle', 'arcade', 'indie',
            'emulator', 'launcher'
        ]
        
        # Check if name contains game-like words
        has_game_indicator = any(indicator in app_lower for indicator in game_indicators)
        
        # Look for actual save file patterns in the files
        save_file_count = 0
        for save_file in potential_saves:
            if self._has_strong_save_indicators(save_file):
                save_file_count += 1
        
        # Require either game indicator in name OR strong save file patterns
        return has_game_indicator or (save_file_count >= 2)
    
    def _has_strong_save_indicators(self, file_path):
        """Check if file has strong indicators of being a game save"""
        file_path = Path(file_path)
        name_lower = file_path.name.lower()
        
        # Strong save file indicators
        strong_indicators = [
            'save', 'profile', 'player', 'character', 'world', 'level',
            'progress', 'checkpoint', 'slot', 'game'
        ]
        
        # Check filename
        for indicator in strong_indicators:
            if indicator in name_lower:
                return True
        
        # Check parent directory names
        for parent in file_path.parents:
            parent_name = parent.name.lower()
            if any(indicator in parent_name for indicator in strong_indicators):
                return True
        
        return False