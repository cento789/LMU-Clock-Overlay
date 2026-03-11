# LMU Clock Overlay

A lightweight, fully transparent system clock overlay for **Le Mans Ultimate** (and any other fullscreen/windowed game).  
Built because TinyPedal doesn't include a real-time clock — now you'll never lose track of time during long stints!

![Version](https://img.shields.io/badge/version-1.3.0-brightgreen) ![Author](https://img.shields.io/badge/author-cento789-blue) ![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

---

## Features

- **Real-time system clock** — HH:MM:SS updated every 200ms
- **Fully transparent** — only the text is visible, no background window
- **Always on top** — stays visible over fullscreen/borderless games
- **Draggable** — click and drag to reposition anywhere on screen
- **Settings menu** at startup with live preview:
  - Font family (Consolas, Arial, Segoe UI, Verdana, Tahoma, Courier New, Lucida Console, Calibri, Impact)
  - Font size (10–60 px)
  - Color (full color picker)
  - Opacity (20%–100%)
  - 12h / 24h time format
  - Optional date display (dd/mm/yyyy)
  - Text shadow for readability on bright backgrounds
- **System tray** icon — minimizes to tray after start
- **Global hotkey** `Ctrl+Shift+H` — toggle overlay visibility in-game
- **Persistent settings** — all preferences and position saved to `%APPDATA%\LMUClockOverlay\settings.json`
- **Version info embedded** in the .exe (author: cento789)

---

## Installation

No installation required. Just download and run.

1. Download `LMUClockOverlay.exe` from the `dist/` folder
2. Place it anywhere you like
3. Run it

> **Note:** On first launch Windows SmartScreen may warn you — click "More info" → "Run anyway".

---

## Usage

### 1. Settings Menu

When you launch the app, a settings window appears:

| Setting | Description |
|---------|-------------|
| **Font** | Choose from 9 available fonts |
| **Font size** | Slider from 10 to 60 pixels |
| **Color** | Click "Pick Color" to open color chooser |
| **Opacity** | Slider from 20% to 100% |
| **Format** | 24h (`15:30:00`) or 12h (`03:30:00 PM`) |
| **Show date** | Checkbox to display date below the time |
| **Text shadow** | Checkbox to add a dark shadow behind text |

A **live preview** at the bottom shows exactly how the overlay will look.

Click **▶ START** to launch the overlay.

### 2. In-Game Controls

| Action | How |
|--------|-----|
| **Move the overlay** | Left-click and drag |
| **Hide / Show** | Press `Ctrl+Shift+H` |
| **Close** | Right-click on the overlay, or use "Quit" from the tray icon |

### 3. System Tray

After starting, the app minimizes to the system tray (notification area) with a small clock icon. Right-click the tray icon for:

- **Show/Hide** — toggle overlay visibility
- **Quit** — close the application

### 4. Settings Persistence

All settings (font, size, color, opacity, format, date, shadow, position) are automatically saved when you close the overlay and restored on next launch.

Settings file location: `%APPDATA%\LMUClockOverlay\settings.json`

---

## Command Line

```
LMUClockOverlay.exe --version
```

Prints version info and exits.

---

## Building from Source

### Requirements

- Python 3.10+
- Dependencies: `pip install pyinstaller pystray Pillow keyboard`

### Build

```bash
pyinstaller --onefile --noconsole --name LMUClockOverlay --version-file version_info.py --hidden-import pystray._win32 clock_overlay.py
```

The output will be in the `dist/` folder.

---

## File Structure

```
LMUClockOverlay/
├── clock_overlay.py      # Main application source
├── version_info.py       # Windows version resource for PyInstaller
├── build.bat             # One-click build script
├── README.md             # This file
├── docs/
│   └── LMUClockOverlay_UserGuide.pdf   # User guide
└── dist/
    └── LMUClockOverlay.exe             # Built executable
```

---

## Changelog

### v1.3.0
- Added font family selector (9 fonts)
- Added 12h/24h time format toggle
- Added text shadow option for readability

### v1.2.0
- Added settings persistence (saved to %APPDATA%)
- Added position memory (remembers where you placed the overlay)
- Added optional date display
- Added opacity slider
- Added global hotkey Ctrl+Shift+H to hide/show

### v1.1.0
- Added settings menu with live preview
- Added system tray integration
- Added color picker and font size slider

### v1.0.0
- Initial release — transparent clock overlay

---

## License

Free to use. Created by **cento789**.

---

## Credits

- Author: **cento789**
- Built with: Python, tkinter, PyInstaller, pystray, Pillow, keyboard
