import pytest
import customtkinter as ctk
from datetime import time
from src.views.timeline_page import TimelinePage, BreakSlotDialog
from src.models.timeline_manager import TimelineManager, BreakSlot


class TestTimelineUI:
    """UI tests for timeline components."""

    def test_timeline_page_creation(self, mock_controller):
        """Test timeline page creation."""
        root = ctk.CTk()
        timeline_page = TimelinePage(root, mock_controller)
        
        assert timeline_page is not None
        assert hasattr(timeline_page, 'timeline_manager')
        assert hasattr(timeline_page, 'controller')
        
        root.destroy()

    def test_break_slot_dialog_creation(self, mock_controller):
        """Test break slot dialog creation."""
        root = ctk.CTk()
        dialog = BreakSlotDialog(root, "Add Break Slot", lambda *args: None)
        
        assert dialog is not None
        assert dialog.title() == "Add Break Slot"
        
        root.destroy()

    def test_timeline_page_add_break_slot(self, mock_controller, temp_dir):
        """Test adding break slot through UI."""
        # Setup timeline manager with temporary file
        mock_controller.timeline_manager.timeline_file = temp_dir / "timeline.json"
        
        root = ctk.CTk()
        timeline_page = TimelinePage(root, mock_controller)
        
        # Test adding break slot
        slot = timeline_page.timeline_manager.add_break_slot(
            time(10, 30), 15, "Test break", "daily"
        )
        
        assert slot is not None
        assert slot.start_time == time(10, 30)
        assert slot.duration == 15
        assert slot.message == "Test break"
        assert slot.repeat_pattern == "daily"
        
        # Verify slot was added to timeline
        all_slots = timeline_page.timeline_manager.get_all_break_slots()
        assert len(all_slots) == 1
        assert all_slots[0].id == slot.id
        
        root.destroy()

    def test_timeline_page_refresh_display(self, mock_controller, temp_dir):
        """Test timeline page display refresh."""
        # Setup timeline manager with temporary file
        mock_controller.timeline_manager.timeline_file = temp_dir / "timeline.json"
        
        root = ctk.CTk()
        timeline_page = TimelinePage(root, mock_controller)
        
        # Add break slots
        timeline_page.timeline_manager.add_break_slot(time(9, 0), 15, "Morning", "daily")
        timeline_page.timeline_manager.add_break_slot(time(12, 0), 30, "Lunch", "daily")
        
        # Refresh display
        timeline_page.refresh_timeline()
        
        # Verify slots are displayed
        # Note: In a real test, we'd check the actual UI elements
        all_slots = timeline_page.timeline_manager.get_all_break_slots()
        assert len(all_slots) == 2
        
        root.destroy()

    def test_break_slot_dialog_save(self, mock_controller):
        """Test break slot dialog save functionality."""
        root = ctk.CTk()
        
        saved_data = []
        def save_callback(start_time, duration, message, repeat_pattern):
            saved_data.append((start_time, duration, message, repeat_pattern))
        
        dialog = BreakSlotDialog(root, "Add Break Slot", save_callback)
        
        # Simulate setting values (in a real test, we'd interact with UI elements)
        dialog.hour_var.set("10")
        dialog.minute_var.set("30")
        dialog.duration_var.set("15")
        dialog.message_text.delete("1.0", "end")
        dialog.message_text.insert("1.0", "Test break")
        dialog.pattern_var.set("daily")
        
        # Simulate save
        dialog.save_slot()
        
        # Verify callback was called
        assert len(saved_data) == 1
        start_time, duration, message, repeat_pattern = saved_data[0]
        assert start_time == time(10, 30)
        assert duration == 15
        assert message == "Test break"
        assert repeat_pattern == "daily"
        
        root.destroy()

    def test_timeline_page_validation(self, mock_controller, temp_dir):
        """Test timeline page validation."""
        # Setup timeline manager with temporary file
        mock_controller.timeline_manager.timeline_file = temp_dir / "timeline.json"
        
        root = ctk.CTk()
        timeline_page = TimelinePage(root, mock_controller)
        
        # Add valid slots
        timeline_page.timeline_manager.add_break_slot(time(9, 0), 15, "Morning", "daily")
        timeline_page.timeline_manager.add_break_slot(time(12, 0), 30, "Lunch", "daily")
        
        # Validate timeline
        errors = timeline_page.timeline_manager.validate_timeline()
        assert len(errors) == 0
        
        # Add invalid slot (duration too long)
        timeline_page.timeline_manager.add_break_slot(time(15, 0), 150, "Invalid", "daily")
        errors = timeline_page.timeline_manager.validate_timeline()
        assert len(errors) > 0
        assert any("duration too long" in error for error in errors)
        
        root.destroy()

    def test_timeline_page_delete_slot(self, mock_controller, temp_dir):
        """Test deleting break slot through UI."""
        # Setup timeline manager with temporary file
        mock_controller.timeline_manager.timeline_file = temp_dir / "timeline.json"
        
        root = ctk.CTk()
        timeline_page = TimelinePage(root, mock_controller)
        
        # Add break slot
        slot = timeline_page.timeline_manager.add_break_slot(time(10, 30), 15, "Test break", "daily")
        
        # Select the slot
        timeline_page.selected_slot = slot
        
        # Delete the slot
        result = timeline_page.delete_selected_slot()
        
        # Verify slot was deleted
        assert result is True
        assert len(timeline_page.timeline_manager.break_slots) == 0
        
        root.destroy()

    def test_timeline_page_edit_slot(self, mock_controller, temp_dir):
        """Test editing break slot through UI."""
        # Setup timeline manager with temporary file
        mock_controller.timeline_manager.timeline_file = temp_dir / "timeline.json"
        
        root = ctk.CTk()
        timeline_page = TimelinePage(root, mock_controller)
        
        # Add break slot
        original_slot = timeline_page.timeline_manager.add_break_slot(
            time(10, 30), 15, "Original", "daily"
        )
        
        # Edit the slot
        edited_slot = timeline_page.timeline_manager.edit_break_slot(
            original_slot.id,
            start_time=time(11, 0),
            duration=20,
            message="Updated",
            repeat_pattern="weekdays"
        )
        
        # Verify slot was updated
        assert edited_slot.start_time == time(11, 0)
        assert edited_slot.duration == 20
        assert edited_slot.message == "Updated"
        assert edited_slot.repeat_pattern == "weekdays"
        
        root.destroy()

    def test_timeline_page_error_handling(self, mock_controller, temp_dir):
        """Test timeline page error handling."""
        # Setup timeline manager with temporary file
        mock_controller.timeline_manager.timeline_file = temp_dir / "timeline.json"
        
        root = ctk.CTk()
        timeline_page = TimelinePage(root, mock_controller)
        
        # Try to add overlapping slots
        timeline_page.timeline_manager.add_break_slot(time(10, 0), 30, "First break", "daily")
        
        # This should raise an error
        with pytest.raises(ValueError, match="overlaps"):
            timeline_page.timeline_manager.add_break_slot(time(10, 15), 30, "Overlapping break", "daily")
        
        root.destroy()

    def test_timeline_page_details_display(self, mock_controller, temp_dir):
        """Test timeline page details display."""
        # Setup timeline manager with temporary file
        mock_controller.timeline_manager.timeline_file = temp_dir / "timeline.json"
        
        root = ctk.CTk()
        timeline_page = TimelinePage(root, mock_controller)
        
        # Add break slot
        slot = timeline_page.timeline_manager.add_break_slot(
            time(10, 30), 15, "Test break", "daily"
        )
        
        # Select the slot
        timeline_page.select_slot(slot)
        
        # Update details display
        timeline_page.update_details()
        
        # Verify slot is selected
        assert timeline_page.selected_slot == slot
        
        root.destroy()

    def test_timeline_page_complex_scenario(self, mock_controller, temp_dir):
        """Test complex timeline page scenario."""
        # Setup timeline manager with temporary file
        mock_controller.timeline_manager.timeline_file = temp_dir / "timeline.json"
        
        root = ctk.CTk()
        timeline_page = TimelinePage(root, mock_controller)
        
        # Add multiple break slots
        slots_data = [
            (time(9, 0), 15, "Morning stretch", "daily"),
            (time(12, 0), 30, "Lunch break", "daily"),
            (time(15, 0), 10, "Afternoon break", "weekdays"),
            (time(17, 30), 15, "End of day", "daily")
        ]
        
        for start_time, duration, message, pattern in slots_data:
            slot = timeline_page.timeline_manager.add_break_slot(start_time, duration, message, pattern)
        
        # Refresh display
        timeline_page.refresh_timeline()
        
        # Verify all slots were added
        all_slots = timeline_page.timeline_manager.get_all_break_slots()
        assert len(all_slots) == 4
        
        # Test selecting a slot
        if all_slots:
            timeline_page.select_slot(all_slots[0])
            assert timeline_page.selected_slot == all_slots[0]
        
        # Test validation
        errors = timeline_page.timeline_manager.validate_timeline()
        assert len(errors) == 0
        
        # Test saving timeline
        timeline_page.timeline_manager.save_timeline()
        
        # Verify timeline file was created
        assert timeline_page.timeline_manager.timeline_file.exists()
        
        root.destroy() 