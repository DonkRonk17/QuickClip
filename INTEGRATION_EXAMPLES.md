# QuickClip - Integration Examples

## INTEGRATION PHILOSOPHY

QuickClip stores clipboard history in a simple JSON format, making it easy to integrate with other tools. This document provides **copy-paste-ready code examples** for common integration patterns.

---

## TABLE OF CONTENTS

1. [Pattern 1: Basic Data Access](#pattern-1-basic-data-access)
2. [Pattern 2: QuickClip + DevSnapshot](#pattern-2-quickclip--devsnapshot)
3. [Pattern 3: QuickClip + SynapseLink](#pattern-3-quickclip--synapselink)
4. [Pattern 4: QuickClip + AgentHealth](#pattern-4-quickclip--agenthealth)
5. [Pattern 5: QuickClip + SessionReplay](#pattern-5-quickclip--sessionreplay)
6. [Pattern 6: QuickClip + ContextCompressor](#pattern-6-quickclip--contextcompressor)
7. [Pattern 7: QuickClip + MemoryBridge](#pattern-7-quickclip--memorybridge)
8. [Pattern 8: QuickClip + PostMortem](#pattern-8-quickclip--postmortem)
9. [Pattern 9: Multi-Tool Workflow](#pattern-9-multi-tool-workflow)
10. [Pattern 10: Bash Integration](#pattern-10-bash-integration)

---

## Pattern 1: Basic Data Access

**Use Case:** Read QuickClip history in any Python script

**Code:**

```python
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class QuickClipReader:
    """Simple interface to read QuickClip data."""
    
    def __init__(self):
        self.history_file = Path.home() / ".quickclip_history.json"
    
    def get_all(self) -> List[Dict]:
        """Get all clipboard items."""
        if not self.history_file.exists():
            return []
        
        with open(self.history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_recent(self, count: int = 10) -> List[Dict]:
        """Get most recent items."""
        return self.get_all()[:count]
    
    def get_pinned(self) -> List[Dict]:
        """Get only pinned items."""
        return [c for c in self.get_all() if c.get('pinned')]
    
    def search(self, term: str) -> List[Dict]:
        """Search for items containing term."""
        term = term.lower()
        return [c for c in self.get_all() if term in c['text'].lower()]
    
    def get_by_timeframe(self, hours: int = 24) -> List[Dict]:
        """Get items from last N hours."""
        cutoff = datetime.now() - timedelta(hours=hours)
        results = []
        
        for clip in self.get_all():
            try:
                clip_time = datetime.fromisoformat(clip['timestamp'])
                if clip_time > cutoff:
                    results.append(clip)
            except:
                continue
        
        return results


# Usage example
reader = QuickClipReader()
print(f"Total clips: {len(reader.get_all())}")
print(f"Pinned: {len(reader.get_pinned())}")
print(f"Last 24h: {len(reader.get_by_timeframe(24))}")
```

---

## Pattern 2: QuickClip + DevSnapshot

**Use Case:** Include clipboard context in development snapshots

**Code:**

```python
import json
from pathlib import Path
from datetime import datetime

def capture_dev_snapshot_with_clipboard():
    """Capture development snapshot including clipboard history."""
    
    history_file = Path.home() / ".quickclip_history.json"
    
    clipboard_context = {
        "source": "QuickClip",
        "captured_at": datetime.now().isoformat(),
        "clips": []
    }
    
    if history_file.exists():
        with open(history_file, 'r', encoding='utf-8') as f:
            all_clips = json.load(f)
        
        # Include last 20 clips and all pinned
        recent = all_clips[:20]
        pinned = [c for c in all_clips if c.get('pinned') and c not in recent]
        
        clipboard_context["clips"] = recent + pinned
        clipboard_context["total_history"] = len(all_clips)
        clipboard_context["pinned_count"] = len([c for c in all_clips if c.get('pinned')])
    
    # Create snapshot
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "type": "dev_snapshot",
        "clipboard": clipboard_context
    }
    
    # Save snapshot
    snapshot_file = Path.home() / ".devsnapshots" / f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    snapshot_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(snapshot_file, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, indent=2)
    
    return snapshot_file


# Usage
snapshot_path = capture_dev_snapshot_with_clipboard()
print(f"Snapshot saved: {snapshot_path}")
```

---

## Pattern 3: QuickClip + SynapseLink

**Use Case:** Alert team about important clipboard activity

**Code:**

```python
import json
from pathlib import Path
from datetime import datetime, timedelta

# Assume SynapseLink is available
import sys
sys.path.insert(0, str(Path.home() / "OneDrive/Documents/AutoProjects/SynapseLink"))

def alert_clipboard_patterns():
    """Check clipboard for patterns and alert if found."""
    from synapselink import quick_send
    
    history_file = Path.home() / ".quickclip_history.json"
    
    if not history_file.exists():
        return
    
    with open(history_file, 'r', encoding='utf-8') as f:
        clips = json.load(f)
    
    # Check for patterns
    alerts = []
    
    # Pattern 1: API keys/secrets
    secret_patterns = ['api_key', 'api-key', 'secret', 'password', 'token']
    secrets = [c for c in clips[:50] 
               if any(p in c['text'].lower() for p in secret_patterns)]
    
    if secrets:
        alerts.append(f"[!] Found {len(secrets)} potential secrets in clipboard")
    
    # Pattern 2: Error messages
    error_patterns = ['error:', 'exception:', 'failed', 'traceback']
    errors = [c for c in clips[:20]
              if any(p in c['text'].lower() for p in error_patterns)]
    
    if errors:
        alerts.append(f"[!] Found {len(errors)} error messages copied recently")
    
    # Send alert if patterns found
    if alerts:
        quick_send(
            "FORGE",
            "QuickClip Pattern Alert",
            "\n".join(alerts) + f"\n\nTotal clips: {len(clips)}",
            priority="NORMAL"
        )
        print("Alert sent via SynapseLink")
    
    return alerts


# Usage
alerts = alert_clipboard_patterns()
print(f"Patterns found: {len(alerts) if alerts else 0}")
```

---

## Pattern 4: QuickClip + AgentHealth

**Use Case:** Track clipboard activity as engagement metric

**Code:**

```python
import json
from pathlib import Path
from datetime import datetime, timedelta

def track_clipboard_health(agent_name: str):
    """Track clipboard activity as health metric."""
    
    history_file = Path.home() / ".quickclip_history.json"
    
    if not history_file.exists():
        return {"status": "no_data"}
    
    with open(history_file, 'r', encoding='utf-8') as f:
        clips = json.load(f)
    
    # Analyze activity
    now = datetime.now()
    metrics = {
        "total_clips": len(clips),
        "pinned": sum(1 for c in clips if c.get('pinned')),
        "last_hour": 0,
        "last_24h": 0,
        "code_clips": 0,
        "url_clips": 0
    }
    
    hour_ago = now - timedelta(hours=1)
    day_ago = now - timedelta(hours=24)
    
    for clip in clips:
        try:
            clip_time = datetime.fromisoformat(clip['timestamp'])
            
            if clip_time > hour_ago:
                metrics["last_hour"] += 1
            if clip_time > day_ago:
                metrics["last_24h"] += 1
            
            text = clip['text']
            if any(x in text for x in ['def ', 'class ', 'function', 'import']):
                metrics["code_clips"] += 1
            if 'http' in text:
                metrics["url_clips"] += 1
                
        except:
            continue
    
    # Determine activity level
    if metrics["last_hour"] >= 10:
        activity = "high"
    elif metrics["last_hour"] >= 3:
        activity = "medium"
    elif metrics["last_hour"] >= 1:
        activity = "low"
    else:
        activity = "inactive"
    
    return {"activity": activity, "metrics": metrics}


# Usage
health = track_clipboard_health("ATLAS")
print(f"Activity level: {health['activity']}")
print(f"Last hour: {health['metrics']['last_hour']} clips")
```

---

## Pattern 5: QuickClip + SessionReplay

**Use Case:** Include clipboard context in session debugging

**Code:**

```python
import json
from pathlib import Path
from datetime import datetime

def enrich_session_with_clipboard(session_data: dict):
    """Add clipboard context to session replay."""
    
    session_start = session_data.get('start_time')
    session_end = session_data.get('end_time')
    
    if not session_start or not session_end:
        return session_data
    
    start = datetime.fromisoformat(session_start)
    end = datetime.fromisoformat(session_end)
    
    history_file = Path.home() / ".quickclip_history.json"
    
    if not history_file.exists():
        session_data['clipboard'] = {"status": "unavailable"}
        return session_data
    
    with open(history_file, 'r', encoding='utf-8') as f:
        clips = json.load(f)
    
    # Filter clips to session timeframe
    session_clips = []
    for clip in clips:
        try:
            clip_time = datetime.fromisoformat(clip['timestamp'])
            if start <= clip_time <= end:
                session_clips.append({
                    "time": clip['timestamp'],
                    "text": clip['text'][:200],
                    "pinned": clip.get('pinned', False)
                })
        except:
            continue
    
    session_data['clipboard'] = {
        "status": "available",
        "clip_count": len(session_clips),
        "clips": session_clips
    }
    
    return session_data


# Usage
session = {
    "start_time": "2026-01-15T10:00:00",
    "end_time": "2026-01-15T14:00:00",
    "events": []
}

enriched = enrich_session_with_clipboard(session)
print(f"Session clips: {enriched['clipboard']['clip_count']}")
```

---

## Pattern 6: QuickClip + ContextCompressor

**Use Case:** Compress clipboard history for efficient AI context

**Code:**

```python
import json
from pathlib import Path

def get_compressed_clipboard_context(max_chars: int = 2000):
    """Get token-efficient clipboard summary."""
    
    history_file = Path.home() / ".quickclip_history.json"
    
    if not history_file.exists():
        return "No clipboard history available."
    
    with open(history_file, 'r', encoding='utf-8') as f:
        clips = json.load(f)
    
    # Build context string
    lines = ["CLIPBOARD CONTEXT (QuickClip):"]
    lines.append(f"Total items: {len(clips)}")
    lines.append(f"Pinned: {sum(1 for c in clips if c.get('pinned'))}")
    lines.append("")
    
    # Add pinned items first
    pinned = [c for c in clips if c.get('pinned')]
    if pinned:
        lines.append("=== PINNED ITEMS ===")
        for p in pinned[:5]:
            lines.append(f"- {p['text'][:100]}...")
        lines.append("")
    
    # Add recent items
    lines.append("=== RECENT CLIPS ===")
    for clip in clips[:10]:
        if not clip.get('pinned'):
            preview = clip['text'][:80].replace('\n', ' ')
            lines.append(f"[{clip['timestamp'][:10]}] {preview}...")
    
    context = "\n".join(lines)
    
    # Truncate if too long
    if len(context) > max_chars:
        context = context[:max_chars-3] + "..."
    
    return context


# Usage
context = get_compressed_clipboard_context(1500)
print(context)
print(f"\nContext length: {len(context)} chars")
```

---

## Pattern 7: QuickClip + MemoryBridge

**Use Case:** Persist important clips to memory core

**Code:**

```python
import json
from pathlib import Path
from datetime import datetime

def sync_pinned_to_memory():
    """Save pinned clipboard items to memory core."""
    
    history_file = Path.home() / ".quickclip_history.json"
    
    if not history_file.exists():
        return {"status": "no_data"}
    
    with open(history_file, 'r', encoding='utf-8') as f:
        clips = json.load(f)
    
    # Get pinned items
    pinned = [c for c in clips if c.get('pinned')]
    
    if not pinned:
        return {"status": "no_pinned_items"}
    
    # Format for memory storage
    memory_data = {
        "source": "QuickClip",
        "synced_at": datetime.now().isoformat(),
        "pinned_items": [
            {
                "text": p['text'],
                "timestamp": p['timestamp']
            }
            for p in pinned
        ]
    }
    
    # Save to local memory file
    memory_file = Path.home() / ".memorybridge" / "quickclip_pinned.json"
    memory_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(memory_file, 'w', encoding='utf-8') as f:
        json.dump(memory_data, f, indent=2)
    
    return {
        "status": "synced",
        "items": len(pinned),
        "file": str(memory_file)
    }


# Usage
result = sync_pinned_to_memory()
print(f"Sync status: {result['status']}")
```

---

## Pattern 8: QuickClip + PostMortem

**Use Case:** Analyze clipboard patterns in failed sessions

**Code:**

```python
import json
from pathlib import Path
from datetime import datetime

def analyze_clipboard_for_postmortem(session_start: str, session_end: str):
    """Analyze clipboard activity for post-mortem analysis."""
    
    start = datetime.fromisoformat(session_start)
    end = datetime.fromisoformat(session_end)
    
    history_file = Path.home() / ".quickclip_history.json"
    
    if not history_file.exists():
        return {"status": "no_data"}
    
    with open(history_file, 'r', encoding='utf-8') as f:
        clips = json.load(f)
    
    # Filter to session
    session_clips = []
    for clip in clips:
        try:
            clip_time = datetime.fromisoformat(clip['timestamp'])
            if start <= clip_time <= end:
                session_clips.append(clip)
        except:
            continue
    
    if not session_clips:
        return {"status": "no_clips_in_session"}
    
    # Analyze patterns
    analysis = {
        "clip_count": len(session_clips),
        "patterns": {},
        "insights": []
    }
    
    patterns = {"errors": 0, "code": 0, "urls": 0}
    
    for clip in session_clips:
        text = clip['text'].lower()
        
        if any(x in text for x in ['error', 'exception', 'traceback']):
            patterns["errors"] += 1
        if any(x in text for x in ['def ', 'class ', 'function']):
            patterns["code"] += 1
        if 'http' in text:
            patterns["urls"] += 1
    
    analysis["patterns"] = patterns
    
    if patterns["errors"] > 0:
        analysis["insights"].append(
            f"[!] {patterns['errors']} error messages - review for debugging"
        )
    
    return analysis


# Usage
analysis = analyze_clipboard_for_postmortem(
    "2026-01-15T10:00:00",
    "2026-01-15T14:00:00"
)

print(f"Clips in session: {analysis.get('clip_count', 0)}")
print(f"Patterns: {analysis.get('patterns', {})}")
```

---

## Pattern 9: Multi-Tool Workflow

**Use Case:** Complete workflow using multiple tools with QuickClip

**Code:**

```python
import json
from pathlib import Path
from datetime import datetime

def team_brain_clipboard_integration(agent: str, task: str):
    """Full Team Brain stack with QuickClip integration."""
    
    result = {
        "agent": agent,
        "task": task,
        "timestamp": datetime.now().isoformat(),
        "integrations": {}
    }
    
    # Access QuickClip data
    history_file = Path.home() / ".quickclip_history.json"
    clips = []
    
    if history_file.exists():
        with open(history_file, 'r', encoding='utf-8') as f:
            clips = json.load(f)
    
    result["clipboard"] = {
        "available": bool(clips),
        "count": len(clips),
        "pinned": sum(1 for c in clips if c.get('pinned'))
    }
    
    # Integration points
    result["integrations"]["devsnapshot"] = {
        "status": "ready",
        "data": {"clips_to_include": min(20, len(clips))}
    }
    
    result["integrations"]["contextcompressor"] = {
        "status": "ready",
        "raw_chars": sum(len(c['text']) for c in clips[:20]),
    }
    
    return result


# Usage
integration = team_brain_clipboard_integration("FORGE", "Session Review")
print(f"Clipboard: {integration['clipboard']['count']} items")
```

---

## Pattern 10: Bash Integration

**Use Case:** Command-line access to QuickClip

**Code:**

```bash
#!/bin/bash
# QuickClip Bash Integration
# Add these to your ~/.bashrc or ~/.zshrc

# View recent clips
qclips() {
    python3 -c "
import json
from pathlib import Path

clips = json.load(open(Path.home() / '.quickclip_history.json'))[:${1:-5}]
for c in clips:
    pin = '[PIN] ' if c.get('pinned') else ''
    print(f\"{pin}{c['timestamp'][:10]}: {c['text'][:60]}...\")
"
}

# Search clips
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

# Get pinned clips
qpinned() {
    python3 -c "
import json
from pathlib import Path

clips = json.load(open(Path.home() / '.quickclip_history.json'))
pinned = [c for c in clips if c.get('pinned')]
print(f'Pinned items: {len(pinned)}')
for c in pinned:
    print(f\"  {c['text'][:60]}...\")
"
}

# Quick stats
qstats() {
    python3 -c "
import json
from pathlib import Path

clips = json.load(open(Path.home() / '.quickclip_history.json'))
print(f'Total clips: {len(clips)}')
print(f'Pinned: {sum(1 for c in clips if c.get(\"pinned\"))}')
print(f'With URLs: {sum(1 for c in clips if \"http\" in c[\"text\"])}')
print(f'With code: {sum(1 for c in clips if \"def \" in c[\"text\"])}')
"
}
```

**Usage:**
```bash
# View 5 recent clips
qclips 5

# Search for "api"
qfind api

# View pinned items
qpinned

# View stats
qstats
```

---

## TROUBLESHOOTING

**Import Errors:**
```python
from pathlib import Path
history = Path.home() / ".quickclip_history.json"
print(f"Path exists: {history.exists()}")
```

**JSON Errors:**
```python
try:
    with open(history_file) as f:
        clips = json.load(f)
except json.JSONDecodeError:
    clips = []
    print("[!] QuickClip history corrupted")
```

---

**Last Updated:** February 1, 2026  
**Maintained By:** FORGE (Team Brain)
