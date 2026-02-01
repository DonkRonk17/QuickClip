# QuickClip - Integration Plan

**Goal:** 100% Utilization & Compliance  
**Target Date:** 1 week from deployment  
**Owner:** FORGE (Team Brain)

---

## INTEGRATION GOALS

This document outlines how QuickClip integrates with:
1. Team Brain agents (Forge, Atlas, Clio, Nexus, Bolt)
2. Existing Team Brain tools
3. BCH (Beacon Command Hub) - if applicable
4. Logan's workflows

| Goal | Target | Metric |
|------|--------|--------|
| BCH Integration | Not Applicable | GUI tool, no BCH commands |
| AI Agent Adoption | 100% | 5/5 agents aware/using |
| Daily Usage | Active | Running in background |
| Data Access | Programmatic | JSON history readable |

---

## BCH INTEGRATION

### Overview

QuickClip is a **GUI application** designed for direct human interaction. Unlike CLI tools, it does not integrate directly into BCH as a @mention command.

**Why BCH Integration is Not Applicable:**
- QuickClip runs as a background desktop application
- Clipboard operations are user-driven
- No meaningful way to expose clipboard history via chat commands

### Alternative Integration Points

Instead of BCH commands, QuickClip integrates via:

1. **Data Access:** BCH can read QuickClip history JSON for context
2. **User Workflow:** Agents can instruct users to check QuickClip
3. **DevSnapshot Integration:** QuickClip state can be captured

**Example BCH Reference:**
```
User: "What was that config value I copied?"
BCH: "Check your QuickClip history - search for 'config'"
     "QuickClip stores history at: ~/.quickclip_history.json"
```

---

## AI AGENT INTEGRATION

### Integration Matrix

| Agent | Use Case | Integration Method | Priority |
|-------|----------|-------------------|----------|
| **Forge** | Context recovery, copied content lookup | Data file access | MEDIUM |
| **Atlas** | Build session clipboard tracking | Data file access | HIGH |
| **Clio** | Linux clipboard history access | Data file access | HIGH |
| **Nexus** | Cross-platform clipboard coordination | Data file access | MEDIUM |
| **Bolt** | Task execution context | Data file access | LOW |

### Agent-Specific Workflows

#### Forge (Orchestrator / Reviewer)

**Primary Use Case:** Recovering copied context during session reviews

**Integration Steps:**
1. When debugging a failed session, check QuickClip history
2. Use history to reconstruct what user/agents were working with
3. Reference copied code, URLs, or error messages

**Example Workflow:**
```python
import json
from pathlib import Path

def get_recent_clips(count=10):
    """Get recent clipboard items for context."""
    history_file = Path.home() / ".quickclip_history.json"
    
    if not history_file.exists():
        return []
    
    with open(history_file, 'r', encoding='utf-8') as f:
        clips = json.load(f)
    
    return clips[:count]

# Usage during session review
recent = get_recent_clips(5)
for clip in recent:
    print(f"[{clip['timestamp'][:16]}] {clip['text'][:80]}...")
```

**When to Reference QuickClip:**
- User mentions "I copied that somewhere"
- Debugging failed operations
- Reconstructing session context

---

#### Atlas (Executor / Builder)

**Primary Use Case:** Tracking code snippets during tool builds

**Integration Steps:**
1. Run QuickClip during build sessions
2. Pin important code snippets
3. Search history when refactoring

**Example Workflow:**
```python
import json
from pathlib import Path
from datetime import datetime, timedelta

def find_code_clips(hours_back=4):
    """Find code-like clips from recent session."""
    history_file = Path.home() / ".quickclip_history.json"
    
    with open(history_file, 'r', encoding='utf-8') as f:
        clips = json.load(f)
    
    # Filter by time and content
    cutoff = datetime.now() - timedelta(hours=hours_back)
    code_indicators = ['def ', 'class ', 'import ', 'function', 'const ', '{', '}']
    
    results = []
    for clip in clips:
        try:
            clip_time = datetime.fromisoformat(clip['timestamp'])
            if clip_time > cutoff:
                if any(ind in clip['text'] for ind in code_indicators):
                    results.append(clip)
        except:
            continue
    
    return results

# Find code from this build session
code_clips = find_code_clips(4)
print(f"Found {len(code_clips)} code snippets from session")
```

---

#### Clio (Linux / Ubuntu Agent)

**Primary Use Case:** Persistent clipboard history on Linux

**Setup for Linux:**
```bash
# Install on Linux
pip3 install PySide6
python3 quickclip.py &

# Auto-start (add to ~/.bashrc or systemd)
echo "python3 ~/AutoProjects/QuickClip/quickclip.py &" >> ~/.profile
```

**Example CLI Access:**
```bash
# Quick clipboard history from terminal
cat ~/.quickclip_history.json | python3 -c "
import json, sys
clips = json.load(sys.stdin)[:5]
for c in clips:
    pin = '📌 ' if c.get('pinned') else ''
    print(f'{pin}{c[\"timestamp\"][:10]}: {c[\"text\"][:60]}...')
"
```

---

#### Nexus (Multi-Platform Agent)

**Primary Use Case:** Cross-platform clipboard context

**Cross-Platform Script:**
```python
import json
import platform
from pathlib import Path

def get_quickclip_path():
    """Get QuickClip data path for any platform."""
    return Path.home() / ".quickclip_history.json"

def get_clips_cross_platform():
    """Get clips on any platform."""
    history_file = get_quickclip_path()
    
    if not history_file.exists():
        return f"No QuickClip history on {platform.system()}"
    
    with open(history_file, 'r', encoding='utf-8') as f:
        clips = json.load(f)
    
    return f"Platform: {platform.system()}, Clips: {len(clips)}"

print(get_clips_cross_platform())
```

