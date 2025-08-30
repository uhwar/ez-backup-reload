#!/usr/bin/env python3
"""
Game Save Backup Utility - Main Entry Point
Automatically locates and backs up game save files from various PC games.
"""

import argparse
import sys
from pathlib import Path
from game_scanner import GameScanner
from backup_manager import BackupManager
from config import Config

def main():
    parser = argparse.ArgumentParser(description='Game Save Backup Utility')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose output')
    parser.add_argument('--scan-only', action='store_true',
                       help='Scan for saves without backing up')
    parser.add_argument('--game', type=str,
                       help='Backup saves for specific game only')
    
    args = parser.parse_args()
    
    # Initialize components
    config = Config()
    scanner = GameScanner(config, verbose=args.verbose)
    backup_manager = BackupManager(config, verbose=args.verbose)
    
    print("Game Save Backup Utility")
    print("=" * 40)
    
    # Scan for game saves
    print("Scanning for game saves...")
    found_saves = scanner.scan_for_saves(game_filter=args.game)
    
    if not found_saves:
        print("No game saves found.")
        return 0
    
    print(f"Found saves for {len(found_saves)} games:")
    for game_name, saves in found_saves.items():
        print(f"  {game_name}: {len(saves)} save files")
    
    if args.scan_only:
        print("\nScan complete. Use without --scan-only to backup saves.")
        return 0
    
    # Backup saves
    print("\nBacking up saves...")
    backup_manager.backup_saves(found_saves)
    print("Backup complete!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())