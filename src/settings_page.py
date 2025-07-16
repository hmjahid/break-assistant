import customtkinter as ctk
from typing import Optional

class SettingsPage(ctk.CTkFrame):
    """Settings interface view."""
    
    def __init__(self, master, controller) -> None:
        print("DEBUG: Entering SettingsPage.__init__")
        super().__init__(master)
        self.controller = controller
        try:
            print("DEBUG: Calling setup_ui")
            self.setup_ui()
        except Exception as e:
            print(f"Error in setup_ui: {e}")
            raise
        try:
            print("DEBUG: Calling load_settings")
            self.load_settings()
        except Exception as e:
            print(f"Error in load_settings: {e}")
            raise
        try:
            print("DEBUG: Binding mouse wheel")
            self.bind_all_mousewheel()
        except Exception as e:
            print(f"Error in bind_all_mousewheel: {e}")
            raise
    
    def setup_ui(self) -> None:
        print("DEBUG: Entering setup_ui")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.scrollable = ctk.CTkScrollableFrame(self)
        self.scrollable.grid(row=0, column=0, sticky="nsew")
        self.scrollable.grid_columnconfigure(0, weight=1)
        self.scrollable.bind_all("<MouseWheel>", self._on_mousewheel)
        # Info section
        try:
            info_label = ctk.CTkLabel(self.scrollable, text="Configure your notifications and appearance settings.\nSettings are saved automatically.", font=ctk.CTkFont(size=13), justify="center", wraplength=500, text_color="gray")
            info_label.grid(row=0, column=0, pady=(10, 5), sticky="ew")
        except Exception as e:
            print(f"Error in info_label: {e}")
            raise
        # Title
        try:
            title_label = ctk.CTkLabel(self.scrollable, text="Settings", font=ctk.CTkFont(size=20, weight="bold"))
            title_label.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        except Exception as e:
            print(f"Error in title_label: {e}")
            raise
        # Notification Settings Section
        try:
            self.create_notification_settings(self.scrollable, 2)
        except Exception as e:
            print(f"Error in create_notification_settings: {e}")
            raise
        # Appearance Settings Section
        try:
            self.create_appearance_settings(self.scrollable, 3)
        except Exception as e:
            print(f"Error in create_appearance_settings: {e}")
            raise
        # Buttons
        try:
            self.create_buttons(self.scrollable, 4)
        except Exception as e:
            print(f"Error in create_buttons: {e}")
            raise
    
    def _on_mousewheel(self, event):
        try:
            self.scrollable._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except Exception:
            pass
    
    def bind_all_mousewheel(self):
        """Bind mouse wheel events for scrolling."""
        # Windows/Mac
        self.scrollable.bind_all("<MouseWheel>", self._on_mousewheel)
        # Linux
        self.scrollable.bind_all("<Button-4>", self._on_mousewheel_linux)
        self.scrollable.bind_all("<Button-5>", self._on_mousewheel_linux)
    
    def _on_mousewheel_linux(self, event):
        try:
            if event.num == 4:
                self.scrollable._parent_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.scrollable._parent_canvas.yview_scroll(1, "units")
        except Exception:
            pass
    

    
    def create_notification_settings(self, parent, row):
        print("DEBUG: Entering create_notification_settings")
        notif_frame = ctk.CTkFrame(parent)
        notif_frame.grid(row=row, column=0, sticky="ew", pady=(0, 20), padx=10)
        notif_frame.grid_columnconfigure(1, weight=1)
        notif_title = ctk.CTkLabel(notif_frame, text="Notification Settings", font=ctk.CTkFont(size=16, weight="bold"))
        notif_title.grid(row=0, column=0, columnspan=2, pady=(10, 15), sticky="ew")
        self.sound_enabled_var = ctk.BooleanVar(value=True)
        sound_check = ctk.CTkCheckBox(notif_frame, text="Enable sound notifications", variable=self.sound_enabled_var)
        sound_check.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="w")
        self.system_notif_var = ctk.BooleanVar(value=True)
        system_check = ctk.CTkCheckBox(notif_frame, text="Show system notifications", variable=self.system_notif_var)
        system_check.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="w")
        volume_label = ctk.CTkLabel(notif_frame, text="Notification Volume:", wraplength=300)
        volume_label.grid(row=3, column=0, padx=(15, 10), pady=5, sticky="w")
        self.volume_var = ctk.IntVar(value=50)
        volume_slider = ctk.CTkSlider(notif_frame, from_=0, to=100, variable=self.volume_var, width=200)
        volume_slider.grid(row=3, column=1, padx=(0, 15), pady=5, sticky="w")
        volume_display = ctk.CTkLabel(notif_frame, textvariable=self.volume_var)
        volume_display.grid(row=3, column=2, padx=(5, 15), pady=5)
    
    def create_appearance_settings(self, parent, row):
        print("DEBUG: Entering create_appearance_settings")
        appearance_frame = ctk.CTkFrame(parent)
        appearance_frame.grid(row=row, column=0, sticky="ew", pady=(0, 20), padx=10)
        appearance_frame.grid_columnconfigure(1, weight=1)
        appearance_title = ctk.CTkLabel(appearance_frame, text="Appearance Settings", font=ctk.CTkFont(size=16, weight="bold"))
        appearance_title.grid(row=0, column=0, columnspan=2, pady=(10, 15), sticky="ew")
        theme_label = ctk.CTkLabel(appearance_frame, text="Theme:", wraplength=300)
        theme_label.grid(row=1, column=0, padx=(15, 10), pady=5, sticky="w")
        self.theme_var = ctk.StringVar(value="System")
        theme_menu = ctk.CTkOptionMenu(appearance_frame, values=["Light", "Dark", "System"], variable=self.theme_var, width=150)
        theme_menu.grid(row=1, column=1, padx=(0, 15), pady=5, sticky="w")
        self.transparency_var = ctk.BooleanVar(value=False)
        transparency_check = ctk.CTkCheckBox(appearance_frame, text="Enable window transparency", variable=self.transparency_var)
        transparency_check.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="w")
        self.always_on_top_var = ctk.BooleanVar(value=False)
        on_top_check = ctk.CTkCheckBox(appearance_frame, text="Always on top", variable=self.always_on_top_var)
        on_top_check.grid(row=3, column=0, columnspan=2, padx=15, pady=5, sticky="w")
    
    def create_buttons(self, parent, row):
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.grid(row=row, column=0, sticky="ew", pady=(0, 20), padx=10)
        save_button = ctk.CTkButton(buttons_frame, text="Save Settings", command=self.save_settings)
        save_button.pack(side="left", padx=(10, 5), pady=10)
        reset_button = ctk.CTkButton(buttons_frame, text="Reset to Defaults", command=self.reset_settings)
        reset_button.pack(side="left", padx=5, pady=10)
        cancel_button = ctk.CTkButton(buttons_frame, text="Cancel", command=self.cancel_settings)
        cancel_button.pack(side="right", padx=(5, 10), pady=10)
    
    def load_settings(self) -> None:
        try:
            settings = self.controller.get_settings()
            print("DEBUG: settings loaded:", settings)
            
            # Always set default values, then override with saved settings if they exist
            print("DEBUG: Setting default values first...")
            
            # Set default values
            self.volume_var.set(50)
            self.sound_enabled_var.set(True)
            self.system_notif_var.set(True)
            self.theme_var.set('System')
            self.transparency_var.set(False)
            self.always_on_top_var.set(False)
            
            if settings:
                print("DEBUG: volume type:", type(settings.get('volume')))
                print("DEBUG: sound_enabled type:", type(settings.get('sound_enabled')))
                print("DEBUG: system_notifications type:", type(settings.get('system_notifications')))
                print("DEBUG: theme type:", type(settings.get('theme')))
                print("DEBUG: transparency type:", type(settings.get('transparency')))
                print("DEBUG: always_on_top type:", type(settings.get('always_on_top')))
                
                # Safely convert numeric values with proper error handling
                try:
                    volume = settings.get('volume')
                    if volume is not None and volume != "":
                        if isinstance(volume, str):
                            volume = int(volume)
                        self.volume_var.set(volume)
                        print(f"DEBUG: Set volume to {volume}")
                    else:
                        print("DEBUG: Using default volume (50)")
                        self.volume_var.set(50)
                except (ValueError, TypeError):
                    print("DEBUG: Using default volume (50)")
                    self.volume_var.set(50)
                
                # Boolean values - only set if they exist in settings
                if 'sound_enabled' in settings:
                    sound_enabled = settings.get('sound_enabled')
                    if sound_enabled is not None:
                        self.sound_enabled_var.set(bool(sound_enabled))
                        print(f"DEBUG: Set sound_enabled to {sound_enabled}")
                    else:
                        print("DEBUG: Using default sound_enabled (True)")
                        self.sound_enabled_var.set(True)
                
                if 'system_notifications' in settings:
                    system_notifications = settings.get('system_notifications')
                    if system_notifications is not None:
                        self.system_notif_var.set(bool(system_notifications))
                        print(f"DEBUG: Set system_notifications to {system_notifications}")
                    else:
                        print("DEBUG: Using default system_notifications (True)")
                        self.system_notif_var.set(True)
                
                if 'theme' in settings:
                    theme = settings.get('theme')
                    if theme is not None and theme != "":
                        self.theme_var.set(theme)
                        print(f"DEBUG: Set theme to {theme}")
                    else:
                        print("DEBUG: Using default theme (System)")
                        self.theme_var.set('System')
                
                if 'transparency' in settings:
                    transparency = settings.get('transparency')
                    if transparency is not None:
                        self.transparency_var.set(bool(transparency))
                        print(f"DEBUG: Set transparency to {transparency}")
                    else:
                        print("DEBUG: Using default transparency (False)")
                        self.transparency_var.set(False)
                
                if 'always_on_top' in settings:
                    always_on_top = settings.get('always_on_top')
                    if always_on_top is not None:
                        self.always_on_top_var.set(bool(always_on_top))
                        print(f"DEBUG: Set always_on_top to {always_on_top}")
                    else:
                        print("DEBUG: Using default always_on_top (False)")
                        self.always_on_top_var.set(False)
            else:
                print("DEBUG: No settings found, using defaults")
        except Exception as e:
            print(f"Error loading settings: {e}")
            # Set default values if loading fails
            self.volume_var.set(50)
            self.sound_enabled_var.set(True)
            self.system_notif_var.set(True)
            self.theme_var.set('System')
            self.transparency_var.set(False)
            self.always_on_top_var.set(False)
    
    def save_settings(self) -> None:
        try:
            # Get volume value safely
            volume_value = self.volume_var.get()
            if volume_value is None or volume_value == "" or volume_value == 0:
                volume_value = 50
            else:
                try:
                    volume_value = int(volume_value)
                    if volume_value < 0:
                        volume_value = 0
                    elif volume_value > 100:
                        volume_value = 100
                except (ValueError, TypeError):
                    volume_value = 50
            
            settings = {
                'sound_enabled': bool(self.sound_enabled_var.get()),
                'system_notifications': bool(self.system_notif_var.get()),
                'volume': volume_value,
                'theme': self.theme_var.get(),
                'transparency': bool(self.transparency_var.get()),
                'always_on_top': bool(self.always_on_top_var.get())
            }
            print(f"DEBUG: Saving settings: {settings}")
            self.controller.save_settings(settings)
            print("✓ Settings saved successfully")
            
            # Apply settings immediately to main window
            self.apply_settings_to_main_window(settings)
            
            # Show success message
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Success", "Settings saved successfully!")
            
            # Close the window
            print("DEBUG: Closing settings window...")
            self.master.destroy()
            print("DEBUG: Settings window closed")
            
        except ValueError as e:
            print(f"DEBUG: ValueError in save_settings: {e}")
            self.show_error("Invalid Settings", f"Please check your input values: {e}")
        except Exception as e:
            print(f"DEBUG: Exception in save_settings: {e}")
            self.show_error("Error", f"Failed to save settings: {e}")
    
    def apply_settings_to_main_window(self, settings: dict) -> None:
        """Apply settings immediately to the main window."""
        try:
            if hasattr(self.controller, 'main_window') and self.controller.main_window:
                main_window = self.controller.main_window
                
                # Apply theme
                theme = settings.get('theme', 'System')
                if hasattr(self.controller, 'theme_manager'):
                    self.controller.theme_manager.apply_theme(theme)
                    print(f"DEBUG: Applied theme: {theme}")
                
                # Apply transparency setting
                transparency_enabled = settings.get('transparency', False)
                if hasattr(main_window, 'attributes'):
                    try:
                        if transparency_enabled:
                            main_window.attributes('-alpha', 0.9)
                            print(f"DEBUG: Applied transparency: {transparency_enabled}")
                        else:
                            main_window.attributes('-alpha', 1.0)
                            print(f"DEBUG: Removed transparency")
                    except Exception as e:
                        print(f"DEBUG: Could not apply transparency: {e}")
                
                # Apply always on top setting
                always_on_top = settings.get('always_on_top', False)
                if hasattr(main_window, 'attributes'):
                    try:
                        main_window.attributes('-topmost', always_on_top)
                        print(f"DEBUG: Applied always on top: {always_on_top}")
                    except Exception as e:
                        print(f"DEBUG: Could not apply always on top: {e}")
                
                # Force update the main window
                main_window.update()
                print("DEBUG: Main window refreshed with new settings")
                
        except Exception as e:
            print(f"DEBUG: Error applying settings to main window: {e}")
    
    def refresh_main_window(self) -> None:
        """Refresh the main window to apply new settings."""
        try:
            if hasattr(self.controller, 'main_window') and self.controller.main_window:
                # Get current settings
                current_settings = self.controller.get_settings()
                
                # Apply theme immediately
                current_theme = current_settings.get('theme', 'System')
                if hasattr(self.controller, 'theme_manager'):
                    self.controller.theme_manager.apply_theme(current_theme)
                    print(f"DEBUG: Applied theme: {current_theme}")
                
                # Apply transparency setting
                transparency_enabled = current_settings.get('transparency', False)
                if hasattr(self.controller.main_window, 'attributes'):
                    try:
                        if transparency_enabled:
                            self.controller.main_window.attributes('-alpha', 0.9)
                        else:
                            self.controller.main_window.attributes('-alpha', 1.0)
                        print(f"DEBUG: Applied transparency: {transparency_enabled}")
                    except Exception as e:
                        print(f"DEBUG: Could not apply transparency: {e}")
                
                # Apply always on top setting
                always_on_top = current_settings.get('always_on_top', False)
                if hasattr(self.controller.main_window, 'attributes'):
                    try:
                        self.controller.main_window.attributes('-topmost', always_on_top)
                        print(f"DEBUG: Applied always on top: {always_on_top}")
                    except Exception as e:
                        print(f"DEBUG: Could not apply always on top: {e}")
                
                # Force update the main window
                self.controller.main_window.update()
                print("DEBUG: Main window refreshed with new settings")
                
        except Exception as e:
            print(f"DEBUG: Error refreshing main window: {e}")
    
    def reset_settings(self) -> None:
        self.sound_enabled_var.set(True)
        self.system_notif_var.set(True)
        self.volume_var.set(50)
        self.theme_var.set("System")
        self.transparency_var.set(False)
        self.always_on_top_var.set(False)
    
    def cancel_settings(self) -> None:
        self.master.destroy()
    
    def show_error(self, title: str, message: str) -> None:
        import tkinter.messagebox as messagebox
        messagebox.showerror(title, message) 