# QuickClip

**Universal Clipboard History Manager**

A simple, cross-platform clipboard history tool that saves everything you copy and lets you access it later with a single click.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

---

## Table of Contents

- [Overview](#overview)
- [Who Requested This Tool](#who-requested-this-tool)
- [Why It Was Requested](#why-it-was-requested)
- [The Problem](#the-problem)
- [The Solution](#the-solution)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Configuration](#configuration)
- [Data Storage](#data-storage)
- [Integration with Team Brain](#integration-with-team-brain)
- [Programmatic Access](#programmatic-access)
- [Screenshots](#screenshots)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

---

## Overview

**QuickClip** is a lightweight, universal clipboard history manager that automatically captures everything you copy, allowing you to search, pin important items, and access your clipboard history anytime. Unlike the built-in clipboard managers in Windows or macOS, QuickClip:

- Persists history across reboots
- Provides powerful search functionality
- Allows pinning important items
- Offers a beautiful dark-themed GUI
- Stores data in accessible JSON format
- Works cross-platform (Windows, macOS, Linux)

---

## Who Requested This Tool

**Origin:** Self-initiated (Team Brain Utility Tool)

**Primary Users:**
- Developers who frequently copy code snippets
- Writers who need access to previously copied text
- Anyone who wants a better clipboard experience
- Team Brain agents who need clipboard context

**Built By:** FORGE (Team Brain Orchestrator)

---

## Why It Was Requested

The native clipboard on most operating systems only stores **one item at a time**. This creates several problems:

1. **Lost Content:** Copy something new, lose the previous content forever
2. **No Search:** Can't find previously copied content
3. **No Persistence:** Reboot and lose clipboard history
4. **No Importance Marking:** Can't mark certain clips as important
5. **No Context:** AI agents can't see what users were copying

QuickClip solves all of these problems with a single, elegant solution.

---

## The Problem

### Before QuickClip

```
You: *copies API key*
You: *copies a URL*
You: "Wait, what was that API key?"
You: *searches email for 20 minutes*
```

### Common Pain Points

| Problem | Impact | Frequency |
|---------|--------|-----------|
| Lost clipboard content | Time wasted re-finding | Daily |
| Can't find old copies | Frustration, delays | Multiple times/week |
| Clipboard cleared on reboot | Lost important data | Weekly |
| No way to save important clips | Re-copying same content | Daily |

---

## The Solution

### After QuickClip

```
You: *copies API key*
You: *copies a URL*
You: "Wait, what was that API key?"
You: *opens QuickClip, searches "api", finds it instantly*
```

### QuickClip Benefits

| Benefit | How | Impact |
|---------|-----|--------|
| Never lose clipboard content | Automatic capture | Saves hours/week |
| Find anything instantly | Powerful search | Productivity boost |
| Survive reboots | JSON persistence | Peace of mind |
| Save important clips | Pin feature | No re-copying |
| AI context | JSON access | Better assistance |

---

## Features

### Core Features

- **Automatic Clipboard Monitoring** - Captures everything you copy
- **Persistent History** - Saves to JSON, survives reboots (100 items max)
- **Powerful Search** - Find any clip instantly
- **Pin Important Items** - Mark clips to protect from clearing
- **System Tray Integration** - Runs quietly in background
- **Cross-Platform** - Windows, macOS, Linux

### User Interface

- **Dark Theme** - Beautiful, modern design that's easy on the eyes
- **Split View** - List on left, preview on right
- **Real-time Updates** - See new clips immediately
- **Visual Indicators** - Pinned items clearly marked

### Technical Features

- **Deduplication** - Same content moves to top, no duplicates
- **Configurable Limits** - Control history size
- **JSON Export** - Data always accessible
- **Low Resource Usage** - Minimal CPU/memory impact

---

## Quick Start

### One-Line Install (with pip)

```bash
pip install PySide6 && python quickclip.py
```

### Three-Step Start

```bash
# 1. Clone or download QuickClip
git clone https://github.com/DonkRonk17/QuickClip.git
cd QuickClip

# 2. Install dependency
pip install PySide6

# 3. Run
python quickclip.py
```

That's it! QuickClip will start monitoring your clipboard immediately.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- PySide6 (Qt for Python)

### Method 1: Git Clone

```bash
git clone https://github.com/DonkRonk17/QuickClip.git
cd QuickClip
pip install -r requirements.txt
python quickclip.py
```

### Method 2: Manual Download

1. Download the repository as ZIP
2. Extract to desired location
3. Open terminal in extracted folder
4. Run: `pip install PySide6`
5. Run: `python quickclip.py`

### Method 3: Development Install

```bash
git clone https://github.com/DonkRonk17/QuickClip.git
cd QuickClip
pip install -e .
quickclip  # Now available as command
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

## Usage

### Starting QuickClip

```bash
# Standard start
python quickclip.py

# Run in background (Linux/Mac)
python quickclip.py &

# Run in background (Windows PowerShell)
Start-Process python -ArgumentList "quickclip.py" -WindowStyle Hidden
```

### Basic Workflow

1. **Start QuickClip** - Runs in system tray
2. **Copy Anything** - Automatically captured
3. **Access History** - Click tray icon or use shortcut
4. **Search** - Type in search bar to filter
5. **Pin** - Click pin button for important items
6. **Re-Copy** - Double-click any item

### Main Window

```
+------------------------------------------------------------------+
|  QuickClip                                                        |
|  Your clipboard history, always at hand                          |
+------------------------------------------------------------------+
|  [Search clipboard history...]                     [Clear All]   |
|  47 items - 3 pinned - Showing 47                               |
+------------------------------------------------------------------+
|                                 |                                |
|  [PIN] My important note...     |  Full content preview:         |
|  Hello world text...            |                                |
|  https://github.com/...         |  Hello world, this is some    |
|  Another clipboard item...      |  text I copied earlier...     |
|                                 |                                |
+------------------------------------------------------------------+
|  [Copy Selected]  [Pin/Unpin]  [Delete]                         |
+------------------------------------------------------------------+
|  Ctrl+Shift+V to show - 100 items max - Auto-saves              |
+------------------------------------------------------------------+
```

### System Tray

- **Double-Click:** Open main window
- **Right-Click:** Context menu
  - Show QuickClip
  - Quit

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Escape` | Minimize to system tray |
| `Ctrl+F` | Focus search bar |
| `Enter` | Copy selected item |
| `Delete` | Delete selected item |
| `Double-Click` | Copy item to clipboard |

---

## Configuration

QuickClip can be configured by editing constants in `quickclip.py`:

### Available Settings

```python
# Version
VERSION = "1.0.0"

# Application name
APP_NAME = "QuickClip"

# Maximum number of clips to store
MAX_HISTORY = 100

# History file location
SAVE_FILE = Path.home() / ".quickclip_history.json"
```

### Customization Examples

**Store More History:**
```python
MAX_HISTORY = 500  # Store 500 clips
```

**Custom Data Location:**
```python
SAVE_FILE = Path("D:/QuickClip_Data/history.json")  # Custom path
```

---

## Data Storage

### Location

QuickClip stores history in a JSON file in your home directory:

| Platform | Path |
|----------|------|
| Windows | `C:\Users\<you>\.quickclip_history.json` |
| macOS | `/Users/<you>/.quickclip_history.json` |
| Linux | `/home/<you>/.quickclip_history.json` |

### JSON Format

```json
[
  {
    "text": "Hello World",
    "timestamp": "2026-01-15T10:30:00.123456",
    "pinned": false
  },
  {
    "text": "Important API Key",
    "timestamp": "2026-01-15T09:00:00.000000",
    "pinned": true
  }
]
```

### Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | The copied text |
| `timestamp` | ISO string | When it was copied |
| `pinned` | boolean | Protection status |

---

## Integration with Team Brain

QuickClip is part of the Team Brain tool ecosystem. Here's how it integrates:

### For AI Agents

Agents can read clipboard history for context:

```python
import json
from pathlib import Path

def get_clipboard_context():
    history = Path.home() / ".quickclip_history.json"
    if history.exists():
        with open(history) as f:
            return json.load(f)
    return []

# Get recent clips for context
clips = get_clipboard_context()[:5]
```

### Integration Points

| Tool | Integration |
|------|-------------|
| **DevSnapshot** | Include clipboard in snapshots |
| **SessionReplay** | Add clipboard context to replays |
| **SynapseLink** | Alert on clipboard patterns |
| **AgentHealth** | Track activity via clipboard |
| **MemoryBridge** | Persist pinned items |

See [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) for full details.

---

## Programmatic Access

### Python - Read History

```python
import json
from pathlib import Path

def get_clips(count=10):
    history = Path.home() / ".quickclip_history.json"
    with open(history, 'r') as f:
        clips = json.load(f)
    return clips[:count]

for clip in get_clips(5):
    print(f"[{clip['timestamp'][:10]}] {clip['text'][:50]}...")
```

### Python - Search

```python
def search_clips(term):
    clips = get_clips(100)
    return [c for c in clips if term.lower() in c['text'].lower()]

api_clips = search_clips("api")
```

### Python - Get Pinned

```python
def get_pinned():
    clips = get_clips(100)
    return [c for c in clips if c.get('pinned')]

important = get_pinned()
```

### Bash - Quick Access

```bash
# View recent clips
cat ~/.quickclip_history.json | python3 -c "
import json, sys
clips = json.load(sys.stdin)[:5]
for c in clips:
    print(f'{c[\"timestamp\"][:10]}: {c[\"text\"][:60]}...')
"
```

---

## Screenshots

### Main Window (Dark Theme)

```
+==================================================================+
|  QuickClip                                                        |
|  Your clipboard history, always at hand                          |
+==================================================================+
|  [Search clipboard history...]                     [Clear All]   |
|  47 items - 3 pinned - Showing 47                               |
+==================================================================+
|  [PIN] My important note that I pinned...         just now       |
|  Hello world, this is some text I copied...       2m ago         |
|  https://github.com/DonkRonk17/QuickClip          5m ago         |
|  Another clipboard item here...                   1h ago         |
+------------------------------------------------------------------+
|  Preview:                                                        |
|  +------------------------------------------------------------+  |
|  | Hello world, this is some text I copied earlier...         |  |
|  +------------------------------------------------------------+  |
|                                                                  |
|  [Copy Selected]  [Pin/Unpin]  [Delete]                         |
+==================================================================+
```

---

## API Reference

### ClipboardItem Class

```python
class ClipboardItem:
    """Represents a single clipboard history item."""
    
    text: str          # The copied text
    timestamp: str     # ISO format timestamp
    pinned: bool       # Whether item is protected
    
    def to_dict() -> dict    # Serialize to dictionary
    def from_dict(d) -> ClipboardItem  # Deserialize from dict
    def preview(max_len=80) -> str  # Get truncated preview
    def time_ago() -> str    # Human-readable time
```

### ClipboardMonitor Class

```python
class ClipboardMonitor(QObject):
    """Monitors the clipboard for changes."""
    
    new_clip: Signal(str)  # Emitted when new content detected
    
    def check_clipboard()  # Check for changes
    def set_text(text)     # Set clipboard without triggering
```

### QuickClipWindow Class

```python
class QuickClipWindow(QMainWindow):
    """Main application window."""
    
    def on_new_clip(text)    # Handle new clipboard content
    def refresh_list()       # Refresh the history display
    def copy_item(item)      # Copy item back to clipboard
    def toggle_pin()         # Toggle pin status
    def delete_selected()    # Delete selected item
    def clear_history()      # Clear non-pinned items
    def save_history()       # Save to file
    def load_history()       # Load from file
```

---

## Troubleshooting

### Common Issues

#### QuickClip Won't Start

**Symptom:** Error when running `python quickclip.py`

**Solutions:**
1. Check Python version: `python --version` (need 3.8+)
2. Install PySide6: `pip install PySide6`
3. Check for conflicting Qt installations

#### Clipboard Not Being Monitored

**Symptom:** Copies aren't appearing in history

**Solutions:**
1. Restart QuickClip
2. Check if another clipboard manager is interfering
3. On Linux, ensure X11 display is available

#### History Not Saving

**Symptom:** Clips disappear after restart

**Solutions:**
1. Check file permissions: `ls -la ~/.quickclip_history.json`
2. Ensure disk space available
3. Check for JSON corruption

#### System Tray Icon Missing

**Symptom:** Can't see tray icon

**Solutions:**
1. Check system tray settings (show hidden icons)
2. On Linux, install system tray extension
3. Restart QuickClip

### Error Messages

| Error | Meaning | Fix |
|-------|---------|-----|
| `ModuleNotFoundError: PySide6` | Qt not installed | `pip install PySide6` |
| `Permission denied` | Can't write file | Check folder permissions |
| `JSONDecodeError` | Corrupted history | Delete history file |

---

## FAQ

### General Questions

**Q: Does QuickClip send my clipboard data anywhere?**  
A: No! All data is stored locally on your machine. QuickClip has no network features.

**Q: How much disk space does QuickClip use?**  
A: Minimal. History is stored as JSON. 100 clips typically uses under 1 MB.

**Q: Can I sync QuickClip across devices?**  
A: Not built-in. You could sync the history file via cloud storage.

**Q: Does QuickClip capture passwords?**  
A: Yes, it captures everything. Use delete to remove sensitive items.

### Technical Questions

**Q: Why PySide6 instead of tkinter?**  
A: PySide6 provides a more modern appearance and better system tray integration.

**Q: Can I use QuickClip without GUI?**  
A: The main application requires GUI, but you can read the JSON history programmatically.

**Q: What's the polling interval?**  
A: 500ms. Balances responsiveness with CPU usage.

**Q: Does QuickClip capture images?**  
A: Currently text-only. Image support is planned for future versions.

---

## Development

### Project Structure

```
QuickClip/
+-- quickclip.py         # Main application
+-- test_quickclip.py    # Test suite
+-- requirements.txt     # Dependencies
+-- setup.py             # Package configuration
+-- README.md            # This file
+-- EXAMPLES.md          # Usage examples
+-- CHEAT_SHEET.txt      # Quick reference
+-- LICENSE              # MIT License
+-- .gitignore           # Git ignore rules
+-- branding/            # Visual assets
|   +-- BRANDING_PROMPTS.md
+-- INTEGRATION_PLAN.md       # Tool integration guide
+-- QUICK_START_GUIDES.md     # Per-agent guides
+-- INTEGRATION_EXAMPLES.md   # Integration code samples
```

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/DonkRonk17/QuickClip.git
cd QuickClip

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest test_quickclip.py -v
```

---

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest test_quickclip.py -v

# Run with coverage
python -m pytest test_quickclip.py --cov=quickclip --cov-report=html

# Run specific test
python -m pytest test_quickclip.py::TestClipboardItemBasic::test_init_basic -v
```

### Test Coverage

| Component | Coverage | Status |
|-----------|----------|--------|
| ClipboardItem | 100% | Pass |
| Serialization | 100% | Pass |
| Preview | 100% | Pass |
| Time formatting | 100% | Pass |
| Search | 100% | Pass |
| File I/O | 100% | Pass |

---

## Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `python -m pytest test_quickclip.py`
5. Commit: `git commit -m "Add amazing feature"`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Contribution Guidelines

- Write tests for new features
- Follow existing code style
- Update documentation as needed
- Keep PRs focused and small

### Areas for Contribution

- [ ] Image clipboard support
- [ ] Cloud sync feature
- [ ] Keyboard shortcut customization
- [ ] Theme customization
- [ ] CLI interface

---

## License

MIT License

Copyright (c) 2026 Logan Smith / Metaphy LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Credits

### Created By

**Logan Smith**  
Founder, Metaphy LLC  
Healthcare AI Professional & Developer  
*"For the Maximum Benefit of Life"*

### Built With

- **PySide6** - Qt for Python (GUI framework)
- **Python** - Programming language

### Team Brain Contributors

- **FORGE** - Primary development
- **ATLAS** - Testing assistance
- **CLIO** - Linux validation

### Acknowledgments

- Qt Project for the excellent GUI framework
- Python community for the amazing ecosystem
- Team Brain's Holy Grail Workflow

---

## Support

### Getting Help

- **GitHub Issues:** [Report bugs or request features](https://github.com/DonkRonk17/QuickClip/issues)
- **Documentation:** This README and linked files
- **Examples:** See [EXAMPLES.md](EXAMPLES.md)
- **Quick Reference:** See [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

### Useful Links

| Resource | Link |
|----------|------|
| Repository | https://github.com/DonkRonk17/QuickClip |
| Issues | https://github.com/DonkRonk17/QuickClip/issues |
| Examples | [EXAMPLES.md](EXAMPLES.md) |
| Integration | [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) |
| Quick Start | [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md) |

---

## Version History

### v1.0.0 (February 2026)

- Initial release
- Core clipboard monitoring
- Search functionality
- Pin/unpin feature
- System tray integration
- Persistent JSON storage
- Dark theme GUI
- Cross-platform support

### Planned: v1.1.0

- Performance improvements
- Additional keyboard shortcuts
- History export feature

---

<div align="center">

**QuickClip** - Universal Clipboard History Manager

*Part of the Team Brain Tool Ecosystem*

*One World. One Family. One Love.*

</div>