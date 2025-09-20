const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs').promises;

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    show: false, // Don't show until ready
    frame: false, // Remove default window frame
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    },
    backgroundColor: '#0d1117', // Match CSS background exactly
    icon: path.join(__dirname, 'assets', 'icon.png') // Optional icon
  });

  // Load the HTML file
  mainWindow.loadFile('index.html');
  
  // Show window when ready to prevent flash
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    
    // Focus the window
    if (mainWindow) {
      mainWindow.focus();
    }
  });
  
  // Open DevTools in development
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC Handlers
ipcMain.handle('scan-saves', async (event, options = {}) => {
  return new Promise((resolve, reject) => {
    const args = ['backup_saves.py', '--scan-only', '--verbose'];
    if (options.game) {
      args.push('--game', options.game);
    }

    const pythonProcess = spawn('py', args, {
      cwd: path.join(__dirname, '..'),
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        resolve({
          success: true,
          output: stdout,
          error: null
        });
      } else {
        reject({
          success: false,
          output: stdout,
          error: stderr || 'Process failed'
        });
      }
    });

    pythonProcess.on('error', (error) => {
      reject({
        success: false,
        output: '',
        error: error.message
      });
    });
  });
});

ipcMain.handle('backup-saves', async (event, options = {}) => {
  return new Promise((resolve, reject) => {
    const args = ['backup_saves.py', '--verbose'];
    if (options.game) {
      args.push('--game', options.game);
    }

    const pythonProcess = spawn('py', args, {
      cwd: path.join(__dirname, '..'),
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        resolve({
          success: true,
          output: stdout,
          error: null
        });
      } else {
        reject({
          success: false,
          output: stdout,
          error: stderr || 'Process failed'
        });
      }
    });

    pythonProcess.on('error', (error) => {
      reject({
        success: false,
        output: '',
        error: error.message
      });
    });
  });
});

ipcMain.handle('list-backups', async () => {
  try {
    const backupDir = path.join(__dirname, '..', 'loaded saves');
    
    try {
      await fs.access(backupDir);
    } catch {
      return { backups: {} };
    }

    const gameDirectories = await fs.readdir(backupDir, { withFileTypes: true });
    const backups = {};

    for (const gameDir of gameDirectories) {
      if (gameDir.isDirectory()) {
        const gamePath = path.join(backupDir, gameDir.name);
        const backupDirs = await fs.readdir(gamePath, { withFileTypes: true });
        
        const gameBackups = [];
        for (const backupDir of backupDirs) {
          if (backupDir.isDirectory()) {
            const backupPath = path.join(gamePath, backupDir.name);
            const stats = await fs.stat(backupPath);
            
            // Count files in backup
            const fileCount = await countFiles(backupPath);
            
            gameBackups.push({
              timestamp: backupDir.name,
              path: backupPath,
              fileCount,
              created: stats.mtime
            });
          }
        }

        if (gameBackups.length > 0) {
          backups[gameDir.name] = gameBackups.sort((a, b) => 
            new Date(b.created) - new Date(a.created)
          );
        }
      }
    }

    return { backups };
  } catch (error) {
    throw new Error(`Failed to list backups: ${error.message}`);
  }
});

ipcMain.handle('get-logs', async () => {
  try {
    const logsDir = path.join(__dirname, '..', 'logs');
    
    try {
      await fs.access(logsDir);
    } catch {
      return { logs: [] };
    }

    const logFiles = await fs.readdir(logsDir);
    const logs = [];

    for (const logFile of logFiles) {
      if (logFile.endsWith('.json')) {
        try {
          const logPath = path.join(logsDir, logFile);
          const logContent = await fs.readFile(logPath, 'utf8');
          const logData = JSON.parse(logContent);
          
          logs.push({
            filename: logFile,
            ...logData
          });
        } catch (error) {
          console.warn(`Failed to read log file ${logFile}:`, error.message);
        }
      }
    }

    return { 
      logs: logs.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)) 
    };
  } catch (error) {
    throw new Error(`Failed to get logs: ${error.message}`);
  }
});

// Window control handlers
ipcMain.handle('window-minimize', () => {
  if (mainWindow) {
    mainWindow.minimize();
  }
});

ipcMain.handle('window-maximize', () => {
  if (mainWindow) {
    if (mainWindow.isMaximized()) {
      mainWindow.unmaximize();
    } else {
      mainWindow.maximize();
    }
  }
});

ipcMain.handle('window-close', () => {
  if (mainWindow) {
    mainWindow.close();
  }
});

ipcMain.handle('window-is-maximized', () => {
  return mainWindow ? mainWindow.isMaximized() : false;
});

// Helper function to count files in directory recursively
async function countFiles(dirPath) {
  let count = 0;
  
  try {
    const items = await fs.readdir(dirPath, { withFileTypes: true });
    
    for (const item of items) {
      if (item.isFile()) {
        count++;
      } else if (item.isDirectory()) {
        count += await countFiles(path.join(dirPath, item.name));
      }
    }
  } catch (error) {
    // Ignore permission errors
  }
  
  return count;
}
