"""
Handles copying and organizing backups to the "loaded saves" directory
"""

import shutil
from pathlib import Path
from datetime import datetime
import json

class BackupManager:
    def __init__(self, config, verbose=False):
        self.config = config
        self.verbose = verbose
    
    def backup_saves(self, found_saves):
        """Backup all found saves to the loaded saves directory"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_log = {
            'timestamp': timestamp,
            'games_backed_up': {},
            'total_files': 0,
            'errors': []
        }
        
        for game_name, save_files in found_saves.items():
            if self.verbose:
                print(f"\nBacking up {game_name}...")
            
            # Create game directory in loaded saves
            game_backup_dir = self.config.backup_dir / game_name / timestamp
            game_backup_dir.mkdir(parents=True, exist_ok=True)
            
            backed_up_files = []
            
            for save_file in save_files:
                try:
                    # Preserve relative path structure within the game folder
                    relative_path = self._get_relative_save_path(save_file)
                    backup_path = game_backup_dir / relative_path
                    
                    # Ensure parent directory exists
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy the file
                    shutil.copy2(save_file, backup_path)
                    backed_up_files.append({
                        'original': str(save_file),
                        'backup': str(backup_path),
                        'size': save_file.stat().st_size
                    })
                    
                    if self.verbose:
                        print(f"  Copied: {save_file.name}")
                
                except Exception as e:
                    error_msg = f"Failed to backup {save_file}: {e}"
                    backup_log['errors'].append(error_msg)
                    if self.verbose:
                        print(f"  Error: {error_msg}")
            
            if backed_up_files:
                backup_log['games_backed_up'][game_name] = {
                    'files': backed_up_files,
                    'count': len(backed_up_files),
                    'backup_dir': str(game_backup_dir)
                }
                backup_log['total_files'] += len(backed_up_files)
                
                if self.verbose:
                    print(f"  Successfully backed up {len(backed_up_files)} files")
        
        # Save backup log
        self._save_backup_log(backup_log, timestamp)
        
        return backup_log
    
    def _get_relative_save_path(self, save_file):
        """Get a relative path for the save file to preserve structure"""
        save_file = Path(save_file)
        
        # Try to find a meaningful relative path
        # Start from the deepest meaningful directory
        parts = save_file.parts
        
        # Look for common save directory indicators
        save_indicators = ['saves', 'savegames', 'profiles', 'user', 'data']
        
        for i, part in enumerate(parts):
            if part.lower() in save_indicators:
                # Use everything from this directory onwards
                return Path(*parts[i:])
        
        # If no save indicator found, use the last 2-3 directories
        if len(parts) >= 3:
            return Path(*parts[-3:])
        else:
            return save_file.name
    
    def _save_backup_log(self, backup_log, timestamp):
        """Save backup operation log"""
        log_file = self.config.logs_dir / f"backup_{timestamp}.json"
        
        try:
            with open(log_file, 'w') as f:
                json.dump(backup_log, f, indent=2)
            
            if self.verbose:
                print(f"\nBackup log saved to: {log_file}")
        
        except Exception as e:
            print(f"Warning: Could not save backup log: {e}")
    
    def list_backups(self, game_name=None):
        """List existing backups"""
        backups = {}
        
        if not self.config.backup_dir.exists():
            return backups
        
        for game_dir in self.config.backup_dir.iterdir():
            if not game_dir.is_dir():
                continue
            
            if game_name and game_name.lower() not in game_dir.name.lower():
                continue
            
            game_backups = []
            for backup_dir in game_dir.iterdir():
                if backup_dir.is_dir():
                    # Count files in backup
                    file_count = sum(1 for _ in backup_dir.rglob('*') if _.is_file())
                    game_backups.append({
                        'timestamp': backup_dir.name,
                        'path': str(backup_dir),
                        'file_count': file_count
                    })
            
            if game_backups:
                backups[game_dir.name] = sorted(game_backups, 
                                              key=lambda x: x['timestamp'], 
                                              reverse=True)
        
        return backups