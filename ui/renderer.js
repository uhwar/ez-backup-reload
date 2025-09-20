// DOM Elements
const navItems = document.querySelectorAll('.nav-item');
const tabContents = document.querySelectorAll('.tab-content');

// Button elements
const scanBtn = document.getElementById('scan-btn');
const backupBtn = document.getElementById('backup-btn');
const refreshBackupsBtn = document.getElementById('refresh-backups-btn');
const refreshLogsBtn = document.getElementById('refresh-logs-btn');

// Input elements
const scanGameFilter = document.getElementById('scan-game-filter');
const backupGameFilter = document.getElementById('backup-game-filter');

// Output elements
const scanOutput = document.getElementById('scan-output');
const backupOutput = document.getElementById('backup-output');
const scanStatus = document.getElementById('scan-status');
const backupStatus = document.getElementById('backup-status');
const backupsContainer = document.getElementById('backups-container');
const logsContainer = document.getElementById('logs-container');

// Status bar elements
const appStatus = document.getElementById('app-status');
const lastUpdate = document.getElementById('last-update');
const electronVersion = document.getElementById('electron-version');

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    // Small delay to ensure styles are loaded
    setTimeout(() => {
        initializeApp();
        setupEventListeners();
        hideLoadingScreen();
        loadInitialData();
    }, 300);
});

function initializeApp() {
    // Show version info
    electronVersion.textContent = `Electron ${window.versions.electron()}`;
    
    // Set initial tab
    showTab('scan');
    updateStatus('Ready');
}

function hideLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    const appContainer = document.getElementById('app-container');
    
    if (loadingScreen && appContainer) {
        // Fade out loading screen
        loadingScreen.style.transition = 'opacity 0.3s ease';
        loadingScreen.style.opacity = '0';
        
        setTimeout(() => {
            loadingScreen.style.display = 'none';
            appContainer.style.display = 'flex';
            
            // Fade in app
            appContainer.style.opacity = '0';
            appContainer.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {
                appContainer.style.opacity = '1';
            }, 50);
        }, 300);
    }
}

function setupEventListeners() {
    // Navigation
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const tabName = item.dataset.tab;
            showTab(tabName);
        });
    });

    // Action buttons
    scanBtn.addEventListener('click', handleScan);
    backupBtn.addEventListener('click', handleBackup);
    refreshBackupsBtn.addEventListener('click', loadBackups);
    refreshLogsBtn.addEventListener('click', loadLogs);

    // Window controls
    const minimizeBtn = document.getElementById('minimize-btn');
    const maximizeBtn = document.getElementById('maximize-btn');
    const closeBtn = document.getElementById('close-btn');
    
    if (minimizeBtn) {
        minimizeBtn.addEventListener('click', () => {
            window.electronAPI.windowMinimize();
        });
    }
    
    if (maximizeBtn) {
        maximizeBtn.addEventListener('click', async () => {
            await window.electronAPI.windowMaximize();
            updateMaximizeIcon();
        });
    }
    
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            window.electronAPI.windowClose();
        });
    }

    // Enter key support for inputs
    scanGameFilter.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleScan();
    });

    backupGameFilter.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleBackup();
    });
}

function loadInitialData() {
    // Load backups and logs when the app starts
    setTimeout(() => {
        loadBackups();
        loadLogs();
        updateMaximizeIcon();
    }, 1000);
}

function showTab(tabName) {
    // Update navigation
    navItems.forEach(item => {
        item.classList.toggle('active', item.dataset.tab === tabName);
    });

    // Update content
    tabContents.forEach(content => {
        content.classList.toggle('active', content.id === `${tabName}-tab`);
    });

    updateStatus(`Viewing ${tabName}`);
}

async function handleScan() {
    const gameFilter = scanGameFilter.value.trim();
    
    try {
        scanBtn.disabled = true;
        scanStatus.textContent = 'Scanning...';
        scanStatus.className = 'status scanning';
        scanOutput.textContent = 'Initializing scan...\n';
        updateStatus('Scanning for game saves...');

        const options = gameFilter ? { game: gameFilter } : {};
        const result = await window.electronAPI.scanSaves(options);

        scanOutput.textContent = result.output;
        scanStatus.textContent = 'Complete';
        scanStatus.className = 'status complete';
        updateStatus('Scan complete');
        updateLastUpdate();

    } catch (error) {
        const errorMessage = error.error || error.message || 'Unknown error occurred';
        scanOutput.textContent = `Error: ${errorMessage}\n\nOutput:\n${error.output || 'No output'}`;
        scanStatus.textContent = 'Error';
        scanStatus.className = 'status error';
        updateStatus('Scan failed');
    } finally {
        scanBtn.disabled = false;
    }
}

