import pygame
import os
import sys

class AudioManager:
    """Handles sound playback for alerts and notifications."""
    def __init__(self, settings_manager=None) -> None:
        self.settings_manager = settings_manager
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Failed to initialize pygame mixer: {e}")

    def get_resource_path(self, relative_path: str) -> str:
        # Handle PyInstaller/AppImage resource extraction
        if hasattr(sys, '_MEIPASS'):
            # Try multiple possible locations for audio files
            possible_paths = [
                os.path.join(sys._MEIPASS, 'audio'),
                os.path.join(sys._MEIPASS, 'resources', 'audio'),
                os.path.join(sys._MEIPASS, 'src', 'audio')
            ]
            
            for base_path in possible_paths:
                resolved = os.path.abspath(os.path.join(base_path, relative_path))
                print(f"[AUDIO DEBUG] Trying path: {resolved}")
                if os.path.exists(resolved):
                    print(f"[AUDIO DEBUG] Found file at: {resolved}")
                    return resolved
            
            # If not found in any location, return the first one for debugging
            resolved = os.path.abspath(os.path.join(possible_paths[0], relative_path))
            print(f"[AUDIO DEBUG] (MEIPASS) Final path: {resolved}")
            return resolved
        else:
            base_path = os.path.dirname(__file__)
            # Try multiple possible locations for audio files in non-bundled environment
            possible_paths = [
                os.path.join(base_path, '../../src/resources/audio'),
                os.path.join(base_path, '../../resources/audio'),
                os.path.join(base_path, '../audio')
            ]
            
            for base_path_option in possible_paths:
                resolved = os.path.abspath(os.path.join(base_path_option, relative_path))
                print(f"[AUDIO DEBUG] Trying path: {resolved}")
                if os.path.exists(resolved):
                    print(f"[AUDIO DEBUG] Found file at: {resolved}")
                    return resolved
            
            # If not found in any location, return the first one for debugging
            resolved = os.path.abspath(os.path.join(possible_paths[0], relative_path))
            print(f"[AUDIO DEBUG] (DEV) Final path: {resolved}")
            return resolved

    def play_sound(self, file_path: str) -> None:
        try:
            # Try to find the file in the resources/audio directory if not absolute
            if not os.path.isabs(file_path):
                file_path = self.get_resource_path(file_path)
            if hasattr(sys, '_MEIPASS'):
                print("[AUDIO DEBUG] Listing files in MEIPASS:")
                for root, dirs, files in os.walk(sys._MEIPASS):
                    for name in files:
                        print(os.path.join(root, name))
            print(f"[AUDIO DEBUG] Final file path: {file_path}")
            print(f"[AUDIO DEBUG] File exists: {os.path.exists(file_path)}")
            if not os.path.exists(file_path):
                print(f"Sound file not found: {file_path}")
                return
            # Set volume from settings if available
            volume = 0.5  # Default volume (50%)
            if self.settings_manager:
                try:
                    v = self.settings_manager.get("volume", 50)
                    volume = max(0, min(1, int(v) / 100))
                except Exception as e:
                    print(f"Failed to get volume from settings: {e}")
            print(f"[AUDIO DEBUG] Setting volume: {volume}")
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play()
            print(f"[AUDIO DEBUG] Sound should be playing now.")
        except Exception as e:
            print(f"Failed to play sound: {e}") 