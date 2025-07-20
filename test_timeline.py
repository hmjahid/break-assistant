#!/usr/bin/env python3
"""Test script to verify timeline functionality."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from datetime import datetime, timedelta
from src.models.timeline_manager import TimelineManager

def test_timeline():
    """Test timeline functionality."""
    print("Testing Timeline Manager...")
    
    # Create timeline manager
    timeline_manager = TimelineManager()
    
    # Get current time
    now = datetime.now()
    print(f"Current time: {now}")
    
    # Get all break slots
    all_slots = timeline_manager.get_all_break_slots()
    print(f"Total break slots: {len(all_slots)}")
    
    for slot in all_slots:
        print(f"  - {slot.start_time.strftime('%H:%M')} ({slot.duration}min) - {slot.message}")
    
    # Get active break slots for today
    active_slots = timeline_manager.get_active_break_slots(now)
    print(f"Active break slots today: {len(active_slots)}")
    
    for slot in active_slots:
        print(f"  - {slot.start_time.strftime('%H:%M')} ({slot.duration}min) - {slot.message}")
    
    # Get next break
    next_break = timeline_manager.get_next_break(now)
    if next_break:
        break_slot, occurrence_time = next_break
        print(f"Next break: {occurrence_time.strftime('%Y-%m-%d %H:%M')} ({break_slot.duration}min) - {break_slot.message}")
        
        # Check if it's today or tomorrow
        if occurrence_time.date() == now.date():
            print("  -> This break is scheduled for today")
        elif occurrence_time.date() == now.date() + timedelta(days=1):
            print("  -> This break is scheduled for tomorrow")
        else:
            print(f"  -> This break is scheduled for {occurrence_time.date()}")
    else:
        print("No upcoming breaks found")
    
    # Test individual slot next occurrences
    print("\nTesting individual slot next occurrences:")
    for slot in active_slots:
        occurrence = slot.get_next_occurrence(now)
        if occurrence:
            print(f"  - {slot.start_time.strftime('%H:%M')}: Next occurrence today at {occurrence.strftime('%H:%M')}")
        else:
            # Check tomorrow
            occurrence = slot.get_next_occurrence_tomorrow(now)
            if occurrence:
                print(f"  - {slot.start_time.strftime('%H:%M')}: Next occurrence tomorrow at {occurrence.strftime('%H:%M')}")
            else:
                print(f"  - {slot.start_time.strftime('%H:%M')}: No upcoming occurrences")

if __name__ == "__main__":
    test_timeline() 