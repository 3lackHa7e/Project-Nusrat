const { app, BrowserWindow, screen, ipcMain } = require('electron');
const path = require('path');

function createWindow () {
    // 1. Get the size of your actual monitor
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;

    // 2. Make the window fill the whole screen
    const win = new BrowserWindow({
        width: width,
        height: height,
        transparent: true, // Keep it invisible
        frame: false,
        alwaysOnTop: true,
        skipTaskbar: true, // Don't show in the taskbar
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    win.loadFile('index.html');
    
    // Default: Ignore mouse so you can click your desktop behind her
    win.setIgnoreMouseEvents(true, { forward: true });
}

app.whenReady().then(createWindow);

// ==========================================
// --- NEW: LISTEN FOR MOUSE HOVER EVENTS ---
// ==========================================
ipcMain.on('set-ignore-mouse-events', (event, ignore, options) => {
    const win = BrowserWindow.fromWebContents(event.sender);
    if (win) {
        win.setIgnoreMouseEvents(ignore, options || { forward: true });
    }
});