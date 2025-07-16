import pytest
from src.controllers.app_controller import AppController


class TestAppController:
    """Integration tests for AppController."""

    def test_app_controller_initialization(self):
        """Test app controller initialization."""
        controller = AppController()
        assert controller is not None
        assert hasattr(controller, 'main_window')

    def test_app_controller_run(self):
        """Test app controller run method."""
        controller = AppController()
        # This test will be updated when run() is fully implemented
        # For now, we just test that the method exists
        assert hasattr(controller, 'run') 