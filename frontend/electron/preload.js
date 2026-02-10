// Preload script
// This file is loaded before the renderer process (React app)
// You can use this to expose Node.js APIs to the renderer securely via contextBridge

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
    // Example:
    // sendNotification: (message) => ipcRenderer.send('notify', message),
});
