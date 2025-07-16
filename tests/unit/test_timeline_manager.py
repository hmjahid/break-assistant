import pytest
from datetime import datetime, time, timedelta
from src.models.timeline_manager import TimelineManager, BreakSlot


class TestBreakSlot:
    """Test cases for BreakSlot class."""

    def test_break_slot_initialization(self):
        """Test break slot initialization."""
        slot = BreakSlot(time(10, 30), 15, "Test break", "daily")
        
        assert slot.start_time == time(10, 30)
        assert slot.duration == 15
        assert slot.message == "Test break"
        assert slot.repeat_pattern == "daily"
        assert slot.enabled is True
        assert slot.id is not None

    def test_break_slot_id_generation(self):
        """Test break slot ID generation."""
        slot1 = BreakSlot(time(10, 30), 15, "Break 1", "daily")
        slot2 = BreakSlot(time(10, 30), 15, "Break 2", "daily")
        slot3 = BreakSlot(time(10, 30), 20, "Break 3", "daily")
        
        assert slot1.id == slot2.id  # Same time, duration, pattern
        assert slot1.id != slot3.id  # Different duration

    def test_break_slot_to_dict(self):
        """Test break slot to dictionary conversion."""
        slot = BreakSlot(time(10, 30), 15, "Test break", "daily")
        data = slot.to_dict()
        
        assert data["start_time"] == "10:30"
        assert data["duration"] == 15
        assert data["message"] == "Test break"
        assert data["repeat_pattern"] == "daily"
        assert data["enabled"] is True
        assert "id" in data

    def test_break_slot_from_dict(self):
        """Test break slot creation from dictionary."""
        data = {
            "id": "test_id",
            "start_time": "10:30",
            "duration": 15,
            "message": "Test break",
            "repeat_pattern": "daily",
            "enabled": True
        }
        
        slot = BreakSlot.from_dict(data)
        
        assert slot.start_time == time(10, 30)
        assert slot.duration == 15
        assert slot.message == "Test break"
        assert slot.repeat_pattern == "daily"
        assert slot.enabled is True

    def test_break_slot_is_active_today(self):
        """Test break slot active status for different patterns."""
        # Test daily pattern
        slot_daily = BreakSlot(time(10, 30), 15, "", "daily")
        assert slot_daily.is_active_today(datetime.now())
        
        # Test weekdays pattern
        slot_weekdays = BreakSlot(time(10, 30), 15, "", "weekdays")
        current_weekday = datetime.now().weekday()
        expected_weekdays = current_weekday < 5
        assert slot_weekdays.is_active_today(datetime.now()) == expected_weekdays
        
        # Test weekends pattern
        slot_weekends = BreakSlot(time(10, 30), 15, "", "weekends")
        expected_weekends = current_weekday >= 5
        assert slot_weekends.is_active_today(datetime.now()) == expected_weekends
        
        # Test disabled slot
        slot_disabled = BreakSlot(time(10, 30), 15, "", "daily", enabled=False)
        assert not slot_disabled.is_active_today(datetime.now())

    def test_break_slot_get_next_occurrence(self):
        """Test getting next occurrence of break slot."""
        # Test future occurrence
        future_time = datetime.now() + timedelta(hours=1)
        slot = BreakSlot(future_time.time(), 15, "", "daily")
        
        occurrence = slot.get_next_occurrence(datetime.now())
        assert occurrence is not None
        assert occurrence.time() == future_time.time()
        
        # Test past occurrence (should return None)
        past_time = datetime.now() - timedelta(hours=1)
        slot_past = BreakSlot(past_time.time(), 15, "", "daily")
        
        occurrence = slot_past.get_next_occurrence(datetime.now())
        assert occurrence is None


