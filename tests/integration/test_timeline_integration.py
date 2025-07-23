import pytest
from datetime import datetime, time, timedelta
from src.controllers.app_controller import AppController
from src.models.timeline_manager import TimelineManager, BreakSlot


class TestTimelineIntegration:
    """Integration tests for timeline functionality."""

    def test_controller_timeline_integration(self, temp_dir):
        """Test timeline integration with app controller."""
        # Create controller with temporary files
        controller = AppController(timeline_file=temp_dir / "timeline.json", settings_file=temp_dir / "settings.json")
        
        # Test adding break slot through controller
        timeline_manager = controller.get_timeline_manager()
        slot = timeline_manager.add_break_slot(time(10, 30), 15, "Test break", "daily")
        
        assert slot is not None
        assert slot.start_time == time(10, 30)
        assert slot.duration == 15
        
        # Test getting next break through controller
        next_break = controller.get_next_break()
        assert next_break is not None
        break_slot, occurrence_time = next_break
        assert break_slot.id == slot.id

    def test_timeline_persistence_integration(self, temp_dir):
        """Test timeline persistence through controller."""
        # Create controller
        controller = AppController(timeline_file=temp_dir / "timeline.json", settings_file=temp_dir / "settings.json")
        
        # Add break slots
        timeline_manager = controller.get_timeline_manager()
        timeline_manager.add_break_slot(time(9, 0), 15, "Morning", "daily")
        timeline_manager.add_break_slot(time(12, 0), 30, "Lunch", "daily")
        
        # Save timeline
        timeline_manager.save_timeline()
        
        # Create new controller and load timeline
        new_controller = AppController(timeline_file=temp_dir / "timeline.json", settings_file=temp_dir / "settings.json")
        
        # Load timeline
        new_timeline_manager = new_controller.get_timeline_manager()
        new_timeline_manager.load_timeline()
        
        # Verify slots were loaded
        assert len(new_timeline_manager.break_slots) == 2
        assert new_timeline_manager.break_slots[0].start_time == time(9, 0)
        assert new_timeline_manager.break_slots[1].start_time == time(12, 0)

    def test_timeline_validation_integration(self, temp_dir):
        """Test timeline validation through controller."""
        controller = AppController(timeline_file=temp_dir / "timeline.json", settings_file=temp_dir / "settings.json")
        
        timeline_manager = controller.get_timeline_manager()
        
        # Add valid slots
        timeline_manager.add_break_slot(time(9, 0), 15, "Morning", "daily")
        timeline_manager.add_break_slot(time(12, 0), 30, "Lunch", "daily")
        
        # Validate timeline
        errors = timeline_manager.validate_timeline()
        assert len(errors) == 0
        
        # Add invalid slot
        timeline_manager.add_break_slot(time(15, 0), 150, "Invalid", "daily")
        errors = timeline_manager.validate_timeline()
        assert len(errors) > 0

    def test_timeline_break_notification_integration(self, temp_dir):
        """Test break notification integration with timeline."""
        controller = AppController(timeline_file=temp_dir / "timeline.json", settings_file=temp_dir / "settings.json")
        
        # Add a future break
        future_time = datetime.now() + timedelta(minutes=5)
        timeline_manager = controller.get_timeline_manager()
        slot = timeline_manager.add_break_slot(future_time.time(), 15, "Test break", "daily")
        
        # Test notification sound
        controller.play_notification_sound()
        # Note: In a real test, we'd mock the audio manager
        
        # Test getting next break
        next_break = controller.get_next_break()
        assert next_break is not None
        break_slot, occurrence_time = next_break
        assert break_slot.id == slot.id

    def test_timeline_settings_integration(self, temp_dir):
        """Test timeline integration with settings."""
        controller = AppController(timeline_file=temp_dir / "timeline.json", settings_file=temp_dir / "settings.json")
        
        # Test saving settings
        settings = {
            "sound_enabled": True,
            "sound_file": "alert.wav",
            "theme": "dark"
        }
        controller.save_settings(settings)
        
        # Test loading settings
        loaded_settings = controller.load_settings()
        assert loaded_settings["sound_enabled"] is True
        assert loaded_settings["sound_file"] == "alert.wav"
        assert loaded_settings["theme"] == "dark"

    def test_timeline_platform_integration(self, temp_dir):
        """Test timeline integration with platform utilities."""
        controller = AppController(timeline_file=temp_dir / "timeline.json", settings_file=temp_dir / "settings.json")
        
        # Test platform detection
        platform = controller.get_platform()
        assert platform in ["windows", "macos", "linux", "unknown"]
        
        # Test platform-specific functionality
        platform_utils = controller.get_platform_utils()
        detected_platform = platform_utils.get_platform()
        assert detected_platform == platform

    def test_timeline_theme_integration(self, temp_dir):
        """Test timeline integration with theme management."""
        controller = AppController(timeline_file=temp_dir / "timeline.json", settings_file=temp_dir / "settings.json")
        
        # Test theme application
        controller.apply_theme("dark")
        
        # Verify theme was saved
        settings = controller.load_settings()
        assert settings["theme"] == "dark"
        
        # Test theme manager
        theme_manager = controller.get_theme_manager()
        assert theme_manager is not None

    def test_timeline_audio_integration(self, temp_dir):
        """Test timeline integration with audio management."""
        controller = AppController(timeline_file=temp_dir / "timeline.json", settings_file=temp_dir / "settings.json")
        
        # Test audio manager
        audio_manager = controller.get_audio_manager()
        assert audio_manager is not None
        
        # Test notification sound
        controller.play_notification_sound()
        # Note: In a real test, we'd verify the sound was played

    def test_timeline_complex_scenario(self, temp_dir):
        """Test complex timeline scenario with multiple components."""
        controller = AppController(timeline_file=temp_dir / "timeline.json", settings_file=temp_dir / "settings.json")
        
        # Setup complex timeline
        timeline_manager = controller.get_timeline_manager()
        
        # Add multiple break slots
        slots = [
            (time(9, 0), 15, "Morning stretch", "daily"),
            (time(12, 0), 30, "Lunch break", "daily"),
            (time(15, 0), 10, "Afternoon break", "weekdays"),
            (time(17, 30), 15, "End of day", "daily")
        ]
        
        for start_time, duration, message, pattern in slots:
            timeline_manager.add_break_slot(start_time, duration, message, pattern)
        
        # Verify timeline
        assert len(timeline_manager.break_slots) == 4
        
        # Test active slots for current date
        current_datetime = datetime.now()
        active_slots = timeline_manager.get_active_break_slots(current_datetime)
        
        # Should have at least daily slots
        daily_slots = [slot for slot in active_slots if slot.repeat_pattern == "daily"]
        assert len(daily_slots) >= 3
        
        # Test next break
        next_break = controller.get_next_break()
        if next_break:
            break_slot, occurrence_time = next_break
            assert break_slot is not None
            assert occurrence_time > current_datetime
        
        # Test settings integration
        controller.save_settings({
            "sound_enabled": True,
            "theme": "light"
        })
        
        # Test persistence
        timeline_manager.save_timeline()
        
        # Create new controller and verify persistence
        new_controller = AppController(timeline_file=temp_dir / "timeline.json", settings_file=temp_dir / "settings.json")
        
        new_timeline_manager = new_controller.get_timeline_manager()
        new_timeline_manager.load_timeline()
        
        assert len(new_timeline_manager.break_slots) == 4
        
        # Verify settings were persisted
        settings = new_controller.load_settings()
        assert settings["sound_enabled"] is True
        assert settings["theme"] == "light"