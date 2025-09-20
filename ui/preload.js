const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Scan for saves without backing up
  scanSaves: (options = {}) => ipcRenderer.invoke('scan-saves', options),
  
  // Backup all saves
  backupSaves: (options = {}) => ipcRenderer.invoke('backup-saves', options),
  
  // List existing backups
  listBackups: () => ipcRenderer.invoke('list-backups'),
  
  // Get backup operation logs
  getLogs: () => ipcRenderer.invoke('get-logs'),
  
  // Window controls
  windowMinimize: () => ipcRenderer.invoke('window-minimize'),
  windowMaximize: () => ipcRenderer.invoke('window-maximize'),
  windowClose: () => ipcRenderer.invoke('window-close'),
  windowIsMaximized: () => ipcRenderer.invoke('window-is-maximized'),
  
  // Utility to format timestamps
  formatTimestamp: (timestamp) => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleString();
    } catch {
      return timestamp;
    }
  }
});

// Expose version info
contextBridge.exposeInMainWorld('versions', {
  node: () => process.versions.node,
  chrome: () => process.versions.chrome,
  electron: () => process.versions.electron
});