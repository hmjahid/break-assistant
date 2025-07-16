#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.models.settings import SettingsManager
from src.models.timeline_manager import TimelineManager

def test_settings():
    print("Testing SettingsManager...")
    try:
        settings = SettingsManager()
        settings.load()
        print("✓ Settings loaded successfully")
        
        # Test getting settings
        work_duration = settings.get('work_duration', 25)
        print(f"✓ Work duration: {work_duration} (type: {type(work_duration)})")
        
        break_duration = settings.get('break_duration', 5)
        print(f"✓ Break duration: {break_duration} (type: {type(break_duration)})")
        
        volume = settings.get('volume', 50)
        print(f"✓ Volume: {volume} (type: {type(volume)})")
        
    except Exception as e:
        print(f"✗ Settings error: {e}")
        return False
    
    return True

def test_timeline():
    print("\nTesting TimelineManager...")
    try:
        timeline = TimelineManager()
        print("✓ Timeline loaded successfully")
        
        # Test validation
        errors = timeline.validate_timeline()
        print(f"✓ Timeline validation: {len(errors)} errors")
        
        for error in errors:
            print(f"  - {error}")
            
    except Exception as e:
        print(f"✗ Timeline error: {e}")
        return False
    
    return True

def test_settings_page():
    print("\nTesting SettingsPage...")
    try:
        from src.settings_page import SettingsPage
        import customtkinter as ctk
        
        root = ctk.CTk()
        root.withdraw()  # Hide the window
        
        # Mock controller
        class MockController:
            def get_settings(self):
                return {
                    'work_duration': 25,
                    'break_duration': 5,
                    'volume': 50,
                    'theme': 'System'
                }
        
        controller = MockController()
        settings_page = SettingsPage(root, controller)
        print("✓ SettingsPage created successfully")
        
        root.destroy()
        
    except Exception as e:
        print(f"✗ SettingsPage error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Debugging Break Assistant Settings...")
    
    success = True
    success &= test_settings()
    success &= test_timeline()
    success &= test_settings_page()
    
    if success:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed!") 