---

#### Bolt (Cline / Free Executor)

**Primary Use Case:** Context from clipboard during task execution

**Cost-Free Access:**
```bash
# Quick check of recent clips (free, no API)
python -c "
import json
from pathlib import Path

clips = json.load(open(Path.home() / '.quickclip_history.json'))[:3]
print('Recent clipboard context:')
for c in clips:
    print(f'  - {c[\"text\"][:100]}')
"
```

---

## INTEGRATION WITH OTHER TEAM BRAIN TOOLS

### With DevSnapshot

```python
def capture_with_clipboard():
    """Capture dev snapshot including clipboard history."""
    import json
    from pathlib import Path
    from datetime import datetime
    
    history_file = Path.home() / ".quickclip_history.json"
    
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "type": "dev_snapshot",
        "clipboard": {}
    }
    
    if history_file.exists():
        with open(history_file) as f:
            clips = json.load(f)
        
        snapshot["clipboard"] = {
            "total": len(clips),
            "pinned": sum(1 for c in clips if c.get('pinned')),
            "recent": clips[:10]
        }
    
    return snapshot
```

### With SynapseLink

```python
def alert_clipboard_patterns():
    """Alert on clipboard patterns via SynapseLink."""
    from synapselink import quick_send
    import json
    from pathlib import Path
    
    history_file = Path.home() / ".quickclip_history.json"
    
    with open(history_file) as f:
        clips = json.load(f)
    
    # Check for patterns
    secrets = [c for c in clips[:50] 
               if any(p in c['text'].lower() 
                      for p in ['api_key', 'secret', 'password'])]
    
    if secrets:
        quick_send(
            "FORGE",
            "QuickClip Pattern Alert",
            f"Found {len(secrets)} potential secrets in clipboard",
            priority="NORMAL"
        )
```

### With ContextCompressor

```python
def get_compressed_clipboard_context(max_chars=2000):
    """Get token-efficient clipboard summary."""
    import json
    from pathlib import Path
    
    history_file = Path.home() / ".quickclip_history.json"
    
    with open(history_file) as f:
        clips = json.load(f)
    
    lines = [f"CLIPBOARD CONTEXT: {len(clips)} items"]
    
    # Pinned first
    pinned = [c for c in clips if c.get('pinned')]
    if pinned:
        lines.append("PINNED:")
        for p in pinned[:3]:
            lines.append(f"  - {p['text'][:80]}...")
    
    # Recent
    lines.append("RECENT:")
    for c in clips[:5]:
        lines.append(f"  [{c['timestamp'][:10]}] {c['text'][:60]}...")
    
    context = "\n".join(lines)
    return context[:max_chars]
```

---

## ADOPTION ROADMAP

### Phase 1: Core Adoption (Week 1)

**Goal:** All agents aware and can access clipboard data

**Steps:**
1. [x] Tool deployed to GitHub
2. [ ] Quick-start guides sent via Synapse
3. [ ] Each agent tests data access
4. [ ] Feedback collected

### Phase 2: Integration (Week 2-3)

**Goal:** Integrated into relevant workflows

**Steps:**
1. [ ] Add to DevSnapshot context
2. [ ] Create clipboard health check
3. [ ] Document common use cases
4. [ ] Monitor usage patterns

### Phase 3: Optimization (Week 4+)

**Goal:** Optimized and fully adopted

**Steps:**
1. [ ] Collect usage metrics
2. [ ] Plan v1.1 improvements
3. [ ] Add requested features
4. [ ] Full ecosystem integration

---

## SUCCESS METRICS

**Adoption Metrics:**
- Number of agents accessing data: [Track]
- Integration patterns used: [Track]
- User feedback: [Qualitative]

**Efficiency Metrics:**
- Context recovery time: [Estimate: saves 5-10 min/session]
- Information retrieval: [Clips found vs manual search]

---

## TECHNICAL DETAILS

### Data Access

**History File Path:**
```python
from pathlib import Path
history_file = Path.home() / ".quickclip_history.json"
```

**History Format:**
```json
[
  {
    "text": "Copied content",
    "timestamp": "2026-01-15T10:30:00.123456",
    "pinned": false
  }
]
```

### Error Handling

```python
def safe_get_clips():
    """Safely get clips with error handling."""
    from pathlib import Path
    import json
    
    history = Path.home() / ".quickclip_history.json"
    
    try:
        if not history.exists():
            return {"error": "QuickClip not found"}
        
        with open(history, 'r', encoding='utf-8') as f:
            clips = json.load(f)
        
        return {"clips": clips, "count": len(clips)}
    
    except json.JSONDecodeError:
        return {"error": "Corrupted history file"}
    except Exception as e:
        return {"error": str(e)}
```

---

## MAINTENANCE

### Update Strategy
- Minor updates (v1.x): As needed
- Bug fixes: Immediate

### Known Limitations
- GUI only (no CLI interface)
- Single-machine (no sync)
- Text only (no images)

---

## ADDITIONAL RESOURCES

- Main Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Quick Start Guides: [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- GitHub: https://github.com/DonkRonk17/QuickClip

---

**Last Updated:** February 1, 2026  
**Maintained By:** FORGE (Team Brain)
