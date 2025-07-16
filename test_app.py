#!/usr/bin/env python3
"""
Simple test script for Break Assistant
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all modules can be imported."""
    print("Testing imports...")
    
    try:
        from models.timeline_manager import TimelineManager, BreakSlot
        print("✓ TimelineManager imported successfully")
    except Exception as e:
        print(f"✗ TimelineManager import failed: {e}")
        return False
    
    try:
        from models.settings import SettingsManager
        print("✓ SettingsManager imported successfully")
    except Exception as e:
        print(f"✗ SettingsManager import failed: {e}")
        return False
    
    try:
        from models.timer import Timer
        print("✓ Timer imported successfully")
    except Exception as e:
        print(f"✗ Timer import failed: {e}")
        return False
    
    try:
        from utils.audio import AudioManager
        print("✓ AudioManager imported successfully")
    except Exception as e:
        print(f"✗ AudioManager import failed: {e}")
        return False
    
    try:
        from utils.themes import ThemeManager
        print("✓ ThemeManager imported successfully")
    except Exception as e:
        print(f"✗ ThemeManager import failed: {e}")
        return False
    
    try:
        from utils.platform import PlatformUtils
        print("✓ PlatformUtils imported successfully")
    except Exception as e:
        print(f"✗ PlatformUtils import failed: {e}")
        return False
    
    return True

def test_timeline_manager():
    """Test timeline manager functionality."""
    print("\nTesting TimelineManager...")
    
    try:
        from models.timeline_manager import TimelineManager, BreakSlot
        from datetime import time
        
        # Create timeline manager
        timeline = TimelineManager("test_timeline.json")
        
        # Test adding break slot
        slot = timeline.add_break_slot(time(10, 30), 15, "Test break", "daily")
        print(f"✓ Added break slot: {slot.start_time} ({slot.duration}min)")
        
        # Test getting all slots
        slots = timeline.get_all_break_slots()
        print(f"✓ Retrieved {len(slots)} break slots")
        
        # Test validation
        errors = timeline.validate_timeline()
        print(f"✓ Timeline validation: {len(errors)} errors")
        
        # Clean up
        if os.path.exists("test_timeline.json"):
            os.remove("test_timeline.json")
        
        return True
    except Exception as e:
        print(f"✗ TimelineManager test failed: {e}")
        return False

def test_settings_manager():
    """Test settings manager functionality."""
    print("\nTesting SettingsManager...")
    
    try:
        from models.settings import SettingsManager
        
        # Create settings manager
        settings = SettingsManager()
        settings.settings_file = "test_settings.json"
        
        # Test setting and getting values
        settings.set("test_key", "test_value")
        value = settings.get("test_key", "default")
        print(f"✓ Settings test: {value}")
        
        # Test saving and loading
        settings.save()
        settings.load()
        value = settings.get("test_key")
        print(f"✓ Settings persistence: {value}")
        
        # Clean up
        if os.path.exists("test_settings.json"):
            os.remove("test_settings.json")
        
        return True
    except Exception as e:
        print(f"✗ SettingsManager test failed: {e}")
        return False

def test_timer():
    """Test timer functionality."""
    print("\nTesting Timer...")
    
    try:
        from models.timer import Timer
        
        # Create timer
        timer = Timer(60)
        print(f"✓ Timer created: {timer.duration}s")
        
        # Test timer state
        print(f"✓ Timer running: {timer.running}")
        print(f"✓ Timer remaining: {timer.remaining}s")
        
        return True
    except Exception as e:
        print(f"✗ Timer test failed: {e}")
        return False

def test_audio_manager():
    """Test audio manager functionality."""
    print("\nTesting AudioManager...")
    
    try:
        from utils.audio import AudioManager
        
        # Create audio manager
        audio = AudioManager()
        print("✓ AudioManager created")
        
        # Test sound file check (won't actually play)
        print("✓ AudioManager test completed")
        
        return True
    except Exception as e:
        print(f"✗ AudioManager test failed: {e}")
        return False

def test_platform_utils():
    """Test platform utilities."""
    print("\nTesting PlatformUtils...")
    
    try:
        from utils.platform import PlatformUtils
        
        # Create platform utils
        platform = PlatformUtils()
        
        # Test platform detection
        detected_platform = platform.get_platform()
        print(f"✓ Platform detected: {detected_platform}")
        
        return True
    except Exception as e:
        print(f"✗ PlatformUtils test failed: {e}")
        return False

def test_theme_manager():
    """Test theme manager functionality."""
    print("\nTesting ThemeManager...")
    
    try:
        from utils.themes import ThemeManager
        
        # Create theme manager
        theme = ThemeManager()
        print("✓ ThemeManager created")
        
        # Test theme application
        theme.apply_theme("light")
        print("✓ Light theme applied")
        
        theme.apply_theme("dark")
        print("✓ Dark theme applied")
        
        return True
    except Exception as e:
        print(f"✗ ThemeManager test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Break Assistant Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_timeline_manager,
        test_settings_manager,
        test_timer,
        test_audio_manager,
        test_platform_utils,
        test_theme_manager
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Application is ready for use.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 