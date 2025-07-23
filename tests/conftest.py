import pytest
import tempfile
import shutil
from pathlib import Path
from src.models.timeline_manager import TimelineManager, BreakSlot
from src.models.settings import SettingsManager
from datetime import datetime, time


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def timeline_manager(temp_dir):
    """Create a TimelineManager with temporary file."""
    manager = TimelineManager()
    manager.timeline_file = temp_dir / "timeline.json"
    manager.break_slots = [] # Clear break slots for each test
    return manager


@pytest.fixture
def settings_manager(temp_dir):
    """Create a SettingsManager with temporary file."""
    manager = SettingsManager()
    manager.settings_file = temp_dir / "settings.json"
    return manager


@pytest.fixture
def sample_break_slot():
    """Create a sample break slot for testing."""
    return BreakSlot(
        start_time=time(10, 30),  # 10:30 AM
        duration=15,
        message="Morning break",
        repeat_pattern="daily",
        enabled=True
    )


@pytest.fixture
def sample_break_slots():
    """Create multiple sample break slots for testing."""
    return [
        BreakSlot(time(9, 0), 5, "Quick stretch", "daily"),
        BreakSlot(time(12, 0), 30, "Lunch break", "daily"),
        BreakSlot(time(15, 0), 10, "Afternoon break", "weekdays"),
        BreakSlot(time(17, 30), 15, "End of day", "daily")
    ]


@pytest.fixture
def mock_controller(temp_dir):
    """Create a mock controller for testing."""
    class MockController:
        def __init__(self):
            self.timeline_manager = TimelineManager()
            self.timeline_manager.timeline_file = temp_dir / "timeline.json"
            self.timeline_manager.break_slots = []
            self.settings_manager = SettingsManager()
            self.settings_manager.settings_file = temp_dir / "settings.json"
        
        def get_timeline_manager(self):
            return self.timeline_manager
        
        def get_settings_manager(self):
            return self.settings_manager
    
    return MockController() 