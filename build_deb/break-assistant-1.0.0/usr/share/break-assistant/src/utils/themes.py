import customtkinter as ctk

class ThemeManager:
    """Handles theme switching and management."""
    def __init__(self) -> None:
        pass

    def apply_theme(self, theme_name: str) -> None:
        # Accepts "Light", "Dark", or "System"
        if theme_name.lower() == "light":
            ctk.set_appearance_mode("Light")
        elif theme_name.lower() == "dark":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("System") 