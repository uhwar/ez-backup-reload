@echo off
REM Quick scan shortcut - just runs scan without prompts
echo Running quick scan for game saves...
py backup_saves.py --scan-only --verbose
pause