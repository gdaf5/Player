import sys
import os
import json
import glob
import random
import subprocess
import threading
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd()

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QLabel, QSlider,
    QFileDialog, QInputDialog, QMessageBox, QFrame, QSplitter,
    QComboBox, QMenu, QLineEdit, QTabWidget, QStackedWidget,
    QProgressBar,
)
from PyQt6.QtCore import (
    Qt, QUrl, QTimer, QSize, QSettings, pyqtSignal, QThread,
)
from PyQt6.QtGui import (
    QFont, QColor, QPixmap, QPainter, QMovie, QImage,
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE
from mutagen.id3 import ID3


THEMES = {
    "Midnight": {
        "bg_primary": "#0d0d1a",
        "bg_secondary": "#151528",
        "bg_tertiary": "#1e1e3a",
        "bg_hover": "#252550",
        "bg_active": "#2a2a60",
        "text_primary": "#e8e8f0",
        "text_secondary": "#8888aa",
        "text_muted": "#555570",
        "accent": "#6c5ce7",
        "accent_hover": "#7c6cf7",
        "border": "#2a2a45",
        "progress_bg": "#1e1e3a",
        "progress_fill": "#6c5ce7",
        "scrollbar": "#2a2a45",
        "scrollbar_hover": "#3a3a60",
        "gradient_start": "#6c5ce7",
        "gradient_end": "#a855f7",
        "success": "#00b894",
        "danger": "#e74c3c",
        "warning": "#f39c12",
    },
    "Ocean": {
        "bg_primary": "#0a192f",
        "bg_secondary": "#112240",
        "bg_tertiary": "#1d3461",
        "bg_hover": "#233567",
        "bg_active": "#2a4070",
        "text_primary": "#ccd6f6",
        "text_secondary": "#8892b0",
        "text_muted": "#495670",
        "accent": "#64ffda",
        "accent_hover": "#7afff0",
        "border": "#1d3461",
        "progress_bg": "#112240",
        "progress_fill": "#64ffda",
        "scrollbar": "#1d3461",
        "scrollbar_hover": "#2a4a80",
        "gradient_start": "#64ffda",
        "gradient_end": "#00b4d8",
        "success": "#00b894",
        "danger": "#e74c3c",
        "warning": "#f39c12",
    },
    "Sunset": {
        "bg_primary": "#1a0a1e",
        "bg_secondary": "#2d1533",
        "bg_tertiary": "#3d1f45",
        "bg_hover": "#4a2555",
        "bg_active": "#552d65",
        "text_primary": "#f8e8ff",
        "text_secondary": "#b888cc",
        "text_muted": "#705580",
        "accent": "#ff6b9d",
        "accent_hover": "#ff85b5",
        "border": "#3d1f45",
        "progress_bg": "#2d1533",
        "progress_fill": "#ff6b9d",
        "scrollbar": "#3d1f45",
        "scrollbar_hover": "#552d65",
        "gradient_start": "#ff6b9d",
        "gradient_end": "#ffa726",
        "success": "#00b894",
        "danger": "#e74c3c",
        "warning": "#f39c12",
    },
    "Forest": {
        "bg_primary": "#0a1a0f",
        "bg_secondary": "#142818",
        "bg_tertiary": "#1e3822",
        "bg_hover": "#254528",
        "bg_active": "#2d5530",
        "text_primary": "#e0f0e5",
        "text_secondary": "#88aa90",
        "text_muted": "#507055",
        "accent": "#4ade80",
        "accent_hover": "#5ee89a",
        "border": "#1e3822",
        "progress_bg": "#142818",
        "progress_fill": "#4ade80",
        "scrollbar": "#1e3822",
        "scrollbar_hover": "#2d5530",
        "gradient_start": "#4ade80",
        "gradient_end": "#22d3ee",
        "success": "#00b894",
        "danger": "#e74c3c",
        "warning": "#f39c12",
    },
    "Light": {
        "bg_primary": "#ffffff",
        "bg_secondary": "#f5f5f7",
        "bg_tertiary": "#e8e8ed",
        "bg_hover": "#e0e0e5",
        "bg_active": "#d5d5da",
        "text_primary": "#1a1a2e",
        "text_secondary": "#666680",
        "text_muted": "#9999aa",
        "accent": "#6c5ce7",
        "accent_hover": "#5a4bd6",
        "border": "#e0e0e5",
        "progress_bg": "#e8e8ed",
        "progress_fill": "#6c5ce7",
        "scrollbar": "#d0d0d5",
        "scrollbar_hover": "#b0b0b5",
        "gradient_start": "#6c5ce7",
        "gradient_end": "#a855f7",
        "success": "#00b894",
        "danger": "#e74c3c",
        "warning": "#f39c12",
    },
    "Cyberpunk": {
        "bg_primary": "#0a0a12",
        "bg_secondary": "#12121f",
        "bg_tertiary": "#1a1a2e",
        "bg_hover": "#222240",
        "bg_active": "#2a2a50",
        "text_primary": "#f0f0ff",
        "text_secondary": "#8888cc",
        "text_muted": "#555570",
        "accent": "#00ffff",
        "accent_hover": "#33ffff",
        "border": "#1a1a2e",
        "progress_bg": "#12121f",
        "progress_fill": "#00ffff",
        "scrollbar": "#1a1a2e",
        "scrollbar_hover": "#2a2a50",
        "gradient_start": "#00ffff",
        "gradient_end": "#ff00ff",
        "success": "#00ff88",
        "danger": "#ff0044",
        "warning": "#ffaa00",
    },
    "Rose Gold": {
        "bg_primary": "#1a1015",
        "bg_secondary": "#251820",
        "bg_tertiary": "#302030",
        "bg_hover": "#3a2840",
        "bg_active": "#453050",
        "text_primary": "#f5e6ef",
        "text_secondary": "#b899aa",
        "text_muted": "#705565",
        "accent": "#f4a7bb",
        "accent_hover": "#f8bdd0",
        "border": "#302030",
        "progress_bg": "#251820",
        "progress_fill": "#f4a7bb",
        "scrollbar": "#302030",
        "scrollbar_hover": "#453050",
        "gradient_start": "#f4a7bb",
        "gradient_end": "#d4a0c0",
        "success": "#00b894",
        "danger": "#e74c3c",
        "warning": "#f39c12",
    },
    "Nord": {
        "bg_primary": "#2e3440",
        "bg_secondary": "#3b4252",
        "bg_tertiary": "#434c5e",
        "bg_hover": "#4c566a",
        "bg_active": "#556075",
        "text_primary": "#eceff4",
        "text_secondary": "#d8dee9",
        "text_muted": "#7b88a1",
        "accent": "#88c0d0",
        "accent_hover": "#8fbcbb",
        "border": "#434c5e",
        "progress_bg": "#3b4252",
        "progress_fill": "#88c0d0",
        "scrollbar": "#434c5e",
        "scrollbar_hover": "#4c566a",
        "gradient_start": "#88c0d0",
        "gradient_end": "#81a1c1",
        "success": "#a3be8c",
        "danger": "#bf616a",
        "warning": "#ebcb8b",
    },
    "Cherry Blossom": {
        "bg_primary": "#1a0f14",
        "bg_secondary": "#241520",
        "bg_tertiary": "#301e2c",
        "bg_hover": "#3d2838",
        "bg_active": "#4a3045",
        "text_primary": "#f5e6f0",
        "text_secondary": "#c8a0b8",
        "text_muted": "#7a5568",
        "accent": "#ffb7c5",
        "accent_hover": "#ffc8d4",
        "border": "#301e2c",
        "progress_bg": "#241520",
        "progress_fill": "#ffb7c5",
        "scrollbar": "#301e2c",
        "scrollbar_hover": "#4a3045",
        "gradient_start": "#ffb7c5",
        "gradient_end": "#ff69b4",
        "success": "#98fb98",
        "danger": "#ff6b6b",
        "warning": "#ffd700",
    },
    "Deep Purple": {
        "bg_primary": "#0d0618",
        "bg_secondary": "#160d28",
        "bg_tertiary": "#1f1238",
        "bg_hover": "#281848",
        "bg_active": "#322060",
        "text_primary": "#e0d0f8",
        "text_secondary": "#9888b8",
        "text_muted": "#5a4870",
        "accent": "#b388ff",
        "accent_hover": "#c8a0ff",
        "border": "#1f1238",
        "progress_bg": "#160d28",
        "progress_fill": "#b388ff",
        "scrollbar": "#1f1238",
        "scrollbar_hover": "#322060",
        "gradient_start": "#b388ff",
        "gradient_end": "#e040fb",
        "success": "#69f0ae",
        "danger": "#ff5252",
        "warning": "#ffd740",
    },
    "Emerald": {
        "bg_primary": "#061410",
        "bg_secondary": "#0a2018",
        "bg_tertiary": "#0e2e22",
        "bg_hover": "#123a2c",
        "bg_active": "#184838",
        "text_primary": "#d4f0e8",
        "text_secondary": "#88c8b0",
        "text_muted": "#487860",
        "accent": "#34d399",
        "accent_hover": "#4adeb0",
        "border": "#0e2e22",
        "progress_bg": "#0a2018",
        "progress_fill": "#34d399",
        "scrollbar": "#0e2e22",
        "scrollbar_hover": "#184838",
        "gradient_start": "#34d399",
        "gradient_end": "#06b6d4",
        "success": "#34d399",
        "danger": "#ef4444",
        "warning": "#fbbf24",
    },
    "Amber": {
        "bg_primary": "#1a1408",
        "bg_secondary": "#28200c",
        "bg_tertiary": "#383014",
        "bg_hover": "#48401c",
        "bg_active": "#585024",
        "text_primary": "#f0e0c0",
        "text_secondary": "#b8a080",
        "text_muted": "#706040",
        "accent": "#fbbf24",
        "accent_hover": "#fcd34d",
        "border": "#383014",
        "progress_bg": "#28200c",
        "progress_fill": "#fbbf24",
        "scrollbar": "#383014",
        "scrollbar_hover": "#585024",
        "gradient_start": "#fbbf24",
        "gradient_end": "#f97316",
        "success": "#22c55e",
        "danger": "#ef4444",
        "warning": "#fbbf24",
    },
    "Crimson": {
        "bg_primary": "#180808",
        "bg_secondary": "#280e0e",
        "bg_tertiary": "#381414",
        "bg_hover": "#482020",
        "bg_active": "#582828",
        "text_primary": "#f0d0d0",
        "text_secondary": "#b88888",
        "text_muted": "#704848",
        "accent": "#ef4444",
        "accent_hover": "#f87171",
        "border": "#381414",
        "progress_bg": "#280e0e",
        "progress_fill": "#ef4444",
        "scrollbar": "#381414",
        "scrollbar_hover": "#582828",
        "gradient_start": "#ef4444",
        "gradient_end": "#f97316",
        "success": "#22c55e",
        "danger": "#ef4444",
        "warning": "#fbbf24",
    },
    "Aqua": {
        "bg_primary": "#061218",
        "bg_secondary": "#0a1e28",
        "bg_tertiary": "#0e2a38",
        "bg_hover": "#123848",
        "bg_active": "#184858",
        "text_primary": "#d0f0f8",
        "text_secondary": "#88c0d8",
        "text_muted": "#487080",
        "accent": "#22d3ee",
        "accent_hover": "#67e8f9",
        "border": "#0e2a38",
        "progress_bg": "#0a1e28",
        "progress_fill": "#22d3ee",
        "scrollbar": "#0e2a38",
        "scrollbar_hover": "#184858",
        "gradient_start": "#22d3ee",
        "gradient_end": "#06b6d4",
        "success": "#22c55e",
        "danger": "#ef4444",
        "warning": "#fbbf24",
    },
    "Spider": {
        "bg_primary": "#080808",
        "bg_secondary": "#101010",
        "bg_tertiary": "#1a1a1a",
        "bg_hover": "#222222",
        "bg_active": "#2a2a2a",
        "text_primary": "#e0e0e0",
        "text_secondary": "#888888",
        "text_muted": "#444444",
        "accent": "#cc0000",
        "accent_hover": "#ee0000",
        "border": "#1a1a1a",
        "progress_bg": "#101010",
        "progress_fill": "#cc0000",
        "scrollbar": "#1a1a1a",
        "scrollbar_hover": "#2a2a2a",
        "gradient_start": "#cc0000",
        "gradient_end": "#880000",
        "success": "#22c55e",
        "danger": "#cc0000",
        "warning": "#ff8800",
    },
}


def generate_stylesheet(t):
    return f"""
    QMainWindow {{ background-color: {t['bg_primary']}; }}
    QWidget {{
        background-color: transparent;
        color: {t['text_primary']};
        font-family: 'Segoe UI', 'SF Pro Display', -apple-system, sans-serif;
        font-size: 13px;
    }}
    QFrame#sidebar {{
        background-color: {t['bg_secondary']};
        border-right: 1px solid {t['border']};
    }}
    QFrame#main_content {{
        background-color: {t['bg_primary']};
    }}
    QFrame#player_bar {{
        background-color: {t['bg_secondary']};
        border-top: 1px solid {t['border']};
    }}
    QFrame#sidebar_header {{
        background-color: transparent;
        border-bottom: 1px solid {t['border']};
    }}
    QListWidget#track_list, QListWidget#playlist_list, QListWidget#search_results {{
        background-color: transparent;
        border: none;
        color: {t['text_primary']};
        font-size: 13px;
        outline: none;
    }}
    QListWidget#track_list::item, QListWidget#playlist_list::item, QListWidget#search_results::item {{
        padding: 10px 15px;
        border-radius: 8px;
        margin: 2px 8px;
        border: none;
    }}
    QListWidget#track_list::item:hover, QListWidget#playlist_list::item:hover, QListWidget#search_results::item:hover {{
        background-color: {t['bg_hover']};
    }}
    QListWidget#track_list::item:selected, QListWidget#playlist_list::item:selected, QListWidget#search_results::item:selected {{
        background-color: {t['bg_active']};
        color: {t['accent']};
    }}
    QListWidget#track_list QScrollBar:vertical, QListWidget#search_results QScrollBar:vertical {{
        width: 6px;
        background: transparent;
    }}
    QListWidget#track_list QScrollBar::handle:vertical, QListWidget#search_results QScrollBar::handle:vertical {{
        background: {t['scrollbar']};
        border-radius: 3px;
        min-height: 30px;
    }}
    QListWidget#track_list QScrollBar::handle:vertical:hover, QListWidget#search_results QScrollBar::handle:vertical:hover {{
        background: {t['scrollbar_hover']};
    }}
    QListWidget#track_list QScrollBar::add-line, QListWidget#track_list QScrollBar::sub-line,
    QListWidget#search_results QScrollBar::add-line, QListWidget#search_results QScrollBar::sub-line {{
        height: 0px;
    }}
    QSlider::groove:horizontal {{
        height: 4px;
        background: {t['progress_bg']};
        border-radius: 2px;
    }}
    QSlider::handle:horizontal {{
        width: 14px;
        height: 14px;
        margin: -5px 0;
        background: {t['accent']};
        border-radius: 7px;
    }}
    QSlider::handle:horizontal:hover {{
        background: {t['accent_hover']};
    }}
    QSlider::sub-page:horizontal {{
        background: {t['progress_fill']};
        border-radius: 2px;
    }}
    QSlider::add-page:horizontal {{
        background: {t['progress_bg']};
        border-radius: 2px;
    }}
    QPushButton {{
        background-color: transparent;
        color: {t['text_primary']};
        border: none;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 13px;
    }}
    QPushButton:hover {{
        background-color: {t['bg_hover']};
    }}
    QPushButton:pressed {{
        background-color: {t['bg_active']};
    }}
    QPushButton#play_btn {{
        background-color: {t['accent']};
        color: {t['bg_primary']};
        border-radius: 22px;
        min-width: 46px;
        min-height: 46px;
        max-width: 46px;
        max-height: 46px;
        font-size: 16px;
    }}
    QPushButton#play_btn:hover {{
        background-color: {t['accent_hover']};
    }}
    QPushButton#control_btn {{
        min-width: 40px;
        min-height: 40px;
        max-width: 40px;
        max-height: 40px;
        border-radius: 20px;
        font-size: 16px;
    }}
    QPushButton#small_btn {{
        min-width: 32px;
        min-height: 32px;
        max-width: 32px;
        max-height: 32px;
        border-radius: 16px;
        font-size: 14px;
        padding: 4px;
    }}
    QPushButton#accent_btn {{
        background-color: {t['accent']};
        color: {t['bg_primary']};
        border-radius: 8px;
        font-weight: bold;
    }}
    QPushButton#accent_btn:hover {{
        background-color: {t['accent_hover']};
    }}
    QPushButton#download_btn {{
        background-color: {t['success']};
        color: {t['bg_primary']};
        border-radius: 6px;
        font-size: 11px;
        padding: 4px 10px;
    }}
    QPushButton#download_btn:hover {{
        opacity: 0.85;
    }}
    QComboBox {{
        background-color: {t['bg_tertiary']};
        color: {t['text_primary']};
        border: 1px solid {t['border']};
        border-radius: 8px;
        padding: 6px 12px;
        min-width: 120px;
    }}
    QComboBox:hover {{
        border-color: {t['accent']};
    }}
    QComboBox::drop-down {{
        border: none;
        padding-right: 8px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {t['bg_secondary']};
        color: {t['text_primary']};
        border: 1px solid {t['border']};
        border-radius: 8px;
        selection-background-color: {t['accent']};
        selection-color: {t['bg_primary']};
        outline: none;
    }}
    QComboBox QAbstractItemView::item {{
        padding: 8px 12px;
        border-radius: 4px;
        margin: 2px;
    }}
    QLabel {{
        color: {t['text_primary']};
        background-color: transparent;
    }}
    QLabel#title_label {{
        color: {t['text_primary']};
        font-size: 14px;
        font-weight: bold;
    }}
    QLabel#artist_label {{
        color: {t['text_secondary']};
        font-size: 12px;
    }}
    QLabel#time_label {{
        color: {t['text_secondary']};
        font-size: 11px;
    }}
    QLabel#section_label {{
        color: {t['text_muted']};
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 10px 15px 5px;
    }}
    QLineEdit {{
        background-color: {t['bg_tertiary']};
        color: {t['text_primary']};
        border: 1px solid {t['border']};
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 13px;
    }}
    QLineEdit:focus {{
        border-color: {t['accent']};
    }}
    QMenu {{
        background-color: {t['bg_secondary']};
        border: 1px solid {t['border']};
        border-radius: 8px;
        padding: 5px;
    }}
    QMenu::item {{
        padding: 8px 25px 8px 15px;
        border-radius: 5px;
        margin: 2px;
    }}
    QMenu::item:selected {{
        background-color: {t['bg_hover']};
    }}
    QScrollBar:vertical {{
        width: 6px;
        background: transparent;
    }}
    QScrollBar::handle:vertical {{
        background: {t['scrollbar']};
        border-radius: 3px;
        min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {t['scrollbar_hover']};
    }}
    QScrollBar::add-line, QScrollBar::sub-line {{
        height: 0px;
    }}
    QToolTip {{
        background-color: {t['bg_tertiary']};
        color: {t['text_primary']};
        border: 1px solid {t['border']};
        border-radius: 5px;
        padding: 5px 10px;
    }}
    QSplitter::handle {{
        background-color: {t['border']};
    }}
    QDialog {{
        background-color: {t['bg_secondary']};
    }}
    QDialog QLabel {{
        color: {t['text_primary']};
    }}
    QTabWidget::pane {{
        border: none;
        background-color: transparent;
    }}
    QTabBar::tab {{
        background-color: {t['bg_tertiary']};
        color: {t['text_secondary']};
        padding: 8px 16px;
        border-radius: 8px 8px 0 0;
        margin-right: 2px;
        font-size: 12px;
    }}
    QTabBar::tab:selected {{
        background-color: {t['bg_active']};
        color: {t['accent']};
    }}
    QTabBar::tab:hover {{
        background-color: {t['bg_hover']};
    }}
    QProgressBar {{
        border: none;
        background-color: {t['progress_bg']};
        border-radius: 3px;
        height: 6px;
        text-align: center;
    }}
    QProgressBar::chunk {{
        background-color: {t['progress_fill']};
        border-radius: 3px;
    }}
    """


def get_track_info(filepath):
    info = {
        "path": filepath,
        "title": Path(filepath).stem,
        "artist": "Unknown Artist",
        "album": "Unknown Album",
        "duration": 0,
        "cover_path": None,
    }
    ext = Path(filepath).suffix.lower()
    try:
        if ext == ".mp3":
            try:
                audio = EasyID3(filepath)
                info["title"] = audio.get("title", [Path(filepath).stem])[0]
                info["artist"] = audio.get("artist", ["Unknown Artist"])[0]
                info["album"] = audio.get("album", ["Unknown Album"])[0]
            except:
                pass
            try:
                audio = MP3(filepath)
                info["duration"] = int(audio.info.length * 1000)
            except:
                pass
            try:
                tags = ID3(filepath)
                for tag in tags.values():
                    if tag.frameid == "APIC":
                        cover_data = tag.data
                        cover_path = filepath + ".cover.jpg"
                        with open(cover_path, "wb") as f:
                            f.write(cover_data)
                        info["cover_path"] = cover_path
                        break
            except:
                pass
        elif ext in (".m4a", ".mp4"):
            audio = MP4(filepath)
            tags = audio.tags
            if tags:
                info["title"] = tags.get("\xa9nam", [Path(filepath).stem])[0]
                info["artist"] = tags.get("\xa9ART", ["Unknown Artist"])[0]
                info["album"] = tags.get("\xa9alb", ["Unknown Album"])[0]
                if "covr" in tags:
                    cover_data = tags["covr"][0]
                    cover_path = filepath + ".cover.jpg"
                    with open(cover_path, "wb") as f:
                        f.write(cover_data)
                    info["cover_path"] = cover_path
            info["duration"] = int(audio.info.length * 1000)
        elif ext == ".flac":
            audio = FLAC(filepath)
            info["title"] = audio.get("title", [Path(filepath).stem])[0]
            info["artist"] = audio.get("artist", ["Unknown Artist"])[0]
            info["album"] = audio.get("album", ["Unknown Album"])[0]
            info["duration"] = int(audio.info.length * 1000)
            if audio.pictures:
                cover_data = audio.pictures[0].data
                cover_path = filepath + ".cover.jpg"
                with open(cover_path, "wb") as f:
                    f.write(cover_data)
                info["cover_path"] = cover_path
        elif ext == ".ogg":
            audio = OggVorbis(filepath)
            info["title"] = audio.get("title", [Path(filepath).stem])[0]
            info["artist"] = audio.get("artist", ["Unknown Artist"])[0]
            info["album"] = audio.get("album", ["Unknown Album"])[0]
            info["duration"] = int(audio.info.length * 1000)
        elif ext == ".wav":
            try:
                audio = WAVE(filepath)
                info["duration"] = int(audio.info.length * 1000)
            except:
                pass
    except Exception:
        pass
    return info


def get_cover_pixmap(track, size=200):
    cover_path = track.get("cover_path")
    if cover_path and os.path.exists(cover_path):
        pm = QPixmap(cover_path)
        if not pm.isNull():
            return pm.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    return None


class TrackListItem(QListWidgetItem):
    def __init__(self, track):
        super().__init__()
        self.track = track
        self.update_display()

    def update_display(self):
        self.setText(f"{self.track['artist']} - {self.track['title']}")
        self.setToolTip(f"{self.track['title']}\n{self.track['artist']}\n{self.track['album']}")


class SearchListItem(QListWidgetItem):
    def __init__(self, result):
        super().__init__()
        self.result = result
        self.update_display()

    def update_display(self):
        title = self.result.get("title", "Unknown")
        uploader = self.result.get("uploader", "Unknown")
        duration = self.result.get("duration_string", "")
        self.setText(f"{uploader} - {title}")
        if duration:
            self.setText(f"{uploader} - {title}  [{duration}]")
        self.setToolTip(f"{title}\n{uploader}")


class PlaylistListItem(QListWidgetItem):
    def __init__(self, name, track_count=0):
        super().__init__()
        self.playlist_name = name
        self.track_count = track_count
        self.update_display()

    def update_display(self):
        self.setText(f"\u266a {self.playlist_name}")
        self.setToolTip(f"{self.playlist_name} ({self.track_count} tracks)")


def format_time(ms):
    if ms <= 0:
        return "0:00"
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"


# ==================== SEARCH THREAD ====================

class SearchWorker(QThread):
    results_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def __init__(self, query, platform="youtube"):
        super().__init__()
        self.query = query
        self.platform = platform

    def run(self):
        try:
            if self.platform == "yandex":
                self._search_yandex()
            else:
                self._search_ytdlp()
        except Exception as e:
            self.error_occurred.emit(str(e))

    def _search_ytdlp(self):
        import yt_dlp
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "socket_timeout": 10,
        }
        results = []
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_query = f"ytsearch10:{self.query}"
            info = ydl.extract_info(search_query, download=False)
            if info and info.get("entries"):
                for entry in info["entries"]:
                    url = entry.get("url", "")
                    if not url and entry.get("id"):
                        url = f"https://www.youtube.com/watch?v={entry.get('id', '')}"

                    results.append({
                        "title": entry.get("title", "Unknown"),
                        "uploader": entry.get("uploader", entry.get("channel", "Unknown")),
                        "url": url,
                        "id": entry.get("id", ""),
                        "duration": entry.get("duration", 0),
                        "duration_string": entry.get("duration_string", ""),
                        "thumbnail": entry.get("thumbnail", ""),
                        "platform": self.platform,
                    })
        self.results_ready.emit(results)

    def _search_yandex(self):
        import yt_dlp
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "socket_timeout": 10,
        }
        results = []
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_query = f"ymsearch10:{self.query}"
            info = ydl.extract_info(search_query, download=False)
            if info and info.get("entries"):
                for entry in info["entries"]:
                    results.append({
                        "title": entry.get("title", "Unknown"),
                        "uploader": entry.get("artist", entry.get("uploader", "Unknown")),
                        "url": entry.get("url", entry.get("webpage_url", "")),
                        "id": entry.get("id", ""),
                        "duration": entry.get("duration", 0),
                        "duration_string": entry.get("duration_string", ""),
                        "thumbnail": entry.get("thumbnail", ""),
                        "platform": "yandex",
                    })
        self.results_ready.emit(results)


