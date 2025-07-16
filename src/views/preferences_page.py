import customtkinter as ctk
from typing import Optional

class PreferencesPage(ctk.CTkFrame):
    """Preferences interface view - Timer settings only."""
    
    def __init__(self, master, controller) -> None:
        print("DEBUG: Entering PreferencesPage.__init__")
        super().__init__(master)
        self.controller = controller
        try:
            print("DEBUG: Calling setup_ui")
            self.setup_ui()
        except Exception as e:
            print(f"Error in setup_ui: {e}")
            raise
        try:
            print("DEBUG: Calling load_preferences")
            self.load_preferences()
        except Exception as e:
            print(f"Error in load_preferences: {e}")
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
            info_label = ctk.CTkLabel(self.scrollable, text="Configure your work/break intervals and timer preferences.\nSettings are saved automatically.", font=ctk.CTkFont(size=13), justify="center", wraplength=500, text_color="gray")
            info_label.grid(row=0, column=0, pady=(10, 5), sticky="ew")
        except Exception as e:
            print(f"Error in info_label: {e}")
            raise
        
        # Title
        try:
            title_label = ctk.CTkLabel(self.scrollable, text="Preferences", font=ctk.CTkFont(size=20, weight="bold"))
            title_label.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        except Exception as e:
            print(f"Error in title_label: {e}")
            raise
        
        # Timer Settings Section
        try:
            self.create_timer_settings(self.scrollable, 2)
        except Exception as e:
            print(f"Error in create_timer_settings: {e}")
            raise
        
        # Buttons
        try:
            self.create_buttons(self.scrollable, 3)
        except Exception as e:
            print(f"Error in create_buttons: {e}")
            raise
    
    def _on_mousewheel(self, event):
        self.scrollable._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_timer_settings(self, parent, row):
        print("DEBUG: Entering create_timer_settings")
        timer_frame = ctk.CTkFrame(parent)
        timer_frame.grid(row=row, column=0, sticky="ew", pady=(0, 20), padx=10)
        timer_frame.grid_columnconfigure(1, weight=1)
        
        timer_title = ctk.CTkLabel(timer_frame, text="Timer Settings", font=ctk.CTkFont(size=16, weight="bold"))
        timer_title.grid(row=0, column=0, columnspan=2, pady=(10, 15), sticky="ew")
        
        work_label = ctk.CTkLabel(timer_frame, text="Default Work Duration (minutes):", wraplength=300)
        work_label.grid(row=1, column=0, padx=(15, 10), pady=5, sticky="w")
        self.work_duration_var = ctk.StringVar(value="25")
        work_entry = ctk.CTkEntry(timer_frame, textvariable=self.work_duration_var, width=100)
        work_entry.grid(row=1, column=1, padx=(0, 15), pady=5, sticky="w")
        
        break_label = ctk.CTkLabel(timer_frame, text="Default Break Duration (minutes):", wraplength=300)
        break_label.grid(row=2, column=0, padx=(15, 10), pady=5, sticky="w")
        self.break_duration_var = ctk.StringVar(value="5")
        break_entry = ctk.CTkEntry(timer_frame, textvariable=self.break_duration_var, width=100)
        break_entry.grid(row=2, column=1, padx=(0, 15), pady=5, sticky="w")
        
        self.auto_start_var = ctk.BooleanVar(value=False)
        auto_start_check = ctk.CTkCheckBox(timer_frame, text="Auto-start next session", variable=self.auto_start_var)
        auto_start_check.grid(row=3, column=0, columnspan=2, padx=15, pady=5, sticky="w")
    
    def create_buttons(self, parent, row):
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.grid(row=row, column=0, sticky="ew", pady=(0, 20), padx=10)
        
        save_button = ctk.CTkButton(buttons_frame, text="Save Preferences", command=self.save_preferences)
        save_button.pack(side="left", padx=(10, 5), pady=10)
        
        reset_button = ctk.CTkButton(buttons_frame, text="Reset to Defaults", command=self.reset_preferences)
        reset_button.pack(side="left", padx=5, pady=10)
        
        cancel_button = ctk.CTkButton(buttons_frame, text="Cancel", command=self.cancel_preferences)
        cancel_button.pack(side="right", padx=(5, 10), pady=10)
    
    def load_preferences(self) -> None:
        try:
            settings = self.controller.get_settings()
            print("DEBUG: preferences loaded:", settings)
            
            # Always set default values, then override with saved settings if they exist
            print("DEBUG: Setting default preferences first...")
            
            # Set default values
            self.work_duration_var.set("20")
            self.break_duration_var.set("5")
            self.auto_start_var.set(False)
            
            if settings:
                print("DEBUG: work_duration type:", type(settings.get('work_duration')))
                print("DEBUG: break_duration type:", type(settings.get('break_duration')))
                print("DEBUG: auto_start type:", type(settings.get('auto_start')))
                
                # Safely convert numeric values with proper error handling
                try:
                    work_duration = settings.get('work_duration')
                    if work_duration is not None:
                        if isinstance(work_duration, str):
                            work_duration = int(work_duration)
                        self.work_duration_var.set(str(work_duration))
                        print(f"DEBUG: Set work_duration to {work_duration}")
                except (ValueError, TypeError):
                    print("DEBUG: Using default work_duration (25)")
                    self.work_duration_var.set("25")
                
                try:
                    break_duration = settings.get('break_duration')
                    if break_duration is not None:
                        if isinstance(break_duration, str):
                            break_duration = int(break_duration)
                        self.break_duration_var.set(str(break_duration))
                        print(f"DEBUG: Set break_duration to {break_duration}")
                except (ValueError, TypeError):
                    print("DEBUG: Using default break_duration (5)")
                    self.break_duration_var.set("5")
                
                # Boolean values - only set if they exist in settings
                if 'auto_start' in settings:
                    self.auto_start_var.set(bool(settings.get('auto_start', False)))
                    print(f"DEBUG: Set auto_start to {settings.get('auto_start')}")
            else:
                print("DEBUG: No preferences found, using defaults")
        except Exception as e:
            print(f"Error loading preferences: {e}")
            # Set default values if loading fails
            self.work_duration_var.set("25")
            self.break_duration_var.set("5")
            self.auto_start_var.set(False)
    
    def save_preferences(self) -> None:
        try:
            # Get string values and convert to integers with validation
            work_duration_str = self.work_duration_var.get().strip()
            break_duration_str = self.break_duration_var.get().strip()
            
            # Validate and convert to integers
            if not work_duration_str:
                work_duration_str = "25"
            if not break_duration_str:
                break_duration_str = "5"
            
            work_duration = int(work_duration_str)
            break_duration = int(break_duration_str)
            
            # Validate ranges
            if work_duration < 1 or work_duration > 480:  # 1 minute to 8 hours
                raise ValueError("Work duration must be between 1 and 480 minutes")
            if break_duration < 1 or break_duration > 120:  # 1 minute to 2 hours
                raise ValueError("Break duration must be between 1 and 120 minutes")
            
            preferences = {
                'work_duration': work_duration,
                'break_duration': break_duration,
                'auto_start': bool(self.auto_start_var.get())
            }
            print(f"DEBUG: Saving preferences: {preferences}")
            self.controller.save_settings(preferences)
            print("✓ Preferences saved successfully")
            print("DEBUG: Closing preferences window...")
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Success", "Preferences saved successfully!")
            
            # Refresh timer settings in main window
            try:
                if hasattr(self.controller, 'main_window_ref'):
                    self.controller.main_window_ref.refresh_timer_settings()
                    print("DEBUG: Timer settings refreshed")
            except Exception as e:
                print(f"DEBUG: Error refreshing timer settings: {e}")
            
            self.master.destroy()
            print("DEBUG: Preferences window closed")
        except ValueError as e:
            self.show_error("Invalid Preferences", f"Please check your input values: {e}")
        except Exception as e:
            self.show_error("Error", f"Failed to save preferences: {e}")
    
    def reset_preferences(self) -> None:
        self.work_duration_var.set("25")
        self.break_duration_var.set("5")
        self.auto_start_var.set(False)
    
    def cancel_preferences(self) -> None:
        self.master.destroy()
    
    def show_error(self, title: str, message: str) -> None:
        import tkinter.messagebox as messagebox
        messagebox.showerror(title, message) 