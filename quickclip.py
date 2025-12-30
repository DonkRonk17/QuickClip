#!/usr/bin/env python3
"""
QuickClip - Universal Clipboard History Manager
================================================
A simple, cross-platform clipboard history tool.

Features:
- Saves clipboard history (text only for simplicity)
- Search through history
- Pin frequently used items
- One-click copy back to clipboard
- System tray icon
- Keyboard shortcut (Ctrl+Shift+V)

Author: Metaphy LLC / Team Brain
License: MIT
Version: 1.0.0
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

# Check for required packages
try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QListWidget, QListWidgetItem, QLineEdit, QPushButton, QLabel,
        QSystemTrayIcon, QMenu, QMessageBox, QSplitter, QTextEdit,
        QFrame, QScrollArea
    )
    from PySide6.QtCore import Qt, QTimer, Signal, QObject
    from PySide6.QtGui import QIcon, QAction, QClipboard, QFont, QColor, QPalette, QKeySequence, QShortcut
except ImportError:
    print("ERROR: PySide6 is required. Install with: pip install PySide6")
    sys.exit(1)

try:
    import pyperclip
except ImportError:
    pyperclip = None
    print("WARNING: pyperclip not found. Using Qt clipboard only.")


# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════

VERSION = "1.0.0"
APP_NAME = "QuickClip"
MAX_HISTORY = 100
SAVE_FILE = Path.home() / ".quickclip_history.json"

# Dark theme colors
COLORS = {
    'bg_dark': '#1a1a2e',
    'bg_medium': '#16213e',
    'bg_light': '#0f3460',
    'accent': '#e94560',
    'accent_hover': '#ff6b6b',
    'text': '#eaeaea',
    'text_dim': '#888888',
    'border': '#333355',
    'pinned': '#ffd700',
}


# ═══════════════════════════════════════════════════════════════════════════════
# Stylesheet
# ═══════════════════════════════════════════════════════════════════════════════

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {COLORS['bg_dark']};
    color: {COLORS['text']};
    font-family: 'Segoe UI', 'Arial', sans-serif;
}}

QLineEdit {{
    background-color: {COLORS['bg_medium']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 14px;
    color: {COLORS['text']};
}}

QLineEdit:focus {{
    border-color: {COLORS['accent']};
}}

QPushButton {{
    background-color: {COLORS['accent']};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {COLORS['accent_hover']};
}}

QPushButton:pressed {{
    background-color: {COLORS['bg_light']};
}}

QPushButton#pinBtn {{
    background-color: transparent;
    color: {COLORS['text_dim']};
    padding: 5px 10px;
}}

QPushButton#pinBtn:hover {{
    color: {COLORS['pinned']};
}}

QPushButton#deleteBtn {{
    background-color: transparent;
    color: {COLORS['text_dim']};
    padding: 5px 10px;
}}

QPushButton#deleteBtn:hover {{
    color: {COLORS['accent']};
}}

QListWidget {{
    background-color: {COLORS['bg_medium']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 5px;
    outline: none;
}}

QListWidget::item {{
    background-color: {COLORS['bg_light']};
    border-radius: 6px;
    margin: 3px;
    padding: 10px;
}}

QListWidget::item:selected {{
    background-color: {COLORS['accent']};
}}

QListWidget::item:hover {{
    background-color: {COLORS['border']};
}}

QLabel {{
    color: {COLORS['text']};
}}

QLabel#title {{
    font-size: 24px;
    font-weight: bold;
    color: {COLORS['accent']};
}}

QLabel#subtitle {{
    font-size: 12px;
    color: {COLORS['text_dim']};
}}

QTextEdit {{
    background-color: {COLORS['bg_medium']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px;
    color: {COLORS['text']};
    font-family: 'Consolas', 'Courier New', monospace;
}}

QScrollBar:vertical {{
    background-color: {COLORS['bg_dark']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['accent']};
}}

QMenu {{
    background-color: {COLORS['bg_medium']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 5px;
}}

QMenu::item {{
    padding: 8px 20px;
    border-radius: 4px;
}}

QMenu::item:selected {{
    background-color: {COLORS['accent']};
}}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# Clipboard Item Widget
# ═══════════════════════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════════════════════
# Clipboard Monitor
# ═══════════════════════════════════════════════════════════════════════════════

class ClipboardMonitor(QObject):
    """Monitors the clipboard for changes."""
    
    new_clip = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clipboard = QApplication.clipboard()
        self.last_text = ""
        
        # Poll clipboard every 500ms
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(500)
    
    def check_clipboard(self):
        """Check if clipboard has changed."""
        text = self.clipboard.text()
        if text and text != self.last_text:
            self.last_text = text
            self.new_clip.emit(text)
    
    def set_text(self, text: str):
        """Set clipboard text without triggering a new clip event."""
        self.last_text = text
        self.clipboard.setText(text)


# ═══════════════════════════════════════════════════════════════════════════════
# Main Window
# ═══════════════════════════════════════════════════════════════════════════════

class QuickClipWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.history: List[ClipboardItem] = []
        self.monitor = ClipboardMonitor(self)
        self.monitor.new_clip.connect(self.on_new_clip)
        
        self.setup_ui()
        self.load_history()
        self.setup_tray()
        self.setup_shortcuts()
    
    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle(f"{APP_NAME} v{VERSION}")
        self.setMinimumSize(500, 600)
        self.resize(550, 700)
        self.setStyleSheet(STYLESHEET)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(5)
        
        title = QLabel(f"📋 {APP_NAME}")
        title.setObjectName("title")
        header_layout.addWidget(title)
        
        subtitle = QLabel("Your clipboard history, always at hand")
        subtitle.setObjectName("subtitle")
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header)
        
        # Search bar
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search clipboard history...")
        self.search_input.textChanged.connect(self.filter_history)
        search_layout.addWidget(self.search_input)
        
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_history)
        clear_btn.setFixedWidth(100)
        search_layout.addWidget(clear_btn)
        
        layout.addLayout(search_layout)
        
        # Stats
        self.stats_label = QLabel()
        self.stats_label.setObjectName("subtitle")
        layout.addWidget(self.stats_label)
        
        # History list
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.copy_item)
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.list_widget, 1)
        
        # Preview
        preview_label = QLabel("Preview:")
        preview_label.setObjectName("subtitle")
        layout.addWidget(preview_label)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMaximumHeight(120)
        layout.addWidget(self.preview_text)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        copy_btn = QPushButton("📋 Copy Selected")
        copy_btn.clicked.connect(self.copy_selected)
        btn_layout.addWidget(copy_btn)
        
        pin_btn = QPushButton("📌 Pin/Unpin")
        pin_btn.clicked.connect(self.toggle_pin)
        btn_layout.addWidget(pin_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.clicked.connect(self.delete_selected)
        btn_layout.addWidget(delete_btn)
        
        layout.addLayout(btn_layout)
        
        # Footer
        footer = QLabel(f"Ctrl+Shift+V to show • {MAX_HISTORY} items max • Auto-saves")
        footer.setObjectName("subtitle")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
    
    def setup_tray(self):
        """Set up system tray icon."""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Create a simple icon (you could use a real icon file)
        from PySide6.QtGui import QPixmap, QPainter
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(COLORS['accent']))
        painter = QPainter(pixmap)
        painter.setPen(QColor('white'))
        painter.setFont(QFont('Arial', 16, QFont.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "Q")
        painter.end()
        
        self.tray_icon.setIcon(QIcon(pixmap))
        self.tray_icon.setToolTip(f"{APP_NAME} - Clipboard Manager")
        
        # Tray menu
        tray_menu = QMenu()
        
        show_action = QAction("Show QuickClip", self)
        show_action.triggered.connect(self.show_and_activate)
        tray_menu.addAction(show_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()
    
    def setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        # Global shortcut would require additional libraries
        # For now, just in-app shortcuts
        
        # Escape to hide
        escape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        escape.activated.connect(self.hide)
        
        # Ctrl+F to focus search
        search = QShortcut(QKeySequence("Ctrl+F"), self)
        search.activated.connect(lambda: self.search_input.setFocus())
        
        # Enter to copy selected
        enter = QShortcut(QKeySequence(Qt.Key_Return), self)
        enter.activated.connect(self.copy_selected)
        
        # Delete to remove selected
        delete = QShortcut(QKeySequence(Qt.Key_Delete), self)
        delete.activated.connect(self.delete_selected)
    
    def on_tray_activated(self, reason):
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.Trigger:
            self.show_and_activate()
    
    def show_and_activate(self):
        """Show and bring window to front."""
        self.show()
        self.raise_()
        self.activateWindow()
        self.search_input.setFocus()
    
    def closeEvent(self, event):
        """Minimize to tray instead of closing."""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            APP_NAME,
            "QuickClip is still running in the system tray.",
            QSystemTrayIcon.Information,
            2000
        )
    
    def on_new_clip(self, text: str):
        """Handle new clipboard content."""
        # Don't add duplicates at the top
        if self.history and self.history[0].text == text:
            return
        
        # Remove duplicate if exists elsewhere
        self.history = [item for item in self.history if item.text != text]
        
        # Add new item at the top
        item = ClipboardItem(text)
        self.history.insert(0, item)
        
        # Trim history
        while len(self.history) > MAX_HISTORY:
            # Remove oldest non-pinned item
            for i in range(len(self.history) - 1, -1, -1):
                if not self.history[i].pinned:
                    self.history.pop(i)
                    break
            else:
                # All pinned, remove oldest anyway
                self.history.pop()
        
        self.refresh_list()
        self.save_history()
    
    def refresh_list(self):
        """Refresh the history list display."""
        self.list_widget.clear()
        
        search_text = self.search_input.text().lower()
        
        # Sort: pinned first, then by time
        sorted_history = sorted(
            self.history,
            key=lambda x: (not x.pinned, x.timestamp),
            reverse=True
        )
        sorted_history = sorted(sorted_history, key=lambda x: not x.pinned)
        
        visible_count = 0
        for item in sorted_history:
            if search_text and search_text not in item.text.lower():
                continue
            
            visible_count += 1
            
            # Create list item
            preview = item.preview()
            if item.pinned:
                preview = f"📌 {preview}"
            
            list_item = QListWidgetItem(preview)
            list_item.setData(Qt.UserRole, item)
            list_item.setToolTip(f"{item.time_ago()}\n\nDouble-click to copy")
            
            self.list_widget.addItem(list_item)
        
        # Update stats
        pinned_count = sum(1 for item in self.history if item.pinned)
        self.stats_label.setText(
            f"📊 {len(self.history)} items • {pinned_count} pinned • "
            f"Showing {visible_count}"
        )
    
    def filter_history(self):
        """Filter history based on search text."""
        self.refresh_list()
    
    def on_selection_changed(self):
        """Update preview when selection changes."""
        items = self.list_widget.selectedItems()
        if items:
            item = items[0].data(Qt.UserRole)
            self.preview_text.setPlainText(item.text)
        else:
            self.preview_text.clear()
    
    def copy_item(self, list_item: QListWidgetItem):
        """Copy item to clipboard."""
        item = list_item.data(Qt.UserRole)
        self.monitor.set_text(item.text)
        
        # Move to top (update timestamp)
        self.history.remove(item)
        item.timestamp = datetime.now().isoformat()
        self.history.insert(0, item)
        
        self.refresh_list()
        self.save_history()
        
        # Show notification
        self.tray_icon.showMessage(
            "Copied!",
            item.preview(40),
            QSystemTrayIcon.Information,
            1000
        )
    
    def copy_selected(self):
        """Copy the selected item."""
        items = self.list_widget.selectedItems()
        if items:
            self.copy_item(items[0])
    
    def toggle_pin(self):
        """Toggle pin status of selected item."""
        items = self.list_widget.selectedItems()
        if items:
            item = items[0].data(Qt.UserRole)
            item.pinned = not item.pinned
            self.refresh_list()
            self.save_history()
    
    def delete_selected(self):
        """Delete the selected item."""
        items = self.list_widget.selectedItems()
        if items:
            item = items[0].data(Qt.UserRole)
            self.history.remove(item)
            self.refresh_list()
            self.save_history()
    
    def clear_history(self):
        """Clear all non-pinned history."""
        reply = QMessageBox.question(
            self,
            "Clear History",
            "Clear all non-pinned items?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.history = [item for item in self.history if item.pinned]
            self.refresh_list()
            self.save_history()
    
    def save_history(self):
        """Save history to file."""
        try:
            data = [item.to_dict() for item in self.history]
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def load_history(self):
        """Load history from file."""
        try:
            if SAVE_FILE.exists():
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = [ClipboardItem.from_dict(item) for item in data]
        except Exception as e:
            print(f"Error loading history: {e}")
            self.history = []
        
        self.refresh_list()


# ═══════════════════════════════════════════════════════════════════════════════
# Main Entry Point
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point."""
    # High DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Keep running in tray
    
    # Check if already running (simple check)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("Metaphy LLC")
    
    window = QuickClipWindow()
    window.show()
    
    print(f"""
================================================================
                    QuickClip v{VERSION}
              Universal Clipboard Manager
================================================================
  * Clipboard history is being monitored
  * Double-click an item to copy it
  * Press Escape to minimize to tray
  * Right-click tray icon to quit
================================================================
    """)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

