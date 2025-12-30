# 📋 QuickClip

**Universal Clipboard History Manager**

A simple, cross-platform clipboard history tool that saves everything you copy and lets you access it later with a single click.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey.svg)

---

## ✨ Features

- 📋 **Clipboard History** - Automatically saves everything you copy (up to 100 items)
- 🔍 **Search** - Quickly find past clips with instant search
- 📌 **Pin Items** - Keep important clips at the top
- 🖱️ **One-Click Copy** - Double-click to copy any item back to clipboard
- 🔔 **System Tray** - Runs quietly in the background
- 💾 **Auto-Save** - History persists between sessions
- 🌙 **Dark Theme** - Beautiful dark UI that's easy on the eyes

---

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DonkRonk17/QuickClip.git
   cd QuickClip
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run QuickClip:**
   ```bash
   python quickclip.py
   ```

### One-Line Install (Windows PowerShell)

```powershell
git clone https://github.com/DonkRonk17/QuickClip.git; cd QuickClip; pip install -r requirements.txt; python quickclip.py
```

### One-Line Install (Mac/Linux)

```bash
git clone https://github.com/DonkRonk17/QuickClip.git && cd QuickClip && pip install -r requirements.txt && python quickclip.py
```

---

## 📖 How to Use

### Basic Usage

1. **Start QuickClip** - Run `python quickclip.py`
2. **Copy anything** - QuickClip automatically captures it
3. **Find past clips** - Use the search bar to filter
4. **Copy again** - Double-click any item to copy it

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Escape` | Minimize to system tray |
| `Ctrl+F` | Focus search bar |
| `Enter` | Copy selected item |
| `Delete` | Delete selected item |

### Features Explained

- **📌 Pin Items**: Click "Pin/Unpin" to keep important clips at the top. Pinned items won't be deleted when history is full.

- **🔍 Search**: Type in the search bar to instantly filter your clipboard history.

- **🗑️ Clear All**: Removes all non-pinned items from history.

- **System Tray**: When you close the window, QuickClip minimizes to the system tray. Right-click the tray icon to quit completely.

---

## 📁 Files

```
QuickClip/
├── quickclip.py      # Main application
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── LICENSE           # MIT License
```

**Data Storage:**
- History is saved to `~/.quickclip_history.json` in your home directory

---

## 🛠️ Requirements

- **Python 3.8+**
- **PySide6** (Qt for Python)
- **pyperclip** (optional, for enhanced clipboard support)

---

## 🎨 Screenshots

QuickClip features a modern dark theme:

```
╔══════════════════════════════════════════════════════════════╗
║  📋 QuickClip                                                ║
║  Your clipboard history, always at hand                      ║
╠══════════════════════════════════════════════════════════════╣
║  🔍 Search clipboard history...                    [Clear]   ║
║  📊 47 items • 3 pinned • Showing 47                        ║
╠══════════════════════════════════════════════════════════════╣
║  📌 My important note that I pinned...            just now   ║
║  Hello world, this is some text I copied...       2m ago     ║
║  https://github.com/DonkRonk17/QuickClip          5m ago     ║
║  Another clipboard item here...                   1h ago     ║
╠══════════════════════════════════════════════════════════════╣
║  Preview:                                                    ║
║  ┌────────────────────────────────────────────────────────┐  ║
║  │ Hello world, this is some text I copied earlier...    │  ║
║  └────────────────────────────────────────────────────────┘  ║
║                                                              ║
║  [📋 Copy Selected]  [📌 Pin/Unpin]  [🗑️ Delete]             ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Metaphy LLC / Team Brain**

- GitHub: [@DonkRonk17](https://github.com/DonkRonk17)

---

## 🙏 Acknowledgments

- Built with [PySide6](https://doc.qt.io/qtforpython/) (Qt for Python)
- Created by Team Brain's Holy Grail Workflow

---

*Made with ❤️ by Team Brain*

