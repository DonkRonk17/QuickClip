# QuickClip - Quick Start Guides

## ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#forge-quick-start)
- [Atlas (Executor)](#atlas-quick-start)
- [Clio (Linux Agent)](#clio-quick-start)
- [Nexus (Multi-Platform)](#nexus-quick-start)
- [Bolt (Free Executor)](#bolt-quick-start)

---

## FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Access clipboard history data for context recovery

### Step 1: Verify QuickClip Data

```python
from pathlib import Path

history = Path.home() / ".quickclip_history.json"
print(f"QuickClip data exists: {history.exists()}")
```

### Step 2: Read Recent Clips

```python
import json
from pathlib import Path

def get_recent_clips(count=5):
    """Get recent clipboard items for context."""
    history = Path.home() / ".quickclip_history.json"
    
    if not history.exists():
        return []
    
    with open(history, 'r', encoding='utf-8') as f:
        clips = json.load(f)
    
    return clips[:count]

# Quick context check
for clip in get_recent_clips():
    pin = "[PIN] " if clip.get('pinned') else ""
    print(f"{pin}[{clip['timestamp'][:16]}] {clip['text'][:60]}...")
```

### Step 3: Integration with Orchestration

**Use Case: Session Context Recovery**
```python
def get_session_clipboard_context(start_time, end_time):
    """Get clips from a specific session timeframe."""
    from datetime import datetime
    
    clips = get_recent_clips(100)
    session_clips = []
    
    for clip in clips:
        try:
            clip_time = datetime.fromisoformat(clip['timestamp'])
            if start_time <= clip_time <= end_time:
                session_clips.append(clip)
        except:
            continue
    
    return session_clips
```

### Next Steps for Forge

1. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Full integration details
2. Try [EXAMPLES.md](EXAMPLES.md) - Example 9 (scripting)
3. Add to session review checklist

---

## ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Track code snippets during build sessions

### Step 1: Verify QuickClip is Running

```python
import json
from pathlib import Path
from datetime import datetime, timedelta

history = Path.home() / ".quickclip_history.json"

if history.exists():
    with open(history) as f:
        clips = json.load(f)
    
    if clips:
        latest = datetime.fromisoformat(clips[0]['timestamp'])
        age = datetime.now() - latest
        
        if age < timedelta(hours=1):
            print("[OK] QuickClip is actively monitoring")
        else:
            print("[!] QuickClip may not be running (last clip is old)")
```

### Step 2: Find Code Snippets

```python
import json
from pathlib import Path

def find_code_clips():
    """Find code-like clipboard items."""
    history = Path.home() / ".quickclip_history.json"
    
    with open(history, 'r') as f:
        clips = json.load(f)
    
    code_indicators = ['def ', 'class ', 'import ', 'function ', 'const ', 
                       'return ', 'if ', 'for ', '{', '}', '=>']
    
    code_clips = []
    for clip in clips:
        if any(ind in clip['text'] for ind in code_indicators):
            code_clips.append(clip)
    
    return code_clips

# Find all code snippets
code = find_code_clips()
print(f"Found {len(code)} code snippets")
```

### Step 3: Build Session Workflow

```python
def session_summary(hours=4):
    """Summary of clipboard activity for session."""
    from datetime import datetime, timedelta
    import json
    from pathlib import Path
    
    history = Path.home() / ".quickclip_history.json"
    
    with open(history) as f:
        clips = json.load(f)
    
    cutoff = datetime.now() - timedelta(hours=hours)
    session_clips = []
    
    for clip in clips:
        try:
            if datetime.fromisoformat(clip['timestamp']) > cutoff:
                session_clips.append(clip)
        except:
            continue
    
    print(f"Session ({hours}h): {len(session_clips)} clips captured")
    print("Code clips:", sum(1 for c in session_clips if 'def ' in c['text']))
    print("URLs:", sum(1 for c in session_clips if 'http' in c['text']))
    
    return session_clips
```

### Next Steps for Atlas

1. Run QuickClip during all build sessions
2. Pin important code templates
3. Review history for documentation

---

## CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Persistent clipboard history on Linux

### Step 1: Linux Installation

```bash
# Install PySide6 for GUI
pip3 install PySide6

# Navigate to QuickClip
cd ~/AutoProjects/QuickClip

# Run in background
python3 quickclip.py &

# Verify
ps aux | grep quickclip
```

### Step 2: CLI Access to History

```bash
# Quick view of recent clips
cat ~/.quickclip_history.json | python3 -c "
import json, sys
clips = json.load(sys.stdin)[:5]
for c in clips:
    pin = '[PIN] ' if c.get('pinned') else ''
    print(f'{pin}{c[\"timestamp\"][:10]}: {c[\"text\"][:60]}...')
"

# Count clips
cat ~/.quickclip_history.json | python3 -c "
import json, sys
clips = json.load(sys.stdin)
print(f'Total clips: {len(clips)}')
print(f'Pinned: {sum(1 for c in clips if c.get(\"pinned\"))}')
"
```

### Step 3: Bash Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc

# View recent clips
alias qclips='cat ~/.quickclip_history.json | python3 -c "
import json,sys;clips=json.load(sys.stdin)[:5]
for c in clips:print(f\"{c[\\\"timestamp\\\"][:10]}: {c[\\\"text\\\"][:60]}...\")
"'

# Search clips
qfind() {
    cat ~/.quickclip_history.json | python3 -c "
import json,sys
term='$1'.lower()
clips=json.load(sys.stdin)
found=[c for c in clips if term in c['text'].lower()]
print(f'Found {len(found)} clips')
for c in found[:5]:
    print(f\"{c['timestamp'][:10]}: {c['text'][:60]}...\")
" "$1"
}

# Usage: qfind "api"
```

### Next Steps for Clio

1. Add bash aliases to profile
2. Test with X11 clipboard operations
3. Report Linux-specific issues

---

## NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Cross-platform clipboard context

### Step 1: Platform Detection

```python
import platform
from pathlib import Path

# QuickClip data is in same relative location on all platforms
history = Path.home() / ".quickclip_history.json"

print(f"Platform: {platform.system()}")
print(f"History path: {history}")
print(f"Data exists: {history.exists()}")
```

### Step 2: Cross-Platform Data Access

```python
import json
import platform
from pathlib import Path

def get_clips_cross_platform():
    """Get QuickClip data on any platform."""
    history = Path.home() / ".quickclip_history.json"
    
    if not history.exists():
        return {"platform": platform.system(), "clips": [], "error": "Not found"}
    
    try:
        with open(history, 'r', encoding='utf-8') as f:
            clips = json.load(f)
        
        return {
            "platform": platform.system(),
            "clips": clips,
            "count": len(clips),
            "pinned": sum(1 for c in clips if c.get('pinned'))
        }
    except Exception as e:
        return {"platform": platform.system(), "error": str(e)}

# Works on Windows, Mac, Linux
result = get_clips_cross_platform()
print(f"Platform: {result['platform']}, Clips: {result.get('count', 0)}")
```

### Next Steps for Nexus

1. Test on all 3 platforms
2. Document platform-specific issues
3. Add to multi-platform workflows

---

## BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Access clipboard context without API costs

### Step 1: Verify Free Access

```bash
# No API needed! Just read the JSON file
cat ~/.quickclip_history.json | head -c 500
```

### Step 2: Quick Context Check (Python)

```python
# Zero API costs - just file read
import json
from pathlib import Path

history = Path.home() / ".quickclip_history.json"

if history.exists():
    with open(history) as f:
        clips = json.load(f)
    
    print(f"[FREE] {len(clips)} clipboard items available")
    print(f"[FREE] Latest: {clips[0]['text'][:50] if clips else 'None'}...")
else:
    print("[INFO] QuickClip not found")
```

### Step 3: Batch Operations (Cost-Free)

```python
import json
from pathlib import Path

def free_clip_operations():
    """All operations are local/free."""
    history = Path.home() / ".quickclip_history.json"
    
    with open(history) as f:
        clips = json.load(f)
    
    # All of these are FREE (no API calls)
    total = len(clips)
    pinned = sum(1 for c in clips if c.get('pinned'))
    code = sum(1 for c in clips if 'def ' in c['text'] or 'function' in c['text'])
    urls = sum(1 for c in clips if 'http' in c['text'])
    
    print(f"[FREE] Total: {total}, Pinned: {pinned}, Code: {code}, URLs: {urls}")

free_clip_operations()
```

### Next Steps for Bolt

1. Add to Cline workflow scripts
2. Use for task context gathering
3. Report issues via Synapse

---

## ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/QuickClip/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message FORGE

---

**Last Updated:** February 1, 2026  
**Maintained By:** FORGE (Team Brain)
