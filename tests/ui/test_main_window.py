import pytest
from src.views.main_window import MainWindow
import customtkinter as ctk
from unittest.mock import MagicMock

class TestMainWindow:
    """Test suite for the main window of the application."""

    def test_main_window_initialization(self):
        """Test main window initialization."""
        controller = None  # Mock controller
        window = MainWindow(controller)
        assert window.title() == "Break Assistant"
        assert window.winfo_width() > 0
        assert window.winfo_height() > 0

    def test_main_window_geometry(self):
        """Test main window geometry."""
        controller = None  # Mock controller
        window = MainWindow(controller)
        window.update_idletasks()
        assert "500x460" in window.geometry()