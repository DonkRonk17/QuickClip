# QuickClip - Usage Examples

Quick navigation:
- [Example 1: Basic Usage](#example-1-basic-usage)
- [Example 2: Pinning Important Items](#example-2-pinning-important-items)
- [Example 3: Searching History](#example-3-searching-history)
- [Example 4: Copying from History](#example-4-copying-from-history)
- [Example 5: Deleting Items](#example-5-deleting-items)
- [Example 6: Clearing History](#example-6-clearing-history)
- [Example 7: Using System Tray](#example-7-using-system-tray)
- [Example 8: Handling Large Text](#example-8-handling-large-text)
- [Example 9: Programmatic Access](#example-9-programmatic-access)
- [Example 10: Integration Patterns](#example-10-integration-patterns)

---

## Example 1: Basic Usage

**Scenario:** First time starting QuickClip and capturing clipboard content.

**Steps:**
1. Start QuickClip:
   ```bash
   python quickclip.py
   ```
2. Copy some text (e.g., "Hello World") using Ctrl+C.
3. Copy another text (e.g., "QuickClip is awesome!").
4. Look at the QuickClip window.

**Expected Output:**
```
╔══════════════════════════════════════════════════════════════╗
║  📋 QuickClip                                                ║
║  Your clipboard history, always at hand                      ║
╠══════════════════════════════════════════════════════════════╣
║  🔍 Search clipboard history...                    [Clear]   ║
║  📊 2 items • 0 pinned • Showing 2                          ║
╠══════════════════════════════════════════════════════════════╣
║  QuickClip is awesome!                             just now  ║
║  Hello World                                       just now  ║
╚══════════════════════════════════════════════════════════════╝
```

**What You Learned:**
- QuickClip automatically captures clipboard content
- Newest items appear at the top
- Statistics show total items and visibility

---

## Example 2: Pinning Important Items

**Scenario:** You have an API key you want to keep accessible.

**Steps:**
1. Copy your API key: `sk-abc123XYZ789...`
2. In QuickClip, click the item to select it.
3. Click "📌 Pin/Unpin" button.

**Expected Output:**
```
╠══════════════════════════════════════════════════════════════╣
║  📊 5 items • 1 pinned • Showing 5                          ║
╠══════════════════════════════════════════════════════════════╣
║  📌 sk-abc123XYZ789...                             2h ago    ║  ← Pinned!
║  Some other text I copied                          just now  ║
║  Another clipboard item                            5m ago    ║
╚══════════════════════════════════════════════════════════════╝
```

**What You Learned:**
- Pinned items stay at the top of the list
- Pinned items won't be deleted when history is full
- Pinned items survive "Clear All" operation

---

## Example 3: Searching History

**Scenario:** Finding a URL you copied earlier.

**Steps:**
1. Type "github" in the search bar.
2. Observe the filtered results.

**Before Search:**
```
║  10 items • 2 pinned • Showing 10                           ║
╠══════════════════════════════════════════════════════════════╣
║  📌 API Key: sk-abc123...                          1h ago    ║
║  Some random text                                  10m ago   ║
║  https://github.com/DonkRonk17/QuickClip          15m ago   ║
║  Another item                                      20m ago   ║
║  https://github.com/DonkRonk17/SynapseLink        25m ago   ║
```

**After Search "github":**
```
║  🔍 github                                         [Clear]   ║
║  📊 10 items • 2 pinned • Showing 2                         ║
╠══════════════════════════════════════════════════════════════╣
║  https://github.com/DonkRonk17/QuickClip          15m ago   ║
║  https://github.com/DonkRonk17/SynapseLink        25m ago   ║
```

**What You Learned:**
- Search filters in real-time as you type
- Search is case-insensitive
- Clear the search to see all items again

---

## Example 4: Copying from History

**Scenario:** Re-using a previously copied code snippet.

**Steps:**
1. Find the item you want to copy.
2. Double-click the item OR select and press Enter.
3. Paste in your target application.

**Visual:**
```
╠══════════════════════════════════════════════════════════════╣
║  def hello():                                      5m ago    ║ ← Double-click
║    return "Hello World"                                      ║
╠══════════════════════════════════════════════════════════════╣
║  Preview:                                                    ║
║  ┌────────────────────────────────────────────────────────┐  ║
║  │ def hello():                                           │  ║
║  │     return "Hello World"                               │  ║
║  └────────────────────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════════════════╝

[System notification: "Copied! def hello():..."]
```

**What You Learned:**
- Double-click copies item back to clipboard
- A notification confirms the copy
- The item moves to the top of the list

---

## Example 5: Deleting Items

**Scenario:** Removing sensitive information you accidentally copied.

**Steps:**
1. Select the item to delete.
2. Click "🗑️ Delete" button OR press Delete key.

**Before:**
```
║  Password123!                                      just now  ║
║  Other safe content                                5m ago    ║
```

**After:**
```
║  Other safe content                                5m ago    ║
```

**What You Learned:**
- Individual items can be deleted
- Delete key is a quick shortcut
- Deletion is immediate (no undo)

---

## Example 6: Clearing History

**Scenario:** Cleaning up your clipboard history while keeping important items.

**Steps:**
1. Pin any items you want to keep.
2. Click "Clear All" button.
3. Confirm in the dialog.

**Before:**
```
║  📊 25 items • 2 pinned • Showing 25                        ║
╠══════════════════════════════════════════════════════════════╣
║  📌 Important API Key                              2h ago    ║
║  📌 My favorite code snippet                       1d ago    ║
║  Random item 1                                     just now  ║
║  Random item 2                                     5m ago    ║
║  ... (21 more items)                                         ║
```

**After Clear:**
```
║  📊 2 items • 2 pinned • Showing 2                          ║
╠══════════════════════════════════════════════════════════════╣
║  📌 Important API Key                              2h ago    ║
║  📌 My favorite code snippet                       1d ago    ║
```

**What You Learned:**
- Clear All removes only non-pinned items
- Pinned items are preserved
- A confirmation dialog prevents accidents

---

## Example 7: Using System Tray

**Scenario:** Running QuickClip in the background.

**Steps:**
1. Close the QuickClip window (X button or Escape key).
2. QuickClip minimizes to system tray.
3. Double-click tray icon to reopen.
4. Right-click tray icon for menu.

**Tray Menu:**
```
┌─────────────────┐
│ Show QuickClip  │
│ ─────────────── │
│ Quit            │
└─────────────────┘
```

**Notification on minimize:**
```
[QuickClip: QuickClip is still running in the system tray.]
```

**What You Learned:**
- Closing the window keeps QuickClip running
- Double-click tray icon to show window
- Right-click for quit option
- Clipboard monitoring continues in background

---

## Example 8: Handling Large Text

**Scenario:** Copying a large code file or document.

**Steps:**
1. Copy a large block of text (e.g., entire Python file).
2. View in QuickClip.
3. Select to see full preview.

**List View (truncated):**
```
║  #!/usr/bin/env python3 """QuickClip - Universal Clipbo... ║
```

**Preview Pane (full content):**
```
║  Preview:                                                    ║
║  ┌────────────────────────────────────────────────────────┐  ║
║  │ #!/usr/bin/env python3                                 │  ║
║  │ """                                                    │  ║
║  │ QuickClip - Universal Clipboard History Manager        │  ║
║  │ ================================================       │  ║
║  │ A simple, cross-platform clipboard history tool.       │  ║
║  │ ...                                                    │  ║
║  │ """                                                    │  ║
║  └────────────────────────────────────────────────────────┘  ║
```

**What You Learned:**
- Large text is truncated in the list view
- Full content visible in preview pane
- QuickClip handles any text size

---

## Example 9: Programmatic Access

**Scenario:** Accessing clipboard history from another script or tool.

**Python Script:**
```python
import json
from pathlib import Path

def get_quickclip_history(count=10):
    """Read QuickClip history from its JSON file."""
    history_file = Path.home() / ".quickclip_history.json"
    
    if not history_file.exists():
        return []
    
    with open(history_file, 'r', encoding='utf-8') as f:
        clips = json.load(f)
    
    return clips[:count]

# Get recent clips
for clip in get_quickclip_history(5):
    pinned = "📌 " if clip.get('pinned') else ""
    text = clip['text'][:50].replace('\n', ' ')
    print(f"{pinned}{text}...")
```

**Expected Output:**
```
📌 sk-abc123XYZ789...
Hello World...
https://github.com/DonkRonk17/QuickClip...
def hello(): return "Hello World"...
Some other text I copied earlier...
```

**What You Learned:**
- History is stored in `~/.quickclip_history.json`
- JSON format is easy to parse
- Other tools can read clipboard context

---

## Example 10: Integration Patterns

**Scenario:** Using QuickClip with other Team Brain tools.

### Pattern A: DevSnapshot Integration

```python
from pathlib import Path
import json

def capture_clipboard_context():
    """Get clipboard context for development snapshot."""
    history_file = Path.home() / ".quickclip_history.json"
    
    if not history_file.exists():
        return {"status": "unavailable"}
    
    with open(history_file) as f:
        clips = json.load(f)
    
    return {
        "status": "available",
        "total_clips": len(clips),
        "pinned_count": sum(1 for c in clips if c.get('pinned')),
        "recent_5": [c['text'][:100] for c in clips[:5]]
    }

context = capture_clipboard_context()
print(f"Clipboard: {context['total_clips']} items, {context['pinned_count']} pinned")
```

### Pattern B: Search and Filter

```python
from pathlib import Path
import json

def search_clipboard(term):
    """Search clipboard history for specific content."""
    history_file = Path.home() / ".quickclip_history.json"
    
    with open(history_file) as f:
        clips = json.load(f)
    
    return [c for c in clips if term.lower() in c['text'].lower()]

# Find all URLs
urls = search_clipboard("http")
print(f"Found {len(urls)} URLs in clipboard history")

# Find code snippets
code = search_clipboard("def ")
print(f"Found {len(code)} Python function definitions")
```

### Pattern C: Bash Quick Access

```bash
# Add to ~/.bashrc or ~/.zshrc

# View recent QuickClip items
alias qclips='python3 -c "
import json
from pathlib import Path
clips = json.load(open(Path.home() / \".quickclip_history.json\"))[:5]
for c in clips:
    pin = \"📌 \" if c.get(\"pinned\") else \"\"
    print(f\"{pin}{c[\"text\"][:60]}...\")
"'

# Search QuickClip history
qfind() {
    python3 -c "
import json
from pathlib import Path
clips = json.load(open(Path.home() / '.quickclip_history.json'))
found = [c for c in clips if '$1'.lower() in c['text'].lower()]
print(f'Found {len(found)} matches')
for c in found[:5]:
    print(f\"  {c['text'][:60]}...\")
" "$1"
}
```

**What You Learned:**
- QuickClip data is accessible via JSON
- Easy integration with other Python tools
- Bash aliases for quick command-line access
- Search patterns for finding specific content

---

## Quick Reference

| Task | Method |
|------|--------|
| Copy from history | Double-click item |
| Pin/Unpin | Select + "Pin/Unpin" button |
| Delete | Select + "Delete" button or Delete key |
| Search | Type in search bar |
| Clear all | "Clear All" button |
| Show/Hide | Escape key or tray icon |
| Focus search | Ctrl+F |

**Data Location:**
- Windows: `C:\Users\<you>\.quickclip_history.json`
- macOS: `/Users/<you>/.quickclip_history.json`
- Linux: `/home/<you>/.quickclip_history.json`

---

**See also:**
- [README.md](README.md) - Full documentation
- [CHEAT_SHEET.txt](CHEAT_SHEET.txt) - Quick reference
- [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Integration details
