from src.views.main_window import MainWindow
from src.models.timeline_manager import TimelineManager
from src.models.settings import SettingsManager
from src.utils.audio import AudioManager
from src.utils.themes import ThemeManager
from src.utils.platform import PlatformUtils
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class AppController:
    """Main application controller."""
    
    def __init__(self, timeline_file=None, settings_file=None) -> None:
        """Initialize application controller."""
        # Initialize managers
        self.settings_manager = SettingsManager(settings_file=settings_file)
        self.timeline_manager = TimelineManager(timeline_file=timeline_file)
        self.audio_manager = AudioManager(self.settings_manager)
        self.theme_manager = ThemeManager()
        self.platform_utils = PlatformUtils()
        
        # Load settings
        self.settings_manager.load()
        
        # Initialize UI
        self.main_window = MainWindow(self)
        # Apply always on top setting immediately after creating main window
        always_on_top = self.settings_manager.get('always_on_top', False)
        if hasattr(self.main_window, 'attributes'):
            try:
                self.main_window.attributes('-topmost', always_on_top)
            except Exception as e:
                print(f"DEBUG: Could not apply always on top at startup: {e}")
        # Store reference to main window for settings refresh
        self.main_window_ref = self.main_window
        
        # Apply theme
        theme = self.settings_manager.get("theme", "system")
        self.theme_manager.apply_theme(theme)
        
        logger.info("Application controller initialized")
    
    def run(self) -> None:
        """Start the application."""
        logger.info("Starting Break Assistant application")
        self.main_window.mainloop()
    
    def quit(self) -> None:
        """Quit the application."""
        logger.info("Quitting Break Assistant application")
        self.settings_manager.save()
        self.main_window.quit()
    
    def get_timeline_manager(self) -> TimelineManager:
        """Get the timeline manager.
        
        Returns:
            Timeline manager instance
        """
        return self.timeline_manager
    
    def get_settings_manager(self) -> SettingsManager:
        """Get the settings manager.
        
        Returns:
            Settings manager instance
        """
        return self.settings_manager
    
    def get_audio_manager(self) -> AudioManager:
        """Get the audio manager.
        
        Returns:
            Audio manager instance
        """
        return self.audio_manager
    
    def get_theme_manager(self) -> ThemeManager:
        """Get the theme manager.
        
        Returns:
            Theme manager instance
        """
        return self.theme_manager
    
    def get_platform_utils(self) -> PlatformUtils:
        """Get the platform utilities.
        
        Returns:
            Platform utilities instance
        """
        return self.platform_utils
    
    def get_next_break(self) -> tuple:
        """Get the next break from timeline."""
        current_datetime = datetime.now()
        
        next_break = self.timeline_manager.get_next_break(current_datetime)
        
        return next_break
    
    def play_notification_sound(self) -> None:
        """Play notification sound."""
        sound_enabled = self.settings_manager.get("sound_enabled", True)
        if sound_enabled:
            sound_file = self.settings_manager.get("sound_file", "alert.wav")
            self.audio_manager.play_sound(sound_file)
    
    def show_break_notification(self, break_slot, occurrence_time) -> None:
        """Show break notification.
        
        Args:
            break_slot: Break slot that triggered
            occurrence_time: When the break should occur
        """
        from src.views.break_popup import BreakPopup
        
        # Play sound
        self.play_notification_sound()
        
        # Show popup
        popup = BreakPopup(self.main_window, self)
        popup.set_break_info(break_slot, occurrence_time)
        # Popup is already visible from __init__
    
    def apply_theme(self, theme_name: str) -> None:
        """Apply theme.
        
        Args:
            theme_name: Name of theme to apply
        """
        self.theme_manager.apply_theme(theme_name)
        self.settings_manager.set("theme", theme_name)
        self.settings_manager.save()
    
    def apply_transparency(self, enabled: bool) -> None:
        """Apply transparency setting.
        
        Args:
            enabled: Whether transparency is enabled
        """
        self.settings_manager.set("transparency", enabled)
        self.settings_manager.save()
        # Note: Actual transparency implementation would go here
    
    def apply_always_on_top(self, enabled: bool) -> None:
        """Apply always on top setting.
        
        Args:
            enabled: Whether window should always be on top
        """
        self.settings_manager.set("always_on_top", enabled)
        self.settings_manager.save()
        # Note: Actual always on top implementation would go here
    
    def get_settings(self) -> dict:
        """Get current settings.
        
        Returns:
            Settings dictionary
        """
        return self.settings_manager.settings.copy()
    
    def save_settings(self, settings: dict) -> None:
        """Save settings.
        
        Args:
            settings: Settings dictionary
        """
        for key, value in settings.items():
            self.settings_manager.set(key, value)
        self.settings_manager.save()
    
    def load_settings(self) -> dict:
        """Load settings.
        
        Returns:
            Settings dictionary
        """
        return self.settings_manager.settings.copy()
    
    def get_platform(self) -> str:
        """Get current platform.
        
        Returns:
            Platform name
        """
        return self.platform_utils.get_platform()
    
    def start_break_timer(self, duration_seconds: int) -> None:
        """Start a break timer.
        
        Args:
            duration_seconds: Break duration in seconds
        """
        # Update main window timer for break
        if hasattr(self.main_window, 'timer_duration'):
            self.main_window.timer_duration = duration_seconds
            self.main_window.timer_remaining = duration_seconds
            self.main_window.timer_running = False
            self.main_window.start_button.configure(text="Start")
            self.main_window.status_label.configure(text="Break time!")
            self.main_window.update_timer_display()
            
            # Start the break timer
            self.main_window.start_timer() 