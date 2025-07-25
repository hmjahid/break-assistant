import json
import os
from typing import Any, Dict

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "break-assistant")
os.makedirs(CONFIG_DIR, exist_ok=True)

class SettingsManager:
    """Handles loading, saving, and managing user settings."""
    
    def __init__(self, settings_file=None) -> None:
        self.settings: Dict[str, Any] = {}
        if settings_file:
            self.settings_file = settings_file
        else:
            self.settings_file = os.path.join(CONFIG_DIR, "settings.json")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value.
        
        Args:
            key: Setting key
            default: Default value if key not found
            
        Returns:
            Setting value or default
        """
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a setting value.
        
        Args:
            key: Setting key
            value: Setting value
        """
        self.settings[key] = value
    
    def load(self) -> None:
        """Load settings from file and normalize numeric values to int."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
                # Normalize numeric settings to int if possible
                for key in ["work_duration", "break_duration", "volume"]:
                    if key in self.settings:
                        try:
                            self.settings[key] = int(self.settings[key])
                        except (ValueError, TypeError):
                            # If conversion fails, set to a safe default
                            if key == "work_duration":
                                self.settings[key] = 25
                            elif key == "break_duration":
                                self.settings[key] = 5
                            elif key == "volume":
                                self.settings[key] = 50
        except Exception:
            self.settings = {}
    
    def save(self) -> None:
        """Save settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception:
            pass 