class TestTimelineManager:
    """Test cases for TimelineManager class."""

    def test_timeline_manager_initialization(self, timeline_manager):
        """Test timeline manager initialization."""
        assert timeline_manager.break_slots == []
        assert timeline_manager.timeline_file is not None

    def test_add_break_slot(self, timeline_manager):
        """Test adding a break slot."""
        slot = timeline_manager.add_break_slot(time(10, 30), 15, "Test break", "daily")
        
        assert len(timeline_manager.break_slots) == 1
        assert slot.start_time == time(10, 30)
        assert slot.duration == 15
        assert slot.message == "Test break"
        assert slot.repeat_pattern == "daily"

    def test_add_break_slot_overlap(self, timeline_manager):
        """Test adding overlapping break slots."""
        # Add first slot
        timeline_manager.add_break_slot(time(10, 0), 30, "First break", "daily")
        
        # Try to add overlapping slot
        with pytest.raises(ValueError, match="overlaps"):
            timeline_manager.add_break_slot(time(10, 15), 30, "Overlapping break", "daily")

    def test_edit_break_slot(self, timeline_manager):
        """Test editing a break slot."""
        # Add a slot
        original_slot = timeline_manager.add_break_slot(time(10, 30), 15, "Original", "daily")
        
        # Edit the slot
        edited_slot = timeline_manager.edit_break_slot(
            original_slot.id,
            start_time=time(11, 0),
            duration=20,
            message="Updated",
            repeat_pattern="weekdays"
        )
        
        assert edited_slot.start_time == time(11, 0)
        assert edited_slot.duration == 20
        assert edited_slot.message == "Updated"
        assert edited_slot.repeat_pattern == "weekdays"

    def test_delete_break_slot(self, timeline_manager):
        """Test deleting a break slot."""
        # Add a slot
        slot = timeline_manager.add_break_slot(time(10, 30), 15, "Test break", "daily")
        
        # Delete the slot
        result = timeline_manager.delete_break_slot(slot.id)
        
        assert result is True
        assert len(timeline_manager.break_slots) == 0

    def test_get_break_slot(self, timeline_manager):
        """Test getting a break slot by ID."""
        # Add a slot
        added_slot = timeline_manager.add_break_slot(time(10, 30), 15, "Test break", "daily")
        
        # Get the slot
        retrieved_slot = timeline_manager.get_break_slot(added_slot.id)
        
        assert retrieved_slot is not None
        assert retrieved_slot.id == added_slot.id
        assert retrieved_slot.start_time == added_slot.start_time

    def test_get_all_break_slots(self, timeline_manager, sample_break_slots):
        """Test getting all break slots."""
        # Add multiple slots
        for slot in sample_break_slots:
            timeline_manager.break_slots.append(slot)
        
        all_slots = timeline_manager.get_all_break_slots()
        
        assert len(all_slots) == len(sample_break_slots)
        assert all_slots == sample_break_slots

    def test_get_active_break_slots(self, timeline_manager):
        """Test getting active break slots for current date."""
        # Add slots with different patterns
        timeline_manager.add_break_slot(time(10, 0), 15, "Daily", "daily")
        timeline_manager.add_break_slot(time(11, 0), 15, "Weekdays", "weekdays")
        timeline_manager.add_break_slot(time(12, 0), 15, "Weekends", "weekends")
        timeline_manager.add_break_slot(time(13, 0), 15, "Disabled", "daily", enabled=False)
        
        current_datetime = datetime.now()
        active_slots = timeline_manager.get_active_break_slots(current_datetime)
        
        # Should have at least the daily slot
        assert len(active_slots) >= 1
        
        # Check that disabled slot is not included
        disabled_slots = [slot for slot in active_slots if not slot.enabled]
        assert len(disabled_slots) == 0

    def test_get_next_break(self, timeline_manager):
        """Test getting the next break."""
        # Add a future break
        future_time = datetime.now() + timedelta(hours=1)
        timeline_manager.add_break_slot(future_time.time(), 15, "Future break", "daily")
        
        next_break = timeline_manager.get_next_break(datetime.now())
        
        assert next_break is not None
        break_slot, occurrence_time = next_break
        assert break_slot.start_time == future_time.time()

    def test_validate_timeline(self, timeline_manager):
        """Test timeline validation."""
        # Add valid slots
        timeline_manager.add_break_slot(time(9, 0), 15, "Morning", "daily")
        timeline_manager.add_break_slot(time(12, 0), 30, "Lunch", "daily")
        
        errors = timeline_manager.validate_timeline()
        assert len(errors) == 0
        
        # Add invalid slot (duration too long)
        timeline_manager.add_break_slot(time(15, 0), 150, "Invalid", "daily")
        errors = timeline_manager.validate_timeline()
        assert len(errors) > 0
        assert any("duration too long" in error for error in errors)

    def test_save_and_load_timeline(self, timeline_manager):
        """Test saving and loading timeline."""
        # Add some slots
        timeline_manager.add_break_slot(time(9, 0), 15, "Morning", "daily")
        timeline_manager.add_break_slot(time(12, 0), 30, "Lunch", "daily")
        
        # Save timeline
        timeline_manager.save_timeline()
        
        # Create new manager and load timeline
        new_manager = TimelineManager()
        new_manager.timeline_file = timeline_manager.timeline_file
        new_manager.load_timeline()
        
        assert len(new_manager.break_slots) == 2
        assert new_manager.break_slots[0].start_time == time(9, 0)
        assert new_manager.break_slots[1].start_time == time(12, 0)

    def test_sort_slots(self, timeline_manager):
        """Test that slots are sorted by start time."""
        # Add slots in random order
        timeline_manager.add_break_slot(time(12, 0), 30, "Lunch", "daily")
        timeline_manager.add_break_slot(time(9, 0), 15, "Morning", "daily")
        timeline_manager.add_break_slot(time(15, 0), 10, "Afternoon", "daily")
        
        # Check that slots are sorted
        assert timeline_manager.break_slots[0].start_time == time(9, 0)
        assert timeline_manager.break_slots[1].start_time == time(12, 0)
        assert timeline_manager.break_slots[2].start_time == time(15, 0) 