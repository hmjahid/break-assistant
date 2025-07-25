import customtkinter as ctk
from typing import Optional
from src.models.settings import SettingsManager

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
        # Configure the main frame to expand properly
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create scrollable frame with proper sizing
        self.scrollable = ctk.CTkScrollableFrame(self, height=600)
        self.scrollable.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scrollable.grid_columnconfigure(0, weight=1)
        self.scrollable.grid_rowconfigure(99, weight=1)  # Add a spacer row at the end
        
        # Fix mouse wheel scrolling
        self.bind_mousewheel()
        
        # Info section
        try:
            info_label = ctk.CTkLabel(self.scrollable, text="Configure your work/break intervals and timer preferences.", font=ctk.CTkFont(size=13), justify="center", wraplength=500, text_color="gray")
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
        
        # After timer settings section, add custom break message
        try:
            self.create_custom_message(self.scrollable, 3)
        except Exception as e:
            print(f"Error in create_custom_message: {e}")
            raise
        
        # Buttons
        try:
            self.create_buttons(self.scrollable, 100)
        except Exception as e:
            print(f"Error in create_buttons: {e}")
            raise
    
    def bind_mousewheel(self):
        """Bind mouse wheel events for scrolling."""
        # Windows/Mac
        self.scrollable.bind_all("<MouseWheel>", self._on_mousewheel)
        # Linux
        self.scrollable.bind_all("<Button-4>", self._on_mousewheel_linux)
        self.scrollable.bind_all("<Button-5>", self._on_mousewheel_linux)
    
    def _on_mousewheel(self, event):
        try:
            self.scrollable._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except Exception:
            pass
    
    def _on_mousewheel_linux(self, event):
        """Handle mouse wheel scrolling on Linux."""
        try:
            if event.num == 4:  # Scroll up
                self.scrollable._parent_canvas.yview_scroll(-1, "units")
            elif event.num == 5:  # Scroll down
                self.scrollable._parent_canvas.yview_scroll(1, "units")
        except Exception:
            pass
    
    def create_timer_settings(self, parent, row):
        print("DEBUG: Entering create_timer_settings")
        timer_frame = ctk.CTkFrame(parent)
        timer_frame.grid(row=row, column=0, sticky="ew", pady=(0, 20), padx=10)
        timer_frame.grid_columnconfigure(1, weight=1)
        
        timer_title = ctk.CTkLabel(timer_frame, text="Timer Settings", font=ctk.CTkFont(size=16, weight="bold"))
        timer_title.grid(row=0, column=0, columnspan=2, pady=(10, 15), sticky="ew")
        
        work_label = ctk.CTkLabel(timer_frame, text="Default Work Duration (minutes):", wraplength=300)
        work_label.grid(row=1, column=0, padx=(15, 10), pady=5, sticky="w")
        self.work_duration_var = ctk.StringVar(value="20")
        work_entry = ctk.CTkEntry(timer_frame, textvariable=self.work_duration_var, width=100)
        work_entry.grid(row=1, column=1, padx=(0, 15), pady=5, sticky="w")
        
        break_label = ctk.CTkLabel(timer_frame, text="Default Break Duration (minutes):", wraplength=300)
        break_label.grid(row=2, column=0, padx=(15, 10), pady=5, sticky="w")
        self.break_duration_var = ctk.StringVar(value="1")
        break_entry = ctk.CTkEntry(timer_frame, textvariable=self.break_duration_var, width=100)
        break_entry.grid(row=2, column=1, padx=(0, 15), pady=5, sticky="w")
        
        # Add default break message input field
        default_break_message_label = ctk.CTkLabel(timer_frame, text="Default Break Message:", wraplength=300)
        default_break_message_label.grid(row=3, column=0, padx=(15, 10), pady=5, sticky="w")
        self.default_break_message_var = ctk.StringVar(value="Time for your break!")
        default_break_message_entry = ctk.CTkEntry(timer_frame, textvariable=self.default_break_message_var)
        default_break_message_entry.grid(row=3, column=1, padx=(0, 15), pady=5, sticky="ew")
        
        self.auto_start_var = ctk.BooleanVar(value=False)
        auto_start_check = ctk.CTkCheckBox(timer_frame, text="Auto-start next session", variable=self.auto_start_var)
        auto_start_check.grid(row=4, column=0, columnspan=2, padx=15, pady=5, sticky="w")
    
    def create_custom_message(self, parent, row):
        message_frame = ctk.CTkFrame(parent)
        message_frame.grid(row=row, column=0, sticky="ew", pady=(0, 20), padx=10)
        message_frame.grid_columnconfigure(1, weight=1)
        message_title = ctk.CTkLabel(message_frame, text="Custom Break", font=ctk.CTkFont(size=16, weight="bold"))
        message_title.grid(row=0, column=0, columnspan=2, pady=(10, 15), sticky="ew")
        
        # Custom break duration (moved from timer settings)
        custom_break_duration_label = ctk.CTkLabel(message_frame, text="Custom Break Duration (minutes):", wraplength=300)
        custom_break_duration_label.grid(row=1, column=0, padx=(15, 10), pady=5, sticky="w")
        self.manual_break_duration_var = ctk.StringVar(value="15")
        custom_break_duration_entry = ctk.CTkEntry(message_frame, textvariable=self.manual_break_duration_var, width=100)
        custom_break_duration_entry.grid(row=1, column=1, padx=(0, 15), pady=5, sticky="w")
        
        # Custom break message
        message_label = ctk.CTkLabel(message_frame, text="Custom Break Message:", wraplength=300)
        message_label.grid(row=2, column=0, padx=(15, 10), pady=5, sticky="w")
        self.break_message_var = ctk.StringVar(value="Time for a break!")
        message_entry = ctk.CTkEntry(message_frame, textvariable=self.break_message_var)
        message_entry.grid(row=2, column=1, padx=(0, 15), pady=5, sticky="ew")

    def create_buttons(self, parent, row):
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.grid(row=row, column=0, sticky="ew", pady=(20, 10), padx=10)
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)
        
        save_button = ctk.CTkButton(buttons_frame, text="Save Preferences", command=self.save_preferences)
        save_button.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        
        reset_button = ctk.CTkButton(buttons_frame, text="Reset to Defaults", command=self.reset_preferences)
        reset_button.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        cancel_button = ctk.CTkButton(buttons_frame, text="Cancel", command=self.cancel_preferences)
        cancel_button.grid(row=0, column=2, padx=(5, 10), pady=10, sticky="ew")
    
    def load_preferences(self) -> None:
        try:
            settings = self.controller.get_settings()
            print("DEBUG: preferences loaded:", settings)
            
            # Always set default values, then override with saved settings if they exist
            print("DEBUG: Setting default preferences first...")
            
            # Set default values
            self.work_duration_var.set("20")
            self.break_duration_var.set("1")
            self.default_break_message_var.set("Time for your break!")
            self.manual_break_duration_var.set("15")
            self.auto_start_var.set(False)
            self.break_message_var.set("Time for a break!")
            
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
                    print("DEBUG: Using default work_duration (20)")
                    self.work_duration_var.set("20")
                
                try:
                    break_duration = settings.get('break_duration')
                    if break_duration is not None:
                        if isinstance(break_duration, str):
                            break_duration = int(break_duration)
                        self.break_duration_var.set(str(break_duration))
                        print(f"DEBUG: Set break_duration to {break_duration}")
                except (ValueError, TypeError):
                    print("DEBUG: Using default break_duration (1)")
                    self.break_duration_var.set("1")
                
                # Load manual break duration
                try:
                    manual_break_duration = settings.get('manual_break_duration')
                    if manual_break_duration is not None:
                        if isinstance(manual_break_duration, str):
                            manual_break_duration = int(manual_break_duration)
                        self.manual_break_duration_var.set(str(manual_break_duration))
                        print(f"DEBUG: Set manual_break_duration to {manual_break_duration}")
                except (ValueError, TypeError):
                    print("DEBUG: Using default manual_break_duration (15)")
                    self.manual_break_duration_var.set("15")
                
                # Boolean values - only set if they exist in settings
                if 'auto_start' in settings:
                    self.auto_start_var.set(bool(settings.get('auto_start', False)))
                    print(f"DEBUG: Set auto_start to {settings.get('auto_start')}")
                
                if 'default_break_message' in settings:
                    self.default_break_message_var.set(settings['default_break_message'])
                    print(f"DEBUG: Set default_break_message to {settings['default_break_message']}")
                
                if 'break_message' in settings:
                    self.break_message_var.set(settings['break_message'])
                    print(f"DEBUG: Set break_message to {settings['break_message']}")
            else:
                print("DEBUG: No preferences found, using defaults")
        except Exception as e:
            print(f"Error loading preferences: {e}")
            # Set default values if loading fails
            self.work_duration_var.set("20")
            self.break_duration_var.set("1")
            self.default_break_message_var.set("Time for your break!")
            self.manual_break_duration_var.set("15")
            self.auto_start_var.set(False)
            self.break_message_var.set("Time for a break!")
    
    def save_preferences(self) -> None:
        try:
            # Get string values and convert to integers with validation
            work_duration_str = self.work_duration_var.get().strip()
            break_duration_str = self.break_duration_var.get().strip()
            manual_break_duration_str = self.manual_break_duration_var.get().strip()
            
            # Validate and convert to integers
            if not work_duration_str:
                work_duration_str = "20"
            if not break_duration_str:
                break_duration_str = "1"
            if not manual_break_duration_str:
                manual_break_duration_str = "15"
            
            work_duration = int(work_duration_str)
            break_duration = int(break_duration_str)
            manual_break_duration = int(manual_break_duration_str)
            
            # Validate ranges
            if work_duration < 1 or work_duration > 480:  # 1 minute to 8 hours
                raise ValueError("Work duration must be between 1 and 480 minutes")
            if break_duration < 1 or break_duration > 120:  # 1 minute to 2 hours
                raise ValueError("Break duration must be between 1 and 120 minutes")
            if manual_break_duration < 1 or manual_break_duration > 120:  # 1 minute to 2 hours
                raise ValueError("Manual break duration must be between 1 and 120 minutes")
            
            preferences = {
                'work_duration': work_duration,
                'break_duration': break_duration,
                'default_break_message': self.default_break_message_var.get(),
                'manual_break_duration': manual_break_duration,
                'auto_start': bool(self.auto_start_var.get()),
                'break_message': self.break_message_var.get()
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
        self.work_duration_var.set("20")
        self.break_duration_var.set("1")
        self.default_break_message_var.set("Time for your break!")
        self.manual_break_duration_var.set("15")
        self.auto_start_var.set(False)
        self.break_message_var.set("Time for a break!")
    
    def cancel_preferences(self) -> None:
        self.master.destroy()
    
    def show_error(self, title: str, message: str) -> None:
        import tkinter.messagebox as messagebox
        messagebox.showerror(title, message) 