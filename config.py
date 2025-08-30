"""
Configuration settings for the Game Save Backup Utility
"""

import os
from pathlib import Path

class Config:
    def __init__(self):
        # Base directories
        self.base_dir = Path(__file__).parent
        self.backup_dir = self.base_dir / "loaded saves"
        self.logs_dir = self.base_dir / "logs"
        
        # Ensure directories exist
        self.backup_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
        # Common save file extensions
        self.save_extensions = {
            '.sav', '.save', '.dat', '.json', '.xml', 
            '.cfg', '.ini', '.profile', '.data'
        }
        
        # Common save folder names
        self.save_folder_names = {
            'saves', 'savegames', 'profiles', 'user', 
            'data', 'savedata', 'saved games'
        }
        
        # Applications to exclude (not games)
        self.excluded_apps = {
            'npm', 'code', 'discord', 'mozilla', 'opera software', 'google', 
            'microsoft', 'atom', 'jetbrains', 'docker', 'kiro', 'obsidian',
            'balenaetcher', 'burpsuite', 'handbrake', 'vlc', 'winrar', 'zoom',
            'qbittorrent', 'qutebrowser', 'ledger live', 'webull desktop',
            'packages', 'programs', 'temp', 'cache', 'crashdumps', 'pip',
            'speech', 'virtualstore', 'intermediate', 'saved', 'publishers',
            'install4j', 'cef', 'base', 'battlEye', 'crashreportclient',
            'discovery', 'overwolf', 'mod.io', 'unisdk_firstopen',
            'ledger-live-desktop-updater', 'lorenz_cuno_klopfenstein',
            'ow-electron', 'electron-hello-world', 'com.seelen.seelen-ui',
            'nomic.ai', 'voicemeeter', 'aimp', 'cherryaudio', 'nnaudio',
            'melkaj', 'maize sampler player', 'fullbucketmusic', 'famistudio',
            'wbcache', 'xfer', 'image-line', 'nvidia corporation', 'nvidia'
        }
        
        # Online games and MMOs to exclude (saves are server-side)
        self.excluded_online_games = {
            'roblox', 'black desert', 'world of warcraft', 'final fantasy xiv',
            'guild wars 2', 'elder scrolls online', 'destiny 2', 'apex legends',
            'fortnite', 'valorant', 'overwatch', 'league of legends', 'dota 2',
            'counter-strike', 'cs2', 'csgo', 'pubg', 'call of duty', 'warzone',
            'lost ark', 'new world', 'albion online', 'eve online', 'warframe',
            'path of exile', 'diablo immortal', 'hearthstone', 'heroes of the storm',
            'starcraft ii', 'world of tanks', 'war thunder', 'rocket league online',
            'fall guys', 'among us', 'dead by daylight', 'sea of thieves',
            'rust', 'ark survival evolved online', 'conan exiles online',
            'minecraft realms', 'terraria multiplayer'
        }
        
        # Known gaming platforms and launchers (keep these)
        self.gaming_platforms = {
            'steam', 'epic games', 'epicgameslauncher', 'battle.net', 'blizzard',
            'riot games', 'valorant', 'riot-client-ux', 'ubisoft', 'origin',
            'gog', 'bethesda', 'rockstar', 'activision'
        }
        
        # Minimum file count threshold for unknown games
        self.min_save_files = 3
        
        # User directories
        self.user_profile = Path(os.environ.get('USERPROFILE', ''))
        self.appdata = Path(os.environ.get('APPDATA', ''))
        self.localappdata = Path(os.environ.get('LOCALAPPDATA', ''))
        
        # Common game save locations
        self.scan_locations = [
            self.user_profile / "Documents" / "My Games",
            self.user_profile / "Documents",
            self.appdata,
            self.localappdata,
            self.localappdata / "Steam",
            self.localappdata / "EpicGamesLauncher",
        ]