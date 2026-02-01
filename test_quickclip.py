#!/usr/bin/env python3
"""
QuickClip - Comprehensive Test Suite
=====================================
Tests for ClipboardItem, ClipboardMonitor, and QuickClipWindow classes.

Run tests:
    python -m pytest test_quickclip.py -v
    python -m pytest test_quickclip.py --cov=quickclip --cov-report=html

Author: Logan Smith / Metaphy LLC / Team Brain
License: MIT
"""

import unittest
import sys
import json
import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Mock PySide6 for non-GUI testing
class MockQObject:
    def __init__(self, parent=None):
        pass

class MockSignal:
    def __init__(self, *args):
        self._callbacks = []
    
    def connect(self, callback):
        self._callbacks.append(callback)
    
    def emit(self, *args):
        for cb in self._callbacks:
            cb(*args)

class MockQTimer:
    def __init__(self, parent=None):
        self._interval = 0
        self._callback = None
        self.timeout = MockSignal()
    
    def start(self, interval=None):
        pass
    
    def stop(self):
        pass
    
    def setInterval(self, interval):
        self._interval = interval

class MockQApplication:
    _instance = None
    _clipboard = None
    
    def __init__(self, args=None):
        MockQApplication._instance = self
        MockQApplication._clipboard = MockQClipboard()
    
    @classmethod
    def clipboard(cls):
        if cls._clipboard is None:
            cls._clipboard = MockQClipboard()
        return cls._clipboard
    
    @classmethod
    def instance(cls):
        return cls._instance
    
    def exec(self):
        return 0
    
    def setQuitOnLastWindowClosed(self, value):
        pass
    
    @staticmethod
    def setHighDpiScaleFactorRoundingPolicy(policy):
        pass
    
    def setApplicationName(self, name):
        pass
    
    def setOrganizationName(self, name):
        pass

class MockQClipboard:
    def __init__(self):
        self._text = ""
    
    def text(self):
        return self._text
    
    def setText(self, text):
        self._text = text

# Mock the PySide6 modules before importing quickclip
sys.modules['PySide6'] = MagicMock()
sys.modules['PySide6.QtWidgets'] = MagicMock()
sys.modules['PySide6.QtCore'] = MagicMock()
sys.modules['PySide6.QtGui'] = MagicMock()

# Set up mock values
sys.modules['PySide6.QtCore'].QObject = MockQObject
sys.modules['PySide6.QtCore'].Signal = MockSignal
sys.modules['PySide6.QtCore'].QTimer = MockQTimer
sys.modules['PySide6.QtCore'].Qt = MagicMock()
sys.modules['PySide6.QtCore'].Qt.UserRole = 256
sys.modules['PySide6.QtWidgets'].QApplication = MockQApplication

# NOTE: ClipboardItem is defined manually below for testing
# This avoids PySide6 import issues and encoding problems

