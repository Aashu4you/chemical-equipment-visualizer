const { app, BrowserWindow } = require("electron");
<<<<<<< HEAD
const path = require("path");

// Use app.isPackaged to detect if we are in dev (running from source) or prod
const isDev = !app.isPackaged;
=======
>>>>>>> 64d14e954da9f7489c8d1a6bfb5129b38bf797cc

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    webPreferences: {
<<<<<<< HEAD
      nodeIntegration: true, // Needed for some electron features, but keeping contextIsolation true is safer
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js') // Best practice: use preload (though we don't have one yet, it's good to prep)
    },
  });

  // Load React dev server in dev mode, or static build file in prod
  const startUrl = isDev
    ? "http://localhost:3000"
    : `file://${path.join(__dirname, "../build/index.html")}`;

  mainWindow.loadURL(startUrl);

  // Open DevTools in dev mode
  if (isDev) {
    mainWindow.webContents.openDevTools({ mode: 'detach' });
  }
=======
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  // Load React dev server
  mainWindow.loadURL("http://localhost:3000");
>>>>>>> 64d14e954da9f7489c8d1a6bfb5129b38bf797cc

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

app.whenReady().then(createWindow);

// Quit on all windows closed (except macOS)
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
