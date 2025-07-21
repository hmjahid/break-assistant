from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, time, timedelta
import json
import logging
import os

logger = logging.getLogger(__name__)


class BreakSlot:
    """Represents a single break slot in the timeline."""
    
    def __init__(self, start_time: time, duration: int, message: str = "", 
                 repeat_pattern: str = "daily", enabled: bool = True) -> None:
        """Initialize a break slot.
        
        Args:
            start_time: Start time of the break
            duration: Duration in minutes
            message: Custom message for this break
            repeat_pattern: Repeat pattern ("daily", "weekdays", "weekends", "once")
            enabled: Whether this break slot is enabled
        """
        self.start_time = start_time
        self.duration = duration
        self.message = message
        self.repeat_pattern = repeat_pattern
        self.enabled = enabled
        self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate unique ID for this break slot."""
        return f"{self.start_time.hour:02d}{self.start_time.minute:02d}_{self.duration}_{self.repeat_pattern}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert break slot to dictionary."""
        return {
            "id": self.id,
            "start_time": self.start_time.strftime("%H:%M"),
            "duration": self.duration,
            "message": self.message,
            "repeat_pattern": self.repeat_pattern,
            "enabled": self.enabled
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BreakSlot':
        """Create break slot from dictionary."""
        start_time = datetime.strptime(data["start_time"], "%H:%M").time()
        try:
            duration = int(data["duration"])
        except (ValueError, TypeError):
            duration = 5  # Default duration if invalid
        return cls(
            start_time=start_time,
            duration=duration,
            message=data.get("message", ""),
            repeat_pattern=data.get("repeat_pattern", "daily"),
            enabled=data.get("enabled", True)
        )
    
    def is_active_today(self, current_date: datetime) -> bool:
        """Check if this break slot is active for the given date.
        
        Args:
            current_date: Current date to check
            
        Returns:
            True if break slot is active today
        """
        if not self.enabled:
            return False
        
        if self.repeat_pattern == "daily":
            return True
        elif self.repeat_pattern == "weekdays":
            return current_date.weekday() < 5  # Monday = 0, Friday = 4
        elif self.repeat_pattern == "weekends":
            return current_date.weekday() >= 5  # Saturday = 5, Sunday = 6
        elif self.repeat_pattern == "once":
            # For "once" pattern, we'd need to store the specific date
            # This is a simplified implementation
            return True
        
        return False
    
    def get_next_occurrence(self, current_datetime: datetime) -> Optional[datetime]:
        """Get the next occurrence of this break slot.
        
        Args:
            current_datetime: Current date and time
            
        Returns:
            Next occurrence datetime or None if no more occurrences today
        """
        if not self.is_active_today(current_datetime):
            return None
        
        # Create datetime for today with the break start time
        today = current_datetime.date()
        break_datetime = datetime.combine(today, self.start_time)
        
        # If the break time has already passed today, return None
        try:
            if break_datetime <= current_datetime:
                return None
        except (TypeError, ValueError):
            # If there's a type error, assume the break has passed
            return None
        
        return break_datetime
    
    def get_next_occurrence_tomorrow(self, current_datetime: datetime) -> Optional[datetime]:
        """Get the next occurrence of this break slot (including tomorrow if needed).
        
        Args:
            current_datetime: Current date and time
            
        Returns:
            Next occurrence datetime or None if no more occurrences
        """
        if not self.is_active_today(current_datetime):
            # Check if it's active tomorrow
            tomorrow = current_datetime.date() + timedelta(days=1)
            tomorrow_datetime = datetime.combine(tomorrow, current_datetime.time())
            if self.is_active_today(tomorrow_datetime):
                return datetime.combine(tomorrow, self.start_time)
            return None
        
        # Create datetime for today with the break start time
        today = current_datetime.date()
        break_datetime = datetime.combine(today, self.start_time)
        
        # If the break time has already passed today, check tomorrow
        try:
            if break_datetime <= current_datetime:
                # Check tomorrow
                tomorrow = today + timedelta(days=1)
                tomorrow_datetime = datetime.combine(tomorrow, current_datetime.time())
                if self.is_active_today(tomorrow_datetime):
                    return datetime.combine(tomorrow, self.start_time)
                return None
        except (TypeError, ValueError):
            # If there's a type error, check tomorrow
            tomorrow = today + timedelta(days=1)
            tomorrow_datetime = datetime.combine(tomorrow, current_datetime.time())
            if self.is_active_today(tomorrow_datetime):
                return datetime.combine(tomorrow, self.start_time)
            return None
        
        return break_datetime


class TimelineManager:
    """Manages custom break timeline and scheduling."""
    
    def __init__(self) -> None:
        """Initialize timeline manager.
        
        Args:
            timeline_file: Path to timeline file
        """
        self.break_slots: List[BreakSlot] = []
        CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "break-assistant")
        os.makedirs(CONFIG_DIR, exist_ok=True)
        self.timeline_file = os.path.join(CONFIG_DIR, "timeline.json")
        self.load_timeline()
    
    def add_break_slot(self, start_time: time, duration: int, message: str = "",
                       repeat_pattern: str = "daily", enabled: bool = True) -> BreakSlot:
        """Add a new break slot to the timeline.
        
        Args:
            start_time: Start time of the break
            duration: Duration in minutes
            message: Custom message for this break
            repeat_pattern: Repeat pattern
            enabled: Whether this break slot is enabled
            
        Returns:
            Created break slot
            
        Raises:
            ValueError: If break slot overlaps with existing slots
        """
        new_slot = BreakSlot(start_time, duration, message, repeat_pattern, enabled)
        
        # Check for overlaps
        if self._has_overlap(new_slot):
            raise ValueError(f"Break slot at {start_time.strftime('%H:%M')} overlaps with existing slots")
        
        self.break_slots.append(new_slot)
        self._sort_slots()
        self.save_timeline()
        
        logger.info(f"Added break slot: {start_time.strftime('%H:%M')} ({duration}min)")
        return new_slot
    
    def edit_break_slot(self, slot_id: str, start_time: Optional[time] = None,
                        duration: Optional[int] = None, message: Optional[str] = None,
                        repeat_pattern: Optional[str] = None, enabled: Optional[bool] = None) -> BreakSlot:
        """Edit an existing break slot.
        
        Args:
            slot_id: ID of the break slot to edit
            start_time: New start time
            duration: New duration
            message: New message
            repeat_pattern: New repeat pattern
            enabled: New enabled state
            
        Returns:
            Updated break slot
            
        Raises:
            ValueError: If slot not found or overlap detected
        """
        slot = self.get_break_slot(slot_id)
        if not slot:
            raise ValueError(f"Break slot with ID {slot_id} not found")
        
        # Create temporary slot for overlap checking
        temp_slot = BreakSlot(
            start_time=start_time or slot.start_time,
            duration=duration or slot.duration,
            message=message or slot.message,
            repeat_pattern=repeat_pattern or slot.repeat_pattern,
            enabled=enabled if enabled is not None else slot.enabled
        )
        
        # Check for overlaps (excluding the current slot)
        if self._has_overlap(temp_slot, exclude_id=slot_id):
            raise ValueError(f"Break slot at {temp_slot.start_time.strftime('%H:%M')} overlaps with existing slots")
        
        # Update slot
        if start_time is not None:
            slot.start_time = start_time
        if duration is not None:
            slot.duration = duration
        if message is not None:
            slot.message = message
        if repeat_pattern is not None:
            slot.repeat_pattern = repeat_pattern
        if enabled is not None:
            slot.enabled = enabled
        
        # Regenerate ID if start time changed
        if start_time is not None:
            slot.id = slot._generate_id()
        
        self._sort_slots()
        self.save_timeline()
        
        logger.info(f"Updated break slot: {slot.start_time.strftime('%H:%M')} ({slot.duration}min)")
        return slot
    
    def delete_break_slot(self, slot_id: str) -> bool:
        """Delete a break slot from the timeline.
        
        Args:
            slot_id: ID of the break slot to delete
            
        Returns:
            True if slot was deleted, False if not found
        """
        for i, slot in enumerate(self.break_slots):
            if slot.id == slot_id:
                deleted_slot = self.break_slots.pop(i)
                self.save_timeline()
                logger.info(f"Deleted break slot: {deleted_slot.start_time.strftime('%H:%M')}")
                return True
        
        return False
    
    def get_break_slot(self, slot_id: str) -> Optional[BreakSlot]:
        """Get a break slot by ID.
        
        Args:
            slot_id: ID of the break slot
            
        Returns:
            Break slot or None if not found
        """
        for slot in self.break_slots:
            if slot.id == slot_id:
                return slot
        return None
    
    def get_all_break_slots(self) -> List[BreakSlot]:
        """Get all break slots.
        
        Returns:
            List of all break slots
        """
        return self.break_slots.copy()
    
    def get_active_break_slots(self, current_datetime: datetime) -> List[BreakSlot]:
        """Get break slots that are active for the given date.
        
        Args:
            current_datetime: Current date and time
            
        Returns:
            List of active break slots
        """
        return [slot for slot in self.break_slots if slot.is_active_today(current_datetime)]
    
    def get_next_break(self, current_datetime: datetime) -> Optional[Tuple[BreakSlot, datetime]]:
        """Get the next break slot and its occurrence time.
        
        Args:
            current_datetime: Current date and time
            
        Returns:
            Tuple of (break_slot, occurrence_datetime) or None if no upcoming breaks
        """
        active_slots = self.get_active_break_slots(current_datetime)
        
        next_break = None
        next_occurrence = None
        
        for slot in active_slots:
            # First try to get next occurrence today
            occurrence = slot.get_next_occurrence(current_datetime)
            if occurrence:
                if next_occurrence is None or occurrence < next_occurrence:
                    next_break = slot
                    next_occurrence = occurrence
                continue
            
            # If no occurrence today, try tomorrow
            occurrence = slot.get_next_occurrence_tomorrow(current_datetime)
            try:
                if occurrence and (next_occurrence is None or occurrence < next_occurrence):
                    next_break = slot
                    next_occurrence = occurrence
            except (TypeError, ValueError):
                # If there's a type error, skip this occurrence
                continue
        
        if next_break and next_occurrence:
            return (next_break, next_occurrence)
        
        return None
    
    def _has_overlap(self, new_slot: BreakSlot, exclude_id: Optional[str] = None) -> bool:
        """Check if a break slot overlaps with existing slots.
        
        Args:
            new_slot: Break slot to check
            exclude_id: ID of slot to exclude from overlap check
            
        Returns:
            True if overlap detected
        """
        try:
            new_start = new_slot.start_time
            new_duration = int(new_slot.duration)
            new_end = self._add_minutes_to_time(new_start, new_duration)
            
            for slot in self.break_slots:
                if exclude_id and slot.id == exclude_id:
                    continue
                
                if not slot.enabled:
                    continue
                
                slot_start = slot.start_time
                slot_duration = int(slot.duration)
                slot_end = self._add_minutes_to_time(slot_start, slot_duration)
                
                # Check for overlap
                if (new_start < slot_end and new_end > slot_start):
                    return True
            
            return False
        except (ValueError, TypeError):
            # If there's a type error, assume no overlap to avoid crashes
            return False
    
    def _add_minutes_to_time(self, time_obj: time, minutes: int) -> time:
        """Add minutes to a time object.
        
        Args:
            time_obj: Time object
            minutes: Minutes to add
            
        Returns:
            New time object
        """
        try:
            minutes_int = int(minutes)
            datetime_obj = datetime.combine(datetime.today().date(), time_obj)
            new_datetime = datetime_obj + timedelta(minutes=minutes_int)
            return new_datetime.time()
        except (ValueError, TypeError):
            # If minutes is invalid, return original time
            return time_obj
    
    def _sort_slots(self) -> None:
        """Sort break slots by start time."""
        self.break_slots.sort(key=lambda slot: slot.start_time)
    
    def load_timeline(self) -> None:
        """Load timeline from file."""
        try:
            with open(self.timeline_file, 'r') as f:
                data = json.load(f)
                self.break_slots = [BreakSlot.from_dict(slot_data) for slot_data in data.get("break_slots", [])]
                self._sort_slots()
                logger.info(f"Loaded {len(self.break_slots)} break slots from timeline")
        except FileNotFoundError:
            logger.info("No timeline file found, starting with empty timeline")
        except Exception as e:
            logger.error(f"Error loading timeline: {e}")
            self.break_slots = []
    
    def save_timeline(self) -> None:
        """Save timeline to file."""
        try:
            data = {
                "break_slots": [slot.to_dict() for slot in self.break_slots]
            }
            with open(self.timeline_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved {len(self.break_slots)} break slots to timeline")
        except Exception as e:
            logger.error(f"Error saving timeline: {e}")
    
    def validate_timeline(self) -> List[str]:
        """Validate the timeline and return any issues.
        
        Returns:
            List of validation error messages
        """
        errors = []
        
        # Check for overlapping slots
        for i, slot1 in enumerate(self.break_slots):
            if self._has_overlap(slot1, exclude_id=slot1.id):
                errors.append(f"Break slot at {slot1.start_time.strftime('%H:%M')} overlaps with another slot")
        
        # Check for invalid durations
        for slot in self.break_slots:
            try:
                duration = int(slot.duration)
                if duration <= 0:
                    errors.append(f"Break slot at {slot.start_time.strftime('%H:%M')} has invalid duration: {slot.duration}")
                elif duration > 120:
                    errors.append(f"Break slot at {slot.start_time.strftime('%H:%M')} has duration too long: {slot.duration} minutes")
            except (ValueError, TypeError):
                errors.append(f"Break slot at {slot.start_time.strftime('%H:%M')} has invalid duration type: {slot.duration}")
        
        # Check for invalid repeat patterns
        valid_patterns = ["daily", "weekdays", "weekends", "once"]
        for slot in self.break_slots:
            if slot.repeat_pattern not in valid_patterns:
                errors.append(f"Break slot at {slot.start_time.strftime('%H:%M')} has invalid repeat pattern: {slot.repeat_pattern}")
        
        return errors 