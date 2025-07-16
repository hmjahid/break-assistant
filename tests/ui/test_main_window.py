import pytest
import customtkinter as ctk
from src.views.main_window import MainWindow


class TestMainWindow:
    """UI tests for MainWindow."""

    def test_main_window_creation(self):
        """Test main window creation."""
        controller = None  # Mock controller
        window = MainWindow(controller)
        assert isinstance(window, ctk.CTk)
        assert window.title() == "Break Assistant"

    def test_main_window_geometry(self):
        """Test main window geometry."""
        controller = None  # Mock controller
        window = MainWindow(controller)
        assert window.geometry() == "400x300" 