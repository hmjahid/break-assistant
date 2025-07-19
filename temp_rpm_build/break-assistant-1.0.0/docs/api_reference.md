# Break Assistant API Reference

## Table of Contents

1. [Models](#models)
2. [Views](#views)
3. [Controllers](#controllers)
4. [Utils](#utils)
5. [Constants](#constants)
6. [Exceptions](#exceptions)

## Models

### SettingsManager

Manages application settings and configuration persistence.

```python
class SettingsManager:
    """Handles loading, saving, and managing user settings."""
    
    def __init__(self) -> None:
        """Initialize settings manager."""
        self.settings: Dict[str, Any] = {}
    
    def load(self) -> None:
        """Load settings from configuration file."""
        
    def save(self) -> None:
        """Save settings to configuration file."""
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value by key.
        
        Args:
            key: Setting key
            default: Default value if key not found
            
        Returns:
            Setting value or default
        """
        
    def set(self, key: str, value: Any) -> None:
        """Set setting value by key.
        
        Args:
            key: Setting key
            value: Setting value
        """
        
    def reset_to_defaults(self) -> None:
        """Reset all settings to default values."""
        
    def get_settings_path(self) -> str:
        """Get the path to settings file.
        
        Returns:
            Path to settings file
        """
```

### Timer

Manages timer logic and state for work/break intervals.

```python
class Timer:
    """Timer logic for work/break intervals."""
    
    def __init__(self, duration: int, callback: Optional[Callable[[], None]] = None) -> None:
        """Initialize timer with duration and optional callback.
        
        Args:
            duration: Timer duration in seconds
            callback: Optional callback function to call when timer expires
        """
        self.duration: int = duration
        self.callback: Optional[Callable[[], None]] = callback
        self.remaining: int = duration
        self.running: bool = False
        self.start_time: Optional[float] = None
    
    def start(self) -> None:
        """Start the timer."""
        
    def stop(self) -> None:
        """Stop the timer."""
        
    def pause(self) -> None:
        """Pause the timer."""
        
    def resume(self) -> None:
        """Resume the timer."""
        
    def reset(self) -> None:
        """Reset timer to initial duration."""
        
    def get_remaining(self) -> int:
        """Get remaining time in seconds.
        
        Returns:
            Remaining time in seconds
        """
        
    def get_elapsed(self) -> int:
        """Get elapsed time in seconds.
        
        Returns:
            Elapsed time in seconds
        """
        
    def is_running(self) -> bool:
        """Check if timer is running.
        
        Returns:
            True if timer is running, False otherwise
        """
        
    def is_expired(self) -> bool:
        """Check if timer has expired.
        
        Returns:
            True if timer has expired, False otherwise
        """
```

### BreakManager

Manages break scheduling and logic.

```python
class BreakManager:
    """Manages break scheduling and logic."""
    
    def __init__(self) -> None:
        """Initialize break manager."""
        self.breaks: List[int] = []
        self.current_break: Optional[int] = None
        self.break_type: str = "frequent"
    
    def schedule_next_break(self) -> None:
        """Schedule the next break."""
        
    def start_break(self) -> None:
        """Start the current break."""
        
    def end_break(self) -> None:
        """End the current break."""
        
    def snooze_break(self, duration: int) -> None:
        """Snooze the current break.
        
        Args:
            duration: Snooze duration in minutes
        """
        
    def skip_break(self) -> None:
        """Skip the current break."""
        
    def get_break_type(self) -> str:
        """Get current break type.
        
        Returns:
            Break type ("frequent" or "once")
        """
        
    def set_break_type(self, break_type: str) -> None:
        """Set break type.
        
        Args:
            break_type: Break type ("frequent" or "once")
        """
```

## Views

### MainWindow

Main application window interface.

```python
class MainWindow(ctk.CTk):
    """Main application window."""
    
    def __init__(self, controller) -> None:
        """Initialize main window.
        
        Args:
            controller: Application controller
        """
        super().__init__()
        self.controller = controller
        self.title("Break Assistant")
        self.geometry("400x300")
        self.setup_ui()
    
    def setup_ui(self) -> None:
        """Setup user interface components."""
        
    def update_timer_display(self, remaining: int) -> None:
        """Update timer display.
        
        Args:
            remaining: Remaining time in seconds
        """
        
    def update_progress_bar(self, progress: float) -> None:
        """Update progress bar.
        
        Args:
            progress: Progress value (0.0 to 1.0)
        """
        
    def show_break_notification(self) -> None:
        """Show break notification."""
        
    def show_settings(self) -> None:
        """Show settings dialog."""
        
    def show_about(self) -> None:
        """Show about dialog."""
        
    def minimize_to_tray(self) -> None:
        """Minimize window to system tray."""
        
    def restore_from_tray(self) -> None:
        """Restore window from system tray."""
```

### SettingsPage

Settings configuration interface.

```python
class SettingsPage(ctk.CTkFrame):
    """Settings interface view."""
    
    def __init__(self, master, controller) -> None:
        """Initialize settings page.
        
        Args:
            master: Parent widget
            controller: Application controller
        """
        super().__init__(master)
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self) -> None:
        """Setup settings interface."""
        
    def load_settings(self) -> None:
        """Load current settings into UI."""
        
    def save_settings(self) -> None:
        """Save settings from UI."""
        
    def reset_settings(self) -> None:
        """Reset settings to defaults."""
        
    def test_sound(self) -> None:
        """Test sound notification."""
        
    def browse_sound_file(self) -> None:
        """Browse for sound file."""
        
    def apply_theme(self, theme_name: str) -> None:
        """Apply theme.
        
        Args:
            theme_name: Name of theme to apply
        """
```

### AboutPage

Application information and about page.

```python
class AboutPage(ctk.CTkFrame):
    """About page view."""
    
    def __init__(self, master, controller) -> None:
        """Initialize about page.
        
        Args:
            master: Parent widget
            controller: Application controller
        """
        super().__init__(master)
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self) -> None:
        """Setup about page interface."""
        
    def show_version_info(self) -> str:
        """Get version information.
        
        Returns:
            Version information string
        """
        
    def show_license_info(self) -> str:
        """Get license information.
        
        Returns:
            License information string
        """
        
    def open_website(self) -> None:
        """Open project website."""
        
    def open_github(self) -> None:
        """Open GitHub repository."""
```

### BreakPopup

Break notification popup window.

```python
class BreakPopup(ctk.CTkToplevel):
    """Break notification popup."""
    
    def __init__(self, master, controller) -> None:
        """Initialize break popup.
        
        Args:
            master: Parent widget
            controller: Application controller
        """
        super().__init__(master)
        self.controller = controller
        self.title("Time for a break!")
        self.setup_ui()
    
    def setup_ui(self) -> None:
        """Setup popup interface."""
        
    def take_break(self) -> None:
        """Start break timer."""
        
    def snooze_break(self) -> None:
        """Snooze break."""
        
    def skip_break(self) -> None:
        """Skip break."""
        
    def close_popup(self) -> None:
        """Close popup window."""
```

## Controllers

### AppController

Main application controller coordinating all components.

```python
class AppController:
    """Main application controller."""
    
    def __init__(self) -> None:
        """Initialize application controller."""
        self.main_window = MainWindow(self)
        self.settings_manager = SettingsManager()
        self.timer_controller = TimerController()
        self.break_manager = BreakManager()
        self.audio_manager = AudioManager()
        self.theme_manager = ThemeManager()
    
    def run(self) -> None:
        """Start the application."""
        
    def quit(self) -> None:
        """Quit the application."""
        
    def start_timer(self) -> None:
        """Start work timer."""
        
    def stop_timer(self) -> None:
        """Stop work timer."""
        
    def pause_timer(self) -> None:
        """Pause work timer."""
        
    def reset_timer(self) -> None:
        """Reset work timer."""
        
    def show_break_notification(self) -> None:
        """Show break notification."""
        
    def take_break(self) -> None:
        """Start break."""
        
    def snooze_break(self, duration: int) -> None:
        """Snooze break.
        
        Args:
            duration: Snooze duration in minutes
        """
        
    def skip_break(self) -> None:
        """Skip break."""
        
    def open_settings(self) -> None:
        """Open settings dialog."""
        
    def save_settings(self, settings: Dict[str, Any]) -> None:
        """Save settings.
        
        Args:
            settings: Settings dictionary
        """
        
    def load_settings(self) -> Dict[str, Any]:
        """Load settings.
        
        Returns:
            Settings dictionary
        """
        
    def apply_theme(self, theme_name: str) -> None:
        """Apply theme.
        
        Args:
            theme_name: Name of theme to apply
        """
        
    def play_sound(self, sound_file: str) -> None:
        """Play sound.
        
        Args:
            sound_file: Path to sound file
        """
```

### TimerController

Timer management controller.

```python
class TimerController:
    """Timer management controller."""
    
    def __init__(self) -> None:
        """Initialize timer controller."""
        self.work_timer: Optional[Timer] = None
        self.break_timer: Optional[Timer] = None
        self.snooze_timer: Optional[Timer] = None
    
    def create_work_timer(self, duration: int) -> Timer:
        """Create work timer.
        
        Args:
            duration: Timer duration in minutes
            
        Returns:
            Timer instance
        """
        
    def create_break_timer(self, duration: int) -> Timer:
        """Create break timer.
        
        Args:
            duration: Timer duration in minutes
            
        Returns:
            Timer instance
        """
        
    def create_snooze_timer(self, duration: int) -> Timer:
        """Create snooze timer.
        
        Args:
            duration: Timer duration in minutes
            
        Returns:
            Timer instance
        """
        
    def start_work_timer(self) -> None:
        """Start work timer."""
        
    def start_break_timer(self) -> None:
        """Start break timer."""
        
    def start_snooze_timer(self) -> None:
        """Start snooze timer."""
        
    def stop_all_timers(self) -> None:
        """Stop all active timers."""
        
    def get_work_timer_remaining(self) -> int:
        """Get work timer remaining time.
        
        Returns:
            Remaining time in seconds
        """
        
    def get_break_timer_remaining(self) -> int:
        """Get break timer remaining time.
        
        Returns:
            Remaining time in seconds
        """
        
    def is_work_timer_running(self) -> bool:
        """Check if work timer is running.
        
        Returns:
            True if work timer is running
        """
        
    def is_break_timer_running(self) -> bool:
        """Check if break timer is running.
        
        Returns:
            True if break timer is running
        """
```

## Utils

### AudioManager

Sound playback and audio management.

```python
class AudioManager:
    """Handles sound playback for alerts and notifications."""
    
    def __init__(self) -> None:
        """Initialize audio manager."""
        self.current_sound: Optional[pygame.mixer.Sound] = None
        self.sound_enabled: bool = True
        self.volume: float = 1.0
    
    def play_sound(self, file_path: str) -> None:
        """Play sound from file.
        
        Args:
            file_path: Path to sound file
        """
        
    def stop_sound(self) -> None:
        """Stop currently playing sound."""
        
    def set_volume(self, volume: float) -> None:
        """Set sound volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        
    def get_volume(self) -> float:
        """Get current volume level.
        
        Returns:
            Current volume level
        """
        
    def enable_sound(self) -> None:
        """Enable sound playback."""
        
    def disable_sound(self) -> None:
        """Disable sound playback."""
        
    def is_sound_enabled(self) -> bool:
        """Check if sound is enabled.
        
        Returns:
            True if sound is enabled
        """
        
    def get_available_sounds(self) -> List[str]:
        """Get list of available sound files.
        
        Returns:
            List of sound file paths
        """
        
    def test_sound(self, file_path: str) -> None:
        """Test sound file.
        
        Args:
            file_path: Path to sound file to test
        """
```

### ThemeManager

UI theming and appearance management.

```python
class ThemeManager:
    """Handles theme switching and management."""
    
    def __init__(self) -> None:
        """Initialize theme manager."""
        self.current_theme: str = "system"
        self.themes: Dict[str, Dict[str, str]] = {}
        self.load_themes()
    
    def load_themes(self) -> None:
        """Load available themes."""
        
    def apply_theme(self, theme_name: str) -> None:
        """Apply theme by name.
        
        Args:
            theme_name: Name of theme to apply
        """
        
    def get_current_theme(self) -> str:
        """Get current theme name.
        
        Returns:
            Current theme name
        """
        
    def get_available_themes(self) -> List[str]:
        """Get list of available themes.
        
        Returns:
            List of theme names
        """
        
    def get_theme_colors(self, theme_name: str) -> Dict[str, str]:
        """Get theme colors.
        
        Args:
            theme_name: Name of theme
            
        Returns:
            Dictionary of color values
        """
        
    def detect_system_theme(self) -> str:
        """Detect system theme.
        
        Returns:
            System theme name ("light" or "dark")
        """
        
    def create_custom_theme(self, name: str, colors: Dict[str, str]) -> None:
        """Create custom theme.
        
        Args:
            name: Theme name
            colors: Dictionary of color values
        """
        
    def delete_theme(self, theme_name: str) -> None:
        """Delete theme.
        
        Args:
            theme_name: Name of theme to delete
        """
```

### PlatformUtils

Cross-platform utilities and platform-specific functionality.

```python
class PlatformUtils:
    """Platform-specific utilities."""
    
    @staticmethod
    def get_platform() -> str:
        """Get current platform.
        
        Returns:
            Platform name ("windows", "macos", "linux", or "unknown")
        """
        
    @staticmethod
    def get_settings_path() -> str:
        """Get platform-specific settings path.
        
        Returns:
            Path to settings directory
        """
        
    @staticmethod
    def get_resource_path() -> str:
        """Get platform-specific resource path.
        
        Returns:
            Path to resources directory
        """
        
    @staticmethod
    def create_system_tray() -> Any:
        """Create system tray icon.
        
        Returns:
            System tray icon object
        """
        
    @staticmethod
    def show_notification(title: str, message: str, duration: int = 5) -> None:
        """Show system notification.
        
        Args:
            title: Notification title
            message: Notification message
            duration: Display duration in seconds
        """
        
    @staticmethod
    def set_window_icon(window: Any, icon_path: str) -> None:
        """Set window icon.
        
        Args:
            window: Window object
            icon_path: Path to icon file
        """
        
    @staticmethod
    def minimize_to_tray(window: Any) -> None:
        """Minimize window to system tray.
        
        Args:
            window: Window to minimize
        """
        
    @staticmethod
    def restore_from_tray(window: Any) -> None:
        """Restore window from system tray.
        
        Args:
            window: Window to restore
        """
        
    @staticmethod
    def register_global_hotkeys() -> None:
        """Register global hotkeys."""
        
    @staticmethod
    def unregister_global_hotkeys() -> None:
        """Unregister global hotkeys."""
```

## Constants

### Application Constants

```python
# Application information
APP_NAME = "Break Assistant"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Break Assistant Team"
APP_EMAIL = "team@breakassistant.app"
APP_WEBSITE = "https://breakassistant.app"
APP_GITHUB = "https://github.com/break-assistant/break-assistant"

# Default settings
DEFAULT_BREAK_INTERVAL = 25  # minutes
DEFAULT_BREAK_DURATION = 5   # minutes
DEFAULT_SNOOZE_DURATION = 5  # minutes
DEFAULT_BREAK_TYPE = "frequent"
DEFAULT_SOUND_ENABLED = True
DEFAULT_THEME = "system"
DEFAULT_CUSTOM_MESSAGE = "Time for a break!"

# Timer limits
MIN_BREAK_INTERVAL = 1    # minutes
MAX_BREAK_INTERVAL = 120  # minutes
MIN_BREAK_DURATION = 1    # minutes
MAX_BREAK_DURATION = 60   # minutes
MIN_SNOOZE_DURATION = 1   # minutes
MAX_SNOOZE_DURATION = 30  # minutes

# UI constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
MIN_WINDOW_WIDTH = 300
MIN_WINDOW_HEIGHT = 200

# File paths
SETTINGS_FILENAME = "settings.json"
LOG_FILENAME = "break_assistant.log"
```

### Theme Colors

```python
# Light theme colors
LIGHT_THEME = {
    "bg_color": "#ffffff",
    "fg_color": "#000000",
    "accent_color": "#007acc",
    "button_color": "#e1e1e1",
    "button_hover_color": "#d1d1d1",
    "text_color": "#333333",
    "border_color": "#cccccc"
}

# Dark theme colors
DARK_THEME = {
    "bg_color": "#2b2b2b",
    "fg_color": "#ffffff",
    "accent_color": "#007acc",
    "button_color": "#404040",
    "button_hover_color": "#505050",
    "text_color": "#ffffff",
    "border_color": "#555555"
}
```

## Exceptions

### Custom Exceptions

```python
class BreakAssistantError(Exception):
    """Base exception for Break Assistant."""
    pass


class SettingsError(BreakAssistantError):
    """Exception raised for settings-related errors."""
    pass


class TimerError(BreakAssistantError):
    """Exception raised for timer-related errors."""
    pass


class AudioError(BreakAssistantError):
    """Exception raised for audio-related errors."""
    pass


class ThemeError(BreakAssistantError):
    """Exception raised for theme-related errors."""
    pass


class PlatformError(BreakAssistantError):
    """Exception raised for platform-specific errors."""
    pass


class ValidationError(BreakAssistantError):
    """Exception raised for validation errors."""
    pass
```

### Error Codes

```python
# Error codes
ERROR_INVALID_SETTINGS = 1001
ERROR_TIMER_FAILURE = 1002
ERROR_AUDIO_FAILURE = 1003
ERROR_THEME_FAILURE = 1004
ERROR_PLATFORM_FAILURE = 1005
ERROR_VALIDATION_FAILURE = 1006
ERROR_FILE_NOT_FOUND = 1007
ERROR_PERMISSION_DENIED = 1008
ERROR_NETWORK_FAILURE = 1009
ERROR_UNKNOWN = 9999
```

---

*Last updated: Version 1.0.0* 