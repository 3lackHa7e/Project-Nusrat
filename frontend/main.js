const { app, BrowserWindow, screen, ipcMain } = require('electron');
const path = require('path');

function createWindow () {
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;

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
