"""
Unit tests for the backup functionality
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from backup_manager import BackupManager
from config import Config

class TestBackupManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.config = Mock()
        self.config.backup_dir = self.temp_dir / "loaded saves"
        self.config.logs_dir = self.temp_dir / "logs"
        self.config.backup_dir.mkdir(parents=True, exist_ok=True)
        self.config.logs_dir.mkdir(parents=True, exist_ok=True)
        
        self.backup_manager = BackupManager(self.config, verbose=False)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_backup_saves_creates_game_directories(self):
        # Create test save files
        test_saves = {
            "Test Game": [self.temp_dir / "test_save.sav"]
        }
        
        # Create the test save file
        test_saves["Test Game"][0].touch()
        
        # Run backup
        result = self.backup_manager.backup_saves(test_saves)
        
        # Check that game directory was created
        game_dirs = list(self.config.backup_dir.glob("Test Game/*"))
        self.assertEqual(len(game_dirs), 1)
        self.assertTrue(game_dirs[0].is_dir())
    
    def test_list_backups_empty(self):
        result = self.backup_manager.list_backups()
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()