class StreamWorker(QThread):
    stream_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, url, result=None):
        super().__init__()
        self.url = url
        self.result = result or {}

    def run(self):
        try:
            if self.result.get("platform") == "vk" and self.result.get("direct_url"):
                self.stream_ready.emit(self.result["direct_url"])
            else:
                import yt_dlp
                ydl_opts = {
                    "quiet": True,
                    "no_warnings": True,
                    "format": "bestaudio/best",
                    "socket_timeout": 10,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(self.url, download=False)
                    stream_url = info.get("url", "")
                    if stream_url:
                        self.stream_ready.emit(stream_url)
                    else:
                        self.error_occurred.emit("No stream URL found")
        except Exception as e:
            self.error_occurred.emit(str(e))


class DownloadWorker(QThread):
    download_complete = pyqtSignal(str)
    download_progress = pyqtSignal(int)
    error_occurred = pyqtSignal(str)

    def __init__(self, url, save_dir, result=None):
        super().__init__()
        self.url = url
        self.save_dir = save_dir
        self.result = result or {}

    def run(self):
        try:
            os.makedirs(self.save_dir, exist_ok=True)

            if self.result.get("platform") == "vk" and self.result.get("direct_url"):
                self._download_vk()
            else:
                self._download_ytdlp()
        except Exception as e:
            self.error_occurred.emit(str(e))

    def _download_vk(self):
        import urllib.request
        title = self.result.get("title", "track")
        safe_title = "".join(c for c in title if c.isalnum() or c in " -_").strip()
        out_path = os.path.join(self.save_dir, f"{safe_title}.mp3")
        req = urllib.request.Request(self.result["direct_url"], headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            total = resp.getheader("Content-Length")
            total = int(total) if total else 0
            downloaded = 0
            with open(out_path, "wb") as f:
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0:
                        self.download_progress.emit(int(downloaded / total * 100))
        self.download_complete.emit(title)

    def _download_ytdlp(self):
        import yt_dlp
        ydl_opts = {
            "outtmpl": os.path.join(self.save_dir, "%(title)s.%(ext)s"),
            "format": "bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio",
            "quiet": True,
            "no_warnings": True,
            "socket_timeout": 10,
            "progress_hooks": [self._progress_hook],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=True)
            title = info.get("title", "downloaded")
            self.download_complete.emit(title)

    def _progress_hook(self, d):
        if d["status"] == "downloading":
            pct = d.get("_percent_str", "0%")
            try:
                val = float(pct.strip("%"))
                self.download_progress.emit(int(val))
            except:
                pass


# ==================== GIF PANEL ====================

class MarqueeLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._offset = 0
        self._full_text = text
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._paused = False
        self._scrolling = False

    def setText(self, text):
        self._full_text = text
        self._offset = 0
        self._scrolling = False
        self._timer.stop()
        super().setText(text)

    def _tick(self):
        if self._paused:
            return
        self._offset += 1
        if self._offset > len(self._full_text):
            self._offset = 0
            self._scrolling = False
            self._timer.stop()
            super().setText(self._full_text)
            return
        display = self._full_text[self._offset:] + "   " + self._full_text[:self._offset]
        super().setText(display)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        fm = self.fontMetrics()
        text_w = fm.horizontalAdvance(self._full_text)
        if text_w > self.width() and not self._scrolling:
            self._scrolling = True
            self._offset = 0
            self._timer.start(150)


class GifPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(300)
        self.setMaximumWidth(350)

        self.gifs_dir = os.path.join(SCRIPT_DIR, "gifs")
        os.makedirs(self.gifs_dir, exist_ok=True)

        self.gif_paths = []
        self.current_movie = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gif_label.setMinimumSize(280, 300)
        self.gif_label.setText("Drop .gif files in the\ngifs/ folder")
        self.gif_label.setStyleSheet("""
            QLabel {
                color: #555570;
                font-size: 14px;
                border: 2px dashed #2a2a45;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        layout.addWidget(self.gif_label)

        self.gif_name_label = QLabel("")
        self.gif_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gif_name_label.setStyleSheet("color: #8888aa; font-size: 11px; padding: 5px;")
        layout.addWidget(self.gif_name_label)

        self.scan_gifs()

    def scan_gifs(self):
        self.gif_paths = []
        if os.path.isdir(self.gifs_dir):
            for f in os.listdir(self.gifs_dir):
                if f.lower().endswith(".gif"):
                    self.gif_paths.append(os.path.join(self.gifs_dir, f))

    def play_random_gif(self):
        if self.current_movie:
            self.current_movie.stop()
            self.current_movie.deleteLater()
            self.current_movie = None

        if not self.gif_paths:
            self.scan_gifs()

        if not self.gif_paths:
            self.gif_label.setText("Drop .gif files in the\ngifs/ folder")
            self.gif_label.setStyleSheet("""
                QLabel {
                    color: #555570;
                    font-size: 14px;
                    border: 2px dashed #2a2a45;
                    border-radius: 12px;
                    padding: 20px;
                }
            """)
            self.gif_label.setMinimumSize(280, 300)
            self.gif_name_label.setText("")
            return

        gif_path = random.choice(self.gif_paths)
        self.current_movie = QMovie(gif_path)
        self.current_movie.setCacheMode(QMovie.CacheMode.CacheAll)

        def on_frame_changed():
            frame = self.current_movie.currentPixmap()
            if not frame.isNull():
                scaled = frame.scaled(
                    self.gif_label.width() - 10,
                    self.gif_label.height() - 10,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.gif_label.setPixmap(scaled)

        self.current_movie.frameChanged.connect(on_frame_changed)

        if self.current_movie.isValid():
            self.current_movie.start()
            self.gif_label.setStyleSheet("border-radius: 12px; background-color: transparent;")
            self.gif_label.setMinimumSize(280, 300)
            self.gif_name_label.setText(Path(gif_path).stem)
        else:
            self.gif_label.setText("Failed to load GIF")
            self.current_movie = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.current_movie and self.current_movie.state() == QMovie.MovieState.Running:
            frame = self.current_movie.currentPixmap()
            if not frame.isNull():
                scaled = frame.scaled(
                    self.gif_label.width() - 10,
                    self.gif_label.height() - 10,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.gif_label.setPixmap(scaled)


# ==================== MAIN WINDOW ====================

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SonicWave Player")
        self.setMinimumSize(1200, 700)
        self.resize(1300, 750)

        self.current_theme_name = "Midnight"
        self.theme = THEMES[self.current_theme_name]

        self.tracks = []
        self.playlists = {}
        self.current_playlist = None
        self.current_track_index = -1
        self.shuffle = False
        self.repeat_mode = 0
        self.slider_pressed = False

        self.is_streaming = False
        self.stream_worker = None
        self.search_worker = None
        self.download_worker = None
        self.search_results = []

        self.download_dir = os.path.join(SCRIPT_DIR, "downloads")
        os.makedirs(self.download_dir, exist_ok=True)

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.7)

        self.setup_ui()
        self.connect_signals()
        self.apply_theme(self.current_theme_name)
        self.load_saved_data()

        self.statusBar().showMessage("Ready")

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(260)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        header = QFrame()
        header.setObjectName("sidebar_header")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(15, 20, 15, 15)

        self.app_title = QLabel("SonicWave")
        self.app_title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {self.theme['accent']}; padding: 5px 0;")
        header_layout.addWidget(self.app_title)

        add_btn_layout = QHBoxLayout()
        add_btn_layout.setSpacing(8)

        self.add_folder_btn = QPushButton("Add Folder")
        self.add_folder_btn.setObjectName("accent_btn")
        self.add_folder_btn.clicked.connect(self.add_folder)
        add_btn_layout.addWidget(self.add_folder_btn)

        self.add_files_btn = QPushButton("Add Files")
        self.add_files_btn.setObjectName("accent_btn")
        self.add_files_btn.clicked.connect(self.add_files)
        add_btn_layout.addWidget(self.add_files_btn)

        header_layout.addLayout(add_btn_layout)
        sidebar_layout.addWidget(header)

        # Search section
        search_header = QLabel("SEARCH")
        search_header.setObjectName("section_label")
        sidebar_layout.addWidget(search_header)

        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(15, 5, 15, 5)
        search_layout.setSpacing(5)

        self.platform_combo = QComboBox()
        self.platform_combo.addItem("YouTube")
        self.platform_combo.addItem("URL")
        self.platform_combo.setFixedWidth(100)
        self.platform_combo.currentTextChanged.connect(self.on_platform_changed)
        search_layout.addWidget(self.platform_combo)

        self.online_search_input = QLineEdit()
        self.online_search_input.setPlaceholderText("Search YouTube...")
        self.online_search_input.returnPressed.connect(self.search_online)
        search_layout.addWidget(self.online_search_input)

        self.search_online_btn = QPushButton("\U0001f50d")
        self.search_online_btn.setObjectName("small_btn")
        self.search_online_btn.clicked.connect(self.search_online)
        search_layout.addWidget(self.search_online_btn)

        sidebar_layout.addLayout(search_layout)

        self.search_progress = QProgressBar()
        self.search_progress.setVisible(False)
        self.search_progress.setFixedHeight(4)
        self.search_progress.setTextVisible(False)
        self.search_progress.setStyleSheet(f"""
            QProgressBar {{ background-color: {self.theme['bg_tertiary']}; border: none; border-radius: 2px; }}
            QProgressBar::chunk {{ background-color: {self.theme['accent']}; border-radius: 2px; }}
        """)
        sidebar_layout.addWidget(self.search_progress)

        self.search_results_list = QListWidget()
        self.search_results_list.setObjectName("search_results")
        self.search_results_list.itemDoubleClicked.connect(self.play_search_result)
        self.search_results_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.search_results_list.customContextMenuRequested.connect(self.show_search_context)
        sidebar_layout.addWidget(self.search_results_list)

        # Playlists section
        pl_label = QLabel("PLAYLISTS")
        pl_label.setObjectName("section_label")
        sidebar_layout.addWidget(pl_label)

        playlist_btn_layout = QHBoxLayout()
        playlist_btn_layout.setContentsMargins(15, 5, 15, 5)

        self.new_playlist_btn = QPushButton("+ New Playlist")
        self.new_playlist_btn.setObjectName("accent_btn")
        self.new_playlist_btn.clicked.connect(self.create_playlist)
        playlist_btn_layout.addWidget(self.new_playlist_btn)
        sidebar_layout.addLayout(playlist_btn_layout)

        self.playlist_list = QListWidget()
        self.playlist_list.setObjectName("playlist_list")
        self.playlist_list.itemClicked.connect(self.on_playlist_selected)
        self.playlist_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.playlist_list.customContextMenuRequested.connect(self.show_playlist_context)
        sidebar_layout.addWidget(self.playlist_list)

        all_label = QLabel("ALL TRACKS")
        all_label.setObjectName("section_label")
        sidebar_layout.addWidget(all_label)

        self.track_count_label = QLabel("0 tracks")
        self.track_count_label.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: 11px; padding: 0 15px 10px;")
        sidebar_layout.addWidget(self.track_count_label)

        sidebar_layout.addStretch()

        theme_layout = QHBoxLayout()
        theme_layout.setContentsMargins(15, 10, 15, 15)
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet(f"color: {self.theme['text_secondary']}; font-size: 12px;")
        theme_layout.addWidget(theme_label)

        self.theme_combo = QComboBox()
        for name in THEMES.keys():
            self.theme_combo.addItem(name)
        self.theme_combo.setCurrentText(self.current_theme_name)
        self.theme_combo.currentTextChanged.connect(self.apply_theme)
        theme_layout.addWidget(self.theme_combo)
        sidebar_layout.addLayout(theme_layout)

        splitter.addWidget(self.sidebar)

        # Main content
        self.main_content = QFrame()
        self.main_content.setObjectName("main_content")
        main_content_layout = QVBoxLayout(self.main_content)
        main_content_layout.setContentsMargins(0, 0, 0, 0)
        main_content_layout.setSpacing(0)

        top_bar = QFrame()
        top_bar.setStyleSheet(f"background-color: {self.theme['bg_secondary']}; border-bottom: 1px solid {self.theme['border']};")
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(20, 10, 20, 10)

        self.current_view_title = QLabel("All Tracks")
        self.current_view_title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {self.theme['text_primary']};")
        top_bar_layout.addWidget(self.current_view_title)
        top_bar_layout.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search local tracks...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self.filter_tracks)
        top_bar_layout.addWidget(self.search_input)

        main_content_layout.addWidget(top_bar)

        self.track_list = QListWidget()
        self.track_list.setObjectName("track_list")
        self.track_list.itemDoubleClicked.connect(self.play_track_from_list)
        self.track_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.track_list.customContextMenuRequested.connect(self.show_track_context)
        main_content_layout.addWidget(self.track_list)

        splitter.addWidget(self.main_content)

        # GIF panel
        self.gif_panel = GifPanel(self)
        splitter.addWidget(self.gif_panel)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)

        main_layout.addWidget(splitter)

        # Player bar
        self.player_bar = QFrame()
        self.player_bar.setObjectName("player_bar")
        self.player_bar.setFixedHeight(100)

        player_bar_main = QVBoxLayout(self.player_bar)
        player_bar_main.setContentsMargins(0, 0, 0, 0)
        player_bar_main.setSpacing(0)

        player_bar_row = QHBoxLayout()
        player_bar_row.setContentsMargins(20, 8, 20, 8)
        player_bar_row.setSpacing(0)

        # === LEFT: cover + info (fixed 350px, never grows) ===
        left_widget = QWidget()
        left_widget.setFixedWidth(350)
        left_layout = QHBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.cover_label = QLabel()
        self.cover_label.setFixedSize(70, 70)
        self.cover_label.setMinimumSize(70, 70)
        self.cover_label.setMaximumSize(70, 70)
        self.cover_label.setStyleSheet(f"""
            QLabel {{
                background-color: {self.theme['bg_tertiary']};
                border-radius: 8px;
            }}
        """)
        self.cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.cover_label)

        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(3)

        self.now_title = QLabel("No track selected")
        self.now_title.setObjectName("title_label")
        self.now_title.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {self.theme['text_primary']};")
        self.now_title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        info_layout.addWidget(self.now_title)

        self.now_artist = QLabel("Select a track to play")
        self.now_artist.setObjectName("artist_label")
        self.now_artist.setStyleSheet(f"font-size: 12px; color: {self.theme['text_secondary']};")
        self.now_artist.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        info_layout.addWidget(self.now_artist)

        left_layout.addWidget(info_widget)
        player_bar_row.addWidget(left_widget)

        # === CENTER: controls + progress (takes all remaining space) ===
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(10, 0, 10, 0)
        center_layout.setSpacing(4)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.shuffle_btn = QPushButton("\U0001f500")
        self.shuffle_btn.setObjectName("control_btn")
        self.shuffle_btn.clicked.connect(self.toggle_shuffle)
        btn_row.addWidget(self.shuffle_btn)

        self.prev_btn = QPushButton("\u23ee")
        self.prev_btn.setObjectName("control_btn")
        self.prev_btn.clicked.connect(self.play_prev)
        btn_row.addWidget(self.prev_btn)

        self.play_btn = QPushButton("\u25b6")
        self.play_btn.setObjectName("play_btn")
        self.play_btn.clicked.connect(self.toggle_play)
        btn_row.addWidget(self.play_btn)

        self.next_btn = QPushButton("\u23ed")
        self.next_btn.setObjectName("control_btn")
        self.next_btn.clicked.connect(self.play_next)
        btn_row.addWidget(self.next_btn)

        self.repeat_btn = QPushButton("\U0001f501")
        self.repeat_btn.setObjectName("control_btn")
        self.repeat_btn.clicked.connect(self.toggle_repeat)
        btn_row.addWidget(self.repeat_btn)

        center_layout.addLayout(btn_row)

        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(10)
        progress_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.time_current = QLabel("0:00")
        self.time_current.setObjectName("time_label")
        self.time_current.setStyleSheet(f"color: {self.theme['text_secondary']}; font-size: 11px; min-width: 40px;")
        progress_layout.addWidget(self.time_current)

        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setRange(0, 1000)
        self.progress_slider.setValue(0)
        self.progress_slider.sliderPressed.connect(self.on_slider_pressed)
        self.progress_slider.sliderReleased.connect(self.on_slider_released)
        progress_layout.addWidget(self.progress_slider)

        self.time_total = QLabel("0:00")
        self.time_total.setObjectName("time_label")
        self.time_total.setStyleSheet(f"color: {self.theme['text_secondary']}; font-size: 11px; min-width: 40px;")
        progress_layout.addWidget(self.time_total)

        center_layout.addLayout(progress_layout)
        player_bar_row.addWidget(center_widget, 1)

        # === RIGHT: volume (fixed 150px, never grows) ===
        right_widget = QWidget()
        right_widget.setFixedWidth(150)
        right_layout = QHBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.volume_btn = QPushButton("\U0001f50a")
        self.volume_btn.setObjectName("small_btn")
        self.volume_btn.clicked.connect(self.toggle_mute)
        right_layout.addWidget(self.volume_btn)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setFixedWidth(80)
        self.volume_slider.valueChanged.connect(self.change_volume)
        right_layout.addWidget(self.volume_slider)

        player_bar_row.addWidget(right_widget)

        player_bar_main.addLayout(player_bar_row)
        main_layout.addWidget(self.player_bar)

    def connect_signals(self):
        self.player.positionChanged.connect(self.on_position_changed)
        self.player.durationChanged.connect(self.on_duration_changed)
        self.player.playbackStateChanged.connect(self.on_state_changed)
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)

    def apply_theme(self, theme_name):
        self.current_theme_name = theme_name
        self.theme = THEMES[theme_name]
        self.setStyleSheet(generate_stylesheet(self.theme))

        self.app_title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {self.theme['accent']}; padding: 5px 0;")
        self.now_title.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {self.theme['text_primary']};")
        self.now_artist.setStyleSheet(f"font-size: 12px; color: {self.theme['text_secondary']};")
        self.time_current.setStyleSheet(f"color: {self.theme['text_secondary']}; font-size: 11px; min-width: 40px;")
        self.time_total.setStyleSheet(f"color: {self.theme['text_secondary']}; font-size: 11px; min-width: 40px; text-align: right;")
        self.track_count_label.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: 11px; padding: 0 15px 10px;")
        self.current_view_title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {self.theme['text_primary']};")

        t = self.theme
        if not self.cover_label.pixmap() or self.cover_label.pixmap().isNull():
            self.cover_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {t['bg_tertiary']};
                    border-radius: 8px;
                }}
            """)

    # ==================== ONLINE SEARCH ====================

    def on_platform_changed(self):
        if self.platform_combo.currentText() == "URL":
            self.online_search_input.setPlaceholderText("Paste URL (YouTube, Yandex, VK...)")
        else:
            self.online_search_input.setPlaceholderText("Search YouTube...")

    def search_online(self):
        query = self.online_search_input.text().strip()
        if not query:
            return

        if self.platform_combo.currentText() == "URL":
            self.play_url(query)
            return

        self.search_progress.setVisible(True)
        self.search_progress.setValue(0)
        self.search_results_list.clear()
        self.statusBar().showMessage(f"Searching: {query}...")

        if self.search_worker and self.search_worker.isRunning():
            self.search_worker.terminate()

        self.search_worker = SearchWorker(query, "youtube")
        self.search_worker.results_ready.connect(self.on_search_results)
        self.search_worker.error_occurred.connect(self.on_search_error)
        self.search_worker.start()

    def play_url(self, url):
        self.statusBar().showMessage(f"Loading: {url}...")

        if self.stream_worker and self.stream_worker.isRunning():
            self.stream_worker.terminate()

        self.stream_worker = StreamWorker(url, {"platform": "yt"})
        self.stream_worker.stream_ready.connect(self.on_stream_ready)
        self.stream_worker.error_occurred.connect(self.on_stream_error)
        self.stream_worker.start()

    def on_search_results(self, results):
        self.search_results = results
        self.search_results_list.clear()
        for r in results:
            item = SearchListItem(r)
            self.search_results_list.addItem(item)
        self.search_progress.setVisible(False)
        self.statusBar().showMessage(f"Found {len(results)} results")

    def on_search_error(self, error):
        self.search_progress.setVisible(False)
        self.statusBar().showMessage(f"Search error: {error}")

    def play_search_result(self, item):
        result = item.result
        self.statusBar().showMessage(f"Loading stream: {result['title']}...")

        if self.stream_worker and self.stream_worker.isRunning():
            self.stream_worker.terminate()

        self.stream_worker = StreamWorker(result["url"], result)
        self.stream_worker.stream_ready.connect(self.on_stream_ready)
        self.stream_worker.error_occurred.connect(self.on_stream_error)
        self.stream_worker.start()

    def on_stream_ready(self, stream_url):
        self.is_streaming = True
        self.player.setSource(QUrl(stream_url))
        self.player.play()
        self.current_track_index = -1

        self.now_title.setText(self.search_results[0]["title"] if self.search_results else "Streaming")
        self.now_artist.setText("Online Stream")
        self.gif_panel.play_random_gif()
        self.statusBar().showMessage("Streaming...")

    def on_stream_error(self, error):
        self.is_streaming = False
        self.statusBar().showMessage(f"Stream error: {error}")

    def show_search_context(self, pos):
        item = self.search_results_list.itemAt(pos)
        if not item:
            return

        menu = QMenu(self)
        play = menu.addAction("Play")
        play.triggered.connect(lambda: self.play_search_result(item))

        download = menu.addAction("Download")
        download.triggered.connect(lambda: self.download_search_result(item))

        menu.exec(self.search_results_list.mapToGlobal(pos))

    def download_search_result(self, item):
        result = item.result
        self.statusBar().showMessage(f"Downloading: {result['title']}...")
        self.search_progress.setVisible(True)
        self.search_progress.setValue(0)

        if self.download_worker and self.download_worker.isRunning():
            self.download_worker.terminate()

        self.download_worker = DownloadWorker(result["url"], self.download_dir, result)
        self.download_worker.download_complete.connect(self.on_download_complete)
        self.download_worker.download_progress.connect(self.search_progress.setValue)
        self.download_worker.error_occurred.connect(self.on_download_error)
        self.download_worker.start()

    def on_download_complete(self, title):
        self.search_progress.setVisible(False)
        self.statusBar().showMessage(f"Downloaded: {title}")

        # Scan downloads folder
        for ext in (".mp3", ".m4a", ".flac", ".ogg", ".wav"):
            for filepath in glob.glob(os.path.join(self.download_dir, f"*{ext}")):
                info = get_track_info(filepath)
                if info["path"] not in [t["path"] for t in self.tracks]:
                    self.tracks.append(info)

        self.refresh_track_list()
        self.save_data()

    def on_download_error(self, error):
        self.search_progress.setVisible(False)
        self.statusBar().showMessage(f"Download error: {error}")

    # ==================== LOCAL TRACKS ====================

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Music Folder")
        if folder:
            self.scan_folder(folder)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Music Files", "",
            "Music Files (*.mp3 *.m4a *.mp4 *.flac *.ogg *.wav);;All Files (*.*)"
        )
        if files:
            for f in files:
                info = get_track_info(f)
                if info["path"] not in [t["path"] for t in self.tracks]:
                    self.tracks.append(info)
            self.refresh_track_list()
            self.save_data()

    def scan_folder(self, folder):
        extensions = {".mp3", ".m4a", ".mp4", ".flac", ".ogg", ".wav"}
        files_found = 0
        for ext in extensions:
            for filepath in glob.glob(os.path.join(folder, f"**/*{ext}"), recursive=True):
                if filepath not in [t["path"] for t in self.tracks]:
                    info = get_track_info(filepath)
                    self.tracks.append(info)
                    files_found += 1
        self.refresh_track_list()
        self.save_data()
        if files_found > 0:
            self.show_status(f"Added {files_found} tracks")

    def refresh_track_list(self):
        self.track_list.clear()
        filtered = self.get_filtered_tracks()
        for track in filtered:
            item = TrackListItem(track)
            self.track_list.addItem(item)
        self.track_count_label.setText(f"{len(self.tracks)} tracks")

    def get_filtered_tracks(self):
        search = self.search_input.text().lower()
        if not search:
            return self.tracks
        return [t for t in self.tracks if
                search in t["title"].lower() or
                search in t["artist"].lower() or
                search in t["album"].lower()]

    def filter_tracks(self):
        self.refresh_track_list()

    def play_track_from_list(self, item):
        self.play_track(item.track)

    def play_track(self, track):
        if not os.path.exists(track["path"]):
            self.show_status(f"File not found: {track['title']}")
            return

        if not track.get("cover_path"):
            info = get_track_info(track["path"])
            track["cover_path"] = info.get("cover_path")

        self.is_streaming = False
        self.player.setSource(QUrl.fromLocalFile(track["path"]))
        self.player.play()
        self.current_track_index = self.get_track_index(track["path"])
        self.update_now_playing(track)
        self.gif_panel.play_random_gif()

    def get_track_index(self, path):
        for i, t in enumerate(self.tracks):
            if t["path"] == path:
                return i
        return -1

    def update_now_playing(self, track):
        self.now_title.setText(track["title"])
        self.now_artist.setText(track["artist"])
        pm = get_cover_pixmap(track, 70)
        if pm:
            self.cover_label.setPixmap(pm)
            self.cover_label.setStyleSheet("border-radius: 8px; background-color: transparent;")
        else:
            self.cover_label.setPixmap(QPixmap())
            t = self.theme
            self.cover_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {t['bg_tertiary']};
                    border-radius: 8px;
                }}
            """)

    def toggle_play(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            if self.player.playbackState() == QMediaPlayer.PlaybackState.StoppedState:
                if self.tracks:
                    self.play_track(self.tracks[0])
            else:
                self.player.play()

    def play_next(self):
        if self.is_streaming:
            self.is_streaming = False
            if self.tracks:
                self.play_track(self.tracks[0])
            return

        if not self.tracks:
            return

        if self.repeat_mode == 2:
            self.player.setPosition(0)
            self.player.play()
            return

        if self.shuffle:
            next_idx = random.randint(0, len(self.tracks) - 1)
        else:
            next_idx = self.current_track_index + 1
            if next_idx >= len(self.tracks):
                if self.repeat_mode == 1:
                    next_idx = 0
                else:
                    return

        self.play_track(self.tracks[next_idx])

    def play_prev(self):
        if not self.tracks:
            return

        if self.player.position() > 3000:
            self.player.setPosition(0)
            return

        prev_idx = self.current_track_index - 1
        if prev_idx < 0:
            if self.repeat_mode >= 1:
                prev_idx = len(self.tracks) - 1
            else:
                return

        self.play_track(self.tracks[prev_idx])

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
        if self.shuffle:
            self.shuffle_btn.setStyleSheet(
                f"background-color: {self.theme['accent']}; color: {self.theme['bg_primary']}; border-radius: 20px;"
            )
        else:
            self.shuffle_btn.setStyleSheet("")

    def toggle_repeat(self):
        self.repeat_mode = (self.repeat_mode + 1) % 3
        if self.repeat_mode == 0:
            self.repeat_btn.setText("\U0001f501")
            self.repeat_btn.setStyleSheet("")
        elif self.repeat_mode == 1:
            self.repeat_btn.setText("\U0001f501")
            self.repeat_btn.setStyleSheet(
                f"background-color: {self.theme['accent']}; color: {self.theme['bg_primary']}; border-radius: 20px;"
            )
        else:
            self.repeat_btn.setText("\U0001f502")
            self.repeat_btn.setStyleSheet(
                f"background-color: {self.theme['accent']}; color: {self.theme['bg_primary']}; border-radius: 20px;"
            )

    def toggle_mute(self):
        if self.audio_output.isMuted():
            self.audio_output.setMuted(False)
            self.volume_btn.setText("\U0001f50a")
        else:
            self.audio_output.setMuted(True)
            self.volume_btn.setText("\U0001f507")

    def change_volume(self, value):
        self.audio_output.setVolume(value / 100.0)
        if value == 0:
            self.volume_btn.setText("\U0001f507")
        elif value < 50:
            self.volume_btn.setText("\U0001f509")
        else:
            self.volume_btn.setText("\U0001f50a")

    def on_position_changed(self, position):
        if not self.slider_pressed:
            if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
                duration = self.player.duration()
                if duration > 0:
                    self.progress_slider.setValue(int(position / duration * 1000))
        self.time_current.setText(format_time(position))

    def on_duration_changed(self, duration):
        self.time_total.setText(format_time(duration))
        self.progress_slider.setRange(0, 1000)

    def on_state_changed(self, state):
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_btn.setText("\u23f8")
        else:
            self.play_btn.setText("\u25b6")

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.play_next()

    def on_slider_pressed(self):
        self.slider_pressed = True

    def on_slider_released(self):
        self.slider_pressed = False
        duration = self.player.duration()
        if duration > 0:
            new_pos = int(self.progress_slider.value() / 1000 * duration)
            self.player.setPosition(new_pos)

    # ==================== PLAYLISTS ====================

    def create_playlist(self):
        name, ok = QInputDialog.getText(self, "New Playlist", "Playlist name:")
        if ok and name.strip():
            name = name.strip()
            if name not in self.playlists:
                self.playlists[name] = []
                self.refresh_playlist_list()
                self.save_data()

    def refresh_playlist_list(self):
        self.playlist_list.clear()
        all_item = PlaylistListItem("All Tracks", len(self.tracks))
        all_item.setData(Qt.ItemDataRole.UserRole, "all")
        self.playlist_list.addItem(all_item)
        for name, tracks in self.playlists.items():
            item = PlaylistListItem(name, len(tracks))
            item.setData(Qt.ItemDataRole.UserRole, name)
            self.playlist_list.addItem(item)

    def on_playlist_selected(self, item):
        playlist_name = item.data(Qt.ItemDataRole.UserRole)
        if playlist_name == "all":
            self.current_playlist = None
            self.current_view_title.setText("All Tracks")
            self.refresh_track_list()
        else:
            self.current_playlist = playlist_name
            self.current_view_title.setText(playlist_name)
            self.track_list.clear()
            for track_path in self.playlists.get(playlist_name, []):
                track = next((t for t in self.tracks if t["path"] == track_path), None)
                if track:
                    self.track_list.addItem(TrackListItem(track))

    def show_playlist_context(self, pos):
        item = self.playlist_list.itemAt(pos)
        if not item:
            return
        playlist_name = item.data(Qt.ItemDataRole.UserRole)
        if playlist_name == "all":
            return
        menu = QMenu(self)
        add_action = menu.addAction("Add current track to this playlist")
        add_action.triggered.connect(lambda: self.add_current_to_playlist(playlist_name))
        del_action = menu.addAction("Delete playlist")
        del_action.triggered.connect(lambda: self.delete_playlist(playlist_name))
        menu.exec(self.playlist_list.mapToGlobal(pos))

    def add_current_to_playlist(self, playlist_name):
        if self.current_track_index >= 0:
            track_path = self.tracks[self.current_track_index]["path"]
            if track_path not in self.playlists[playlist_name]:
                self.playlists[playlist_name].append(track_path)
                self.refresh_playlist_list()
                self.save_data()
                self.show_status(f"Added to {playlist_name}")

    def delete_playlist(self, name):
        reply = QMessageBox.question(
            self, "Delete Playlist",
            f"Delete playlist '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            del self.playlists[name]
            if self.current_playlist == name:
                self.current_playlist = None
                self.current_view_title.setText("All Tracks")
                self.refresh_track_list()
            self.refresh_playlist_list()
            self.save_data()

    def show_track_context(self, pos):
        item = self.track_list.itemAt(pos)
        if not item:
            return
        menu = QMenu(self)
        play = menu.addAction("Play")
        play.triggered.connect(lambda: self.play_track(item.track))
        menu.addSeparator()
        if self.playlists:
            add_submenu = menu.addMenu("Add to playlist")
            for pl_name in self.playlists.keys():
                action = add_submenu.addAction(pl_name)
                action.triggered.connect(lambda checked, n=pl_name: self.add_track_to_playlist(item.track, n))
        else:
            add_to_new = menu.addAction("Create playlist and add...")
            add_to_new.triggered.connect(lambda: self.create_playlist_and_add(item.track))
        remove = menu.addAction("Remove from library")
        remove.triggered.connect(lambda: self.remove_track(item.track))
        menu.exec(self.track_list.mapToGlobal(pos))

    def add_track_to_playlist(self, track, playlist_name):
        if track["path"] not in self.playlists[playlist_name]:
            self.playlists[playlist_name].append(track["path"])
            self.refresh_playlist_list()
            self.save_data()
            self.show_status(f"Added to {playlist_name}")

    def create_playlist_and_add(self, track):
        name, ok = QInputDialog.getText(self, "New Playlist", "Playlist name:")
        if ok and name.strip():
            name = name.strip()
            self.playlists[name] = [track["path"]]
            self.refresh_playlist_list()
            self.save_data()
            self.show_status(f"Created '{name}' and added track")

    def remove_track(self, track):
        self.tracks = [t for t in self.tracks if t["path"] != track["path"]]
        for pl in self.playlists.values():
            if track["path"] in pl:
                pl.remove(track["path"])
        if self.current_track_index >= 0 and self.tracks[self.current_track_index]["path"] == track["path"]:
            self.player.stop()
            self.current_track_index = -1
        self.refresh_track_list()
        self.refresh_playlist_list()
        self.save_data()

    # ==================== SAVE/LOAD ====================

    def save_data(self):
        data = {
            "tracks": self.tracks,
            "playlists": self.playlists,
            "current_theme": self.current_theme_name,
            "volume": self.volume_slider.value(),
        }
        config_path = os.path.join(SCRIPT_DIR, "config.json")
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

    def load_saved_data(self):
        config_path = os.path.join(SCRIPT_DIR, "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.tracks = data.get("tracks", [])
                self.playlists = data.get("playlists", {})
                theme = data.get("current_theme", "Midnight")
                self.theme_combo.setCurrentText(theme)
                self.apply_theme(theme)
                vol = data.get("volume", 70)
                self.volume_slider.setValue(vol)
                self.audio_output.setVolume(vol / 100.0)
            except Exception as e:
                print(f"Error loading config: {e}")
        for track in self.tracks:
            if not track.get("cover_path") and os.path.exists(track["path"]):
                info = get_track_info(track["path"])
                track["cover_path"] = info.get("cover_path")
        self.refresh_track_list()
        self.refresh_playlist_list()

    def show_status(self, message):
        self.statusBar().showMessage(message, 3000)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("SonicWave Player")

    window = MusicPlayer()
    window.show()
    window.raise_()
    window.activateWindow()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