async function handleBackup() {
    const gameFilter = backupGameFilter.value.trim();
    
    try {
        backupBtn.disabled = true;
        backupStatus.textContent = 'Backing up...';
        backupStatus.className = 'status backing-up';
        backupOutput.textContent = 'Initializing backup...\n';
        updateStatus('Creating backups...');

        const options = gameFilter ? { game: gameFilter } : {};
        const result = await window.electronAPI.backupSaves(options);

        backupOutput.textContent = result.output;
        backupStatus.textContent = 'Complete';
        backupStatus.className = 'status complete';
        updateStatus('Backup complete');
        updateLastUpdate();

        // Refresh backups and logs after successful backup
        setTimeout(() => {
            loadBackups();
            loadLogs();
        }, 1000);

    } catch (error) {
        const errorMessage = error.error || error.message || 'Unknown error occurred';
        backupOutput.textContent = `Error: ${errorMessage}\n\nOutput:\n${error.output || 'No output'}`;
        backupStatus.textContent = 'Error';
        backupStatus.className = 'status error';
        updateStatus('Backup failed');
    } finally {
        backupBtn.disabled = false;
    }
}

async function loadBackups() {
    try {
        backupsContainer.innerHTML = '<div class="loading">Loading backups...</div>';
        
        const result = await window.electronAPI.listBackups();
        const backups = result.backups;

        if (Object.keys(backups).length === 0) {
            backupsContainer.innerHTML = `
                <div class="loading">
                    <span class="emoji">📁</span> No backups found yet.<br>
                    <small>Run a backup first to see results here.</small>
                </div>
            `;
            return;
        }

        let html = '';
        for (const [gameName, gameBackups] of Object.entries(backups)) {
            html += `
                <div class="backup-game">
                    <div class="game-name">
                        <span class="emoji">🎮</span>
                        ${escapeHtml(gameName)}
                    </div>
                    <div class="game-backups">
            `;

            gameBackups.forEach(backup => {
                const date = new Date(backup.created);
                const formattedDate = date.toLocaleString();
                
                html += `
                    <div class="backup-item">
                        <div class="backup-timestamp">${backup.timestamp}</div>
                        <div class="backup-details">
                            ${backup.fileCount} files • Created: ${formattedDate}
                        </div>
                    </div>
                `;
            });

            html += `
                    </div>
                </div>
            `;
        }

        backupsContainer.innerHTML = html;

    } catch (error) {
        backupsContainer.innerHTML = `
            <div class="loading">
                <span class="emoji">⚠️</span> Error loading backups: ${error.message}
            </div>
        `;
    }
}

async function loadLogs() {
    try {
        logsContainer.innerHTML = '<div class="loading">Loading logs...</div>';
        
        const result = await window.electronAPI.getLogs();
        const logs = result.logs;

        if (logs.length === 0) {
            logsContainer.innerHTML = `
                <div class="loading">
                    <span class="emoji">📄</span> No logs found yet.<br>
                    <small>Run a backup first to see logs here.</small>
                </div>
            `;
            return;
        }

        let html = '';
        logs.forEach(log => {
            const date = new Date(log.timestamp);
            const formattedDate = date.toLocaleString();
            const gameNames = Object.keys(log.games_backed_up || {});
            const hasErrors = log.errors && log.errors.length > 0;

            html += `
                <div class="log-entry">
                    <div class="log-title">
                        <span class="emoji">${hasErrors ? '⚠️' : '✅'}</span>
                        Backup - ${log.timestamp}
                    </div>
                    <div class="log-meta">
                        ${formattedDate} • ${log.filename}
                    </div>
                    <div class="log-stats">
                        <span class="log-stat">
                            <span class="emoji">🎮</span> 
                            ${gameNames.length} games
                        </span>
                        <span class="log-stat">
                            <span class="emoji">📄</span> 
                            ${log.total_files || 0} files
                        </span>
                        ${hasErrors ? `
                            <span class="log-stat" style="background: var(--error); color: white;">
                                <span class="emoji">⚠️</span> 
                                ${log.errors.length} errors
                            </span>
                        ` : ''}
                    </div>
                    ${gameNames.length > 0 ? `
                        <div class="log-games">
                            Games: ${gameNames.map(escapeHtml).join(', ')}
                        </div>
                    ` : ''}
                </div>
            `;
        });

        logsContainer.innerHTML = html;

    } catch (error) {
        logsContainer.innerHTML = `
            <div class="loading">
                <span class="emoji">⚠️</span> Error loading logs: ${error.message}
            </div>
        `;
    }
}

function updateStatus(status) {
    appStatus.textContent = status;
}

function updateLastUpdate() {
    const now = new Date();
    lastUpdate.textContent = now.toLocaleTimeString();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function updateMaximizeIcon() {
    const maximizeIcon = document.getElementById('maximize-icon');
    if (maximizeIcon) {
        const isMaximized = await window.electronAPI.windowIsMaximized();
        maximizeIcon.textContent = isMaximized ? '⧉' : '□';
        
        const maximizeBtn = document.getElementById('maximize-btn');
        if (maximizeBtn) {
            maximizeBtn.title = isMaximized ? 'Restore' : 'Maximize';
        }
    }
}

// Handle window focus to refresh data
window.addEventListener('focus', () => {
    // Refresh data when window regains focus
    setTimeout(() => {
        loadBackups();
        loadLogs();
    }, 500);
});

// Handle window resize to update maximize icon
window.addEventListener('resize', () => {
    updateMaximizeIcon();
});