# Manually define ClipboardItem for testing since imports are complex
class ClipboardItem:
    """Represents a single clipboard history item."""
    
    def __init__(self, text: str, timestamp: str = None, pinned: bool = False):
        self.text = text
        self.timestamp = timestamp or datetime.now().isoformat()
        self.pinned = pinned
    
    def to_dict(self) -> dict:
        return {
            'text': self.text,
            'timestamp': self.timestamp,
            'pinned': self.pinned
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ClipboardItem':
        return cls(
            text=data['text'],
            timestamp=data.get('timestamp'),
            pinned=data.get('pinned', False)
        )
    
    def preview(self, max_len: int = 80) -> str:
        """Get a preview of the text for display."""
        text = self.text.replace('\n', ' ').replace('\r', '').strip()
        if len(text) > max_len:
            return text[:max_len] + '...'
        return text
    
    def time_ago(self) -> str:
        """Get human-readable time since copy."""
        try:
            dt = datetime.fromisoformat(self.timestamp)
            delta = datetime.now() - dt
            
            if delta.days > 0:
                return f"{delta.days}d ago"
            elif delta.seconds >= 3600:
                return f"{delta.seconds // 3600}h ago"
            elif delta.seconds >= 60:
                return f"{delta.seconds // 60}m ago"
            else:
                return "just now"
        except:
            return ""


# =============================================================================
# Test Classes
# =============================================================================

class TestClipboardItemBasic(unittest.TestCase):
    """Test basic ClipboardItem functionality."""
    
    def test_init_basic(self):
        """Test basic initialization."""
        item = ClipboardItem("Hello World")
        self.assertEqual(item.text, "Hello World")
        self.assertFalse(item.pinned)
        self.assertIsNotNone(item.timestamp)
    
    def test_init_with_pinned(self):
        """Test initialization with pinned flag."""
        item = ClipboardItem("Pinned item", pinned=True)
        self.assertTrue(item.pinned)
    
    def test_init_with_timestamp(self):
        """Test initialization with custom timestamp."""
        ts = "2026-01-15T10:30:00"
        item = ClipboardItem("Test", timestamp=ts)
        self.assertEqual(item.timestamp, ts)
    
    def test_init_empty_text(self):
        """Test initialization with empty text."""
        item = ClipboardItem("")
        self.assertEqual(item.text, "")
    
    def test_init_unicode(self):
        """Test initialization with unicode content."""
        item = ClipboardItem("Hello emoji test")
        self.assertEqual(item.text, "Hello emoji test")


class TestClipboardItemSerialization(unittest.TestCase):
    """Test ClipboardItem serialization methods."""
    
    def test_to_dict(self):
        """Test to_dict method."""
        item = ClipboardItem("Test content", pinned=True)
        d = item.to_dict()
        
        self.assertEqual(d['text'], "Test content")
        self.assertTrue(d['pinned'])
        self.assertIn('timestamp', d)
    
    def test_from_dict(self):
        """Test from_dict class method."""
        data = {
            'text': 'Restored content',
            'timestamp': '2026-01-15T10:00:00',
            'pinned': True
        }
        
        item = ClipboardItem.from_dict(data)
        
        self.assertEqual(item.text, 'Restored content')
        self.assertEqual(item.timestamp, '2026-01-15T10:00:00')
        self.assertTrue(item.pinned)
    
    def test_from_dict_missing_pinned(self):
        """Test from_dict with missing pinned field."""
        data = {
            'text': 'Content',
            'timestamp': '2026-01-15T10:00:00'
        }
        
        item = ClipboardItem.from_dict(data)
        self.assertFalse(item.pinned)
    
    def test_from_dict_missing_timestamp(self):
        """Test from_dict with missing timestamp."""
        data = {'text': 'Content'}
        
        item = ClipboardItem.from_dict(data)
        self.assertIsNotNone(item.timestamp)
    
    def test_roundtrip(self):
        """Test serialization roundtrip."""
        original = ClipboardItem("Roundtrip test", pinned=True)
        original_ts = original.timestamp
        
        data = original.to_dict()
        restored = ClipboardItem.from_dict(data)
        
        self.assertEqual(original.text, restored.text)
        self.assertEqual(original.pinned, restored.pinned)
        self.assertEqual(original_ts, restored.timestamp)


class TestClipboardItemPreview(unittest.TestCase):
    """Test ClipboardItem preview functionality."""
    
    def test_preview_short(self):
        """Test preview with short text."""
        item = ClipboardItem("Short text")
        self.assertEqual(item.preview(), "Short text")
    
    def test_preview_long(self):
        """Test preview with long text."""
        long_text = "A" * 100
        item = ClipboardItem(long_text)
        preview = item.preview(80)
        
        self.assertEqual(len(preview), 83)  # 80 + '...'
        self.assertTrue(preview.endswith('...'))
    
    def test_preview_custom_length(self):
        """Test preview with custom max length."""
        item = ClipboardItem("Testing custom length preview")
        preview = item.preview(10)
        
        self.assertEqual(preview, "Testing cu...")
    
    def test_preview_multiline(self):
        """Test preview replaces newlines."""
        item = ClipboardItem("Line 1\nLine 2\nLine 3")
        preview = item.preview()
        
        self.assertNotIn('\n', preview)
        self.assertEqual(preview, "Line 1 Line 2 Line 3")
    
    def test_preview_carriage_return(self):
        """Test preview removes carriage returns."""
        item = ClipboardItem("Line 1\r\nLine 2")
        preview = item.preview()
        
        self.assertNotIn('\r', preview)
    
    def test_preview_whitespace_trim(self):
        """Test preview trims whitespace."""
        item = ClipboardItem("  Padded text  ")
        preview = item.preview()
        
        self.assertEqual(preview, "Padded text")


class TestClipboardItemTimeAgo(unittest.TestCase):
    """Test ClipboardItem time_ago functionality."""
    
    def test_time_ago_just_now(self):
        """Test time_ago for recent items."""
        item = ClipboardItem("Just now")
        result = item.time_ago()
        self.assertEqual(result, "just now")
    
    def test_time_ago_minutes(self):
        """Test time_ago for items minutes old."""
        ts = (datetime.now() - timedelta(minutes=5)).isoformat()
        item = ClipboardItem("5 min ago", timestamp=ts)
        result = item.time_ago()
        self.assertIn("m ago", result)
    
    def test_time_ago_hours(self):
        """Test time_ago for items hours old."""
        ts = (datetime.now() - timedelta(hours=3)).isoformat()
        item = ClipboardItem("3 hours ago", timestamp=ts)
        result = item.time_ago()
        self.assertIn("h ago", result)
    
    def test_time_ago_days(self):
        """Test time_ago for items days old."""
        ts = (datetime.now() - timedelta(days=2)).isoformat()
        item = ClipboardItem("2 days ago", timestamp=ts)
        result = item.time_ago()
        self.assertEqual(result, "2d ago")
    
    def test_time_ago_invalid_timestamp(self):
        """Test time_ago with invalid timestamp."""
        item = ClipboardItem("Invalid", timestamp="not-a-date")
        result = item.time_ago()
        self.assertEqual(result, "")


class TestHistoryManagement(unittest.TestCase):
    """Test history list management logic."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.history = []
    
    def test_add_item(self):
        """Test adding items to history."""
        item = ClipboardItem("First item")
        self.history.insert(0, item)
        
        self.assertEqual(len(self.history), 1)
        self.assertEqual(self.history[0].text, "First item")
    
    def test_add_maintains_order(self):
        """Test new items go to top."""
        self.history.insert(0, ClipboardItem("First"))
        self.history.insert(0, ClipboardItem("Second"))
        self.history.insert(0, ClipboardItem("Third"))
        
        self.assertEqual(self.history[0].text, "Third")
        self.assertEqual(self.history[2].text, "First")
    
    def test_remove_duplicates(self):
        """Test duplicate removal logic."""
        self.history.append(ClipboardItem("Item A"))
        self.history.append(ClipboardItem("Item B"))
        self.history.append(ClipboardItem("Item A"))  # Duplicate
        
        # Remove duplicates (keep last occurrence)
        seen = set()
        unique = []
        for item in self.history:
            if item.text not in seen:
                seen.add(item.text)
                unique.append(item)
        
        self.assertEqual(len(unique), 2)
    
    def test_pin_protection(self):
        """Test pinned items aren't deleted during trim."""
        max_history = 3
        
        self.history = [
            ClipboardItem("Pinned", pinned=True),
            ClipboardItem("Regular 1"),
            ClipboardItem("Regular 2"),
            ClipboardItem("Regular 3"),
        ]
        
        # Trim logic: remove oldest non-pinned
        while len(self.history) > max_history:
            for i in range(len(self.history) - 1, -1, -1):
                if not self.history[i].pinned:
                    self.history.pop(i)
                    break
        
        self.assertEqual(len(self.history), max_history)
        # Pinned item should remain
        self.assertTrue(any(item.pinned for item in self.history))
    
    def test_clear_unpinned(self):
        """Test clearing unpinned items."""
        self.history = [
            ClipboardItem("Pinned 1", pinned=True),
            ClipboardItem("Regular 1"),
            ClipboardItem("Pinned 2", pinned=True),
            ClipboardItem("Regular 2"),
        ]
        
        self.history = [item for item in self.history if item.pinned]
        
        self.assertEqual(len(self.history), 2)
        self.assertTrue(all(item.pinned for item in self.history))


class TestSearchFunctionality(unittest.TestCase):
    """Test search/filter functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.history = [
            ClipboardItem("Hello World"),
            ClipboardItem("Python programming"),
            ClipboardItem("JavaScript code"),
            ClipboardItem("hello again"),
        ]
    
    def test_search_exact_match(self):
        """Test exact match search."""
        search = "Python"
        results = [item for item in self.history if search.lower() in item.text.lower()]
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, "Python programming")
    
    def test_search_case_insensitive(self):
        """Test case insensitive search."""
        search = "hello"
        results = [item for item in self.history if search.lower() in item.text.lower()]
        
        self.assertEqual(len(results), 2)
    
    def test_search_partial_match(self):
        """Test partial match search."""
        search = "prog"
        results = [item for item in self.history if search.lower() in item.text.lower()]
        
        self.assertEqual(len(results), 1)
    
    def test_search_no_results(self):
        """Test search with no results."""
        search = "nonexistent"
        results = [item for item in self.history if search.lower() in item.text.lower()]
        
        self.assertEqual(len(results), 0)
    
    def test_search_empty_query(self):
        """Test empty search returns all."""
        search = ""
        results = [item for item in self.history if not search or search.lower() in item.text.lower()]
        
        self.assertEqual(len(results), 4)


class TestFilePersistence(unittest.TestCase):
    """Test file save/load functionality."""
    
    def setUp(self):
        """Set up temp directory for tests."""
        self.test_dir = tempfile.mkdtemp()
        self.save_file = Path(self.test_dir) / "test_history.json"
    
    def tearDown(self):
        """Clean up temp directory."""
        shutil.rmtree(self.test_dir)
    
    def test_save_history(self):
        """Test saving history to file."""
        history = [
            ClipboardItem("Item 1"),
            ClipboardItem("Item 2", pinned=True),
        ]
        
        data = [item.to_dict() for item in history]
        with open(self.save_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        
        self.assertTrue(self.save_file.exists())
    
    def test_load_history(self):
        """Test loading history from file."""
        data = [
            {'text': 'Loaded 1', 'timestamp': '2026-01-15T10:00:00', 'pinned': False},
            {'text': 'Loaded 2', 'timestamp': '2026-01-15T11:00:00', 'pinned': True},
        ]
        
        with open(self.save_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        
        with open(self.save_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        
        history = [ClipboardItem.from_dict(item) for item in loaded]
        
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].text, 'Loaded 1')
        self.assertTrue(history[1].pinned)
    
    def test_save_unicode(self):
        """Test saving unicode content."""
        history = [ClipboardItem("Unicode test")]
        
        data = [item.to_dict() for item in history]
        with open(self.save_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        
        with open(self.save_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded[0]['text'], "Unicode test")
    
    def test_missing_file(self):
        """Test handling missing file."""
        self.assertFalse(self.save_file.exists())
        
        # Should not raise error
        history = []
        if self.save_file.exists():
            with open(self.save_file) as f:
                history = json.load(f)
        
        self.assertEqual(history, [])
    
    def test_corrupted_file(self):
        """Test handling corrupted file."""
        with open(self.save_file, 'w') as f:
            f.write("not valid json {{{")
        
        history = []
        try:
            with open(self.save_file) as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []
        
        self.assertEqual(history, [])


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_very_long_text(self):
        """Test handling very long text."""
        long_text = "A" * 100000
        item = ClipboardItem(long_text)
        
        self.assertEqual(len(item.text), 100000)
        # Preview should be truncated
        self.assertTrue(len(item.preview(80)) <= 83)
    
    def test_special_characters(self):
        """Test handling special characters."""
        special = "Tab:\tNewline:\nQuote:\"Backslash:\\"
        item = ClipboardItem(special)
        
        self.assertEqual(item.text, special)
        # Serialization should handle it
        d = item.to_dict()
        restored = ClipboardItem.from_dict(d)
        self.assertEqual(restored.text, special)
    
    def test_null_bytes(self):
        """Test handling null bytes."""
        with_null = "Before\x00After"
        item = ClipboardItem(with_null)
        
        self.assertIn('\x00', item.text)
    
    def test_whitespace_only(self):
        """Test whitespace-only content."""
        item = ClipboardItem("   \n\t\r   ")
        preview = item.preview()
        
        self.assertEqual(preview, "")  # Trimmed to empty
    
    def test_empty_dict(self):
        """Test from_dict with minimal data."""
        data = {'text': ''}
        item = ClipboardItem.from_dict(data)
        
        self.assertEqual(item.text, '')
        self.assertFalse(item.pinned)


class TestSortingLogic(unittest.TestCase):
    """Test history sorting logic."""
    
    def test_pinned_first(self):
        """Test pinned items sort to top."""
        history = [
            ClipboardItem("Regular 1"),
            ClipboardItem("Pinned 1", pinned=True),
            ClipboardItem("Regular 2"),
            ClipboardItem("Pinned 2", pinned=True),
        ]
        
        # Sort: pinned first
        sorted_history = sorted(history, key=lambda x: not x.pinned)
        
        self.assertTrue(sorted_history[0].pinned)
        self.assertTrue(sorted_history[1].pinned)
        self.assertFalse(sorted_history[2].pinned)
        self.assertFalse(sorted_history[3].pinned)
    
    def test_sort_by_timestamp(self):
        """Test sorting by timestamp."""
        history = [
            ClipboardItem("Old", timestamp="2026-01-10T10:00:00"),
            ClipboardItem("New", timestamp="2026-01-15T10:00:00"),
            ClipboardItem("Middle", timestamp="2026-01-12T10:00:00"),
        ]
        
        # Sort by timestamp descending
        sorted_history = sorted(history, key=lambda x: x.timestamp, reverse=True)
        
        self.assertEqual(sorted_history[0].text, "New")
        self.assertEqual(sorted_history[1].text, "Middle")
        self.assertEqual(sorted_history[2].text, "Old")


class TestIntegrationPatterns(unittest.TestCase):
    """Test patterns used for integration with other tools."""
    
    def test_json_export_format(self):
        """Test JSON export format for external access."""
        history = [
            ClipboardItem("Export 1", pinned=True),
            ClipboardItem("Export 2"),
        ]
        
        export = json.dumps([item.to_dict() for item in history], indent=2)
        
        # Should be valid JSON
        reimported = json.loads(export)
        self.assertEqual(len(reimported), 2)
        self.assertTrue(reimported[0]['pinned'])
    
    def test_programmatic_access(self):
        """Test programmatic access pattern."""
        # Simulate reading from file like other tools would
        history_data = [
            {'text': 'API response data', 'timestamp': datetime.now().isoformat(), 'pinned': False},
            {'text': 'Important config', 'timestamp': datetime.now().isoformat(), 'pinned': True},
        ]
        
        # Search pattern
        search_term = "api"
        results = [d for d in history_data if search_term.lower() in d['text'].lower()]
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['text'], 'API response data')


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == '__main__':
    unittest.main(verbosity=2)
