import customtkinter as ctk
from datetime import datetime, timedelta
import threading
import time
from src.models.settings import SettingsManager

class BreakPopup(ctk.CTkToplevel):
    """Break notification popup."""
    
    def __init__(self, master, controller) -> None:
        print("DEBUG: BreakPopup __init__ called")
        super().__init__(master)
        self.controller = controller
        self.title("Break Time!")
        self.geometry("500x450")  # Reduced height to remove empty space
        self.resizable(False, False)
        # Make modal and grab set
        self.transient(master)
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (450 // 2)
        self.geometry(f"500x450+{x}+{y}")
        self.deiconify()
        self.lift()
        self.focus_force()
        # Only call grab_set if window is viewable
        self.update_idletasks()
        if self.winfo_viewable():
            try:
                self.grab_set()
            except Exception as e:
                print(f"Warning: Could not grab popup: {e}")
        else:
            print("DEBUG: BreakPopup not viewable, skipping grab_set")
        self.break_slot = None
        self.occurrence_time = None
        self.break_timer_running = False
        self.break_timer_thread = None
        self.break_start_time = None
        self.break_remaining = 0
        self.break_completed = False  # Track if break finished
        self.setup_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_window_close)
    
    def setup_ui(self) -> None:
        """Setup user interface."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(self, text="Break Time!", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, pady=(20, 10), sticky="ew")
        
        # Main content frame
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Break info
        self.break_info_label = ctk.CTkLabel(main_frame, text="Time for your break!", 
                                            font=ctk.CTkFont(size=16))
        # Use only grid everywhere (no pack)
        # Break info label
        self.break_info_label = ctk.CTkLabel(main_frame, text="Time for your break!", font=ctk.CTkFont(size=16))
        self.break_info_label.grid(row=0, column=0, columnspan=2, pady=20, sticky="ew")
        
        # Timer display frame
        timer_frame = ctk.CTkFrame(main_frame)
        timer_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        timer_frame.grid_columnconfigure(0, weight=1)
        
        self.timer_label = ctk.CTkLabel(timer_frame, text="--:--", font=ctk.CTkFont(size=32, weight="bold"))
        self.timer_label.grid(row=0, column=0, pady=10, sticky="ew")
        self.progress_bar = ctk.CTkProgressBar(timer_frame)
        self.progress_bar.grid(row=1, column=0, pady=(0, 10), padx=20, sticky="ew")
        self.progress_bar.set(0)
        
        # Time details frame
        time_frame = ctk.CTkFrame(main_frame)
        time_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        time_frame.grid_columnconfigure(0, weight=1)
        self.start_time_label = ctk.CTkLabel(time_frame, text="Start: --:--", font=ctk.CTkFont(size=12))
        self.start_time_label.grid(row=0, column=0, pady=5, sticky="ew")
        self.end_time_label = ctk.CTkLabel(time_frame, text="End: --:--", font=ctk.CTkFont(size=12))
        self.end_time_label.grid(row=1, column=0, pady=5, sticky="ew")
        
        # Buttons frame
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        self.start_button = ctk.CTkButton(button_frame, text="Start Break", command=self.start_break)
        self.start_button.grid(row=0, column=0, padx=5, pady=8, sticky="ew")
        self.stop_button = ctk.CTkButton(button_frame, text="Stop", command=self.stop_break, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5, pady=8, sticky="ew")
        self.snooze_button = ctk.CTkButton(button_frame, text="Snooze", command=self.snooze_break)
        self.snooze_button.grid(row=0, column=2, padx=5, pady=8, sticky="ew")
        
        # Skip/OK and Close buttons (row 4, columns 0 and 1)
        self.skip_button = ctk.CTkButton(main_frame, text="Skip", command=self.skip_break)
        self.skip_button.grid(row=4, column=0, padx=(20, 5), pady=8, sticky="ew")
        self.close_button = ctk.CTkButton(main_frame, text="Close", command=self.close_break)
        self.close_button.grid(row=4, column=1, padx=(5, 20), pady=8, sticky="ew")
        main_frame.grid_rowconfigure(0, weight=0)
        main_frame.grid_rowconfigure(1, weight=0)
        main_frame.grid_rowconfigure(2, weight=0)
        main_frame.grid_rowconfigure(3, weight=0)
        main_frame.grid_rowconfigure(4, weight=0)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

    def set_skip_button_to_ok(self):
        # Change skip button to OK and update its command
        if hasattr(self, 'skip_button') and self.skip_button.winfo_exists():
            self.skip_button.grid()  # Ensure visible
            self.skip_button.configure(text="OK", command=self.close_break)
    
    def set_break_info(self, break_slot, occurrence_time, manual_break=False, was_timer_running=False) -> None:
        print(f"DEBUG: set_break_info called - manual_break={manual_break}, slot={break_slot}, occurrence_time={occurrence_time}")
        self.break_slot = break_slot
        self.occurrence_time = occurrence_time
        self.manual_break = manual_break
        self.was_timer_running = was_timer_running
        if break_slot:
            message = getattr(break_slot, 'message', None)
            if message:
                self.break_info_label.configure(text=message)
            else:
                self.break_info_label.configure(text=f"Time for your {break_slot.duration}-minute break!")
            self.break_remaining = break_slot.duration * 60
            # Always reset timer and labels for default/scheduled popups
            self.break_timer_running = False
            self.break_start_time = None
            self.start_time_label.configure(text="Start: --:--")
            self.end_time_label.configure(text="End: --:--")
            self.update_timer_display()
            # Play alert sound as soon as popup is shown
            try:
                if hasattr(self.controller, 'play_notification_sound'):
                    self.controller.play_notification_sound()
            except Exception as e:
                print(f"DEBUG: Could not play break start sound: {e}")
            # Always enable skip and close buttons
            self.skip_button.grid()
            self.close_button.grid()
            # For manual break (Break Now), start immediately
            if self.manual_break:
                self.after(100, self.auto_start_break)
                self.start_button.configure(text="Pause", command=self.pause_break, state="normal")
                self.stop_button.configure(state="normal")
            else:
                # For default/scheduled, do not auto start, but ensure timer is reset and buttons are correct
                self.start_button.configure(text="Start Break", command=self.start_break, state="normal")
                self.stop_button.configure(state="disabled")
        else:
            self.break_info_label.configure(text="Time for your break!")
    
    # Removed calculate_next_break_time (no next break in popup)
    
    def auto_start_break(self) -> None:
        """Automatically start the break timer when popup opens (for manual break only)."""
        if self.break_slot and not self.break_timer_running:
            print("DEBUG: Auto-starting break timer")
            self.start_break()
        else:
            print(f"DEBUG: Cannot auto-start - break_slot: {self.break_slot}, timer_running: {self.break_timer_running}")
    
    def start_break(self) -> None:
        """Start the break timer (always resets for Break Again)."""
        if self.break_slot:
            print("DEBUG: Starting break timer (reset)")
            self.break_timer_running = True
            self.break_remaining = self.break_slot.duration * 60
            self.break_start_time = datetime.now()
            self.start_button.configure(text="Pause", command=self.pause_break, state="normal")
            self.stop_button.configure(state="normal")
            self.skip_button.grid()
            self.close_button.grid()
            # Update time labels
            start_time = self.break_start_time.strftime("%H:%M")
            end_time = (self.break_start_time + timedelta(minutes=self.break_slot.duration)).strftime("%H:%M")
            self.start_time_label.configure(text=f"Start: {start_time}")
            self.end_time_label.configure(text=f"End: {end_time}")
            self.update_timer_display()
            self.break_timer_thread = threading.Thread(target=self.break_timer_loop, daemon=True)
            self.break_timer_thread.start()
        else:
            print(f"DEBUG: Cannot start break - break_slot: {self.break_slot}")
    
    def pause_break(self) -> None:
        """Pause the break timer."""
        if self.break_timer_running:
            self.break_timer_running = False
            self.start_button.configure(text="Resume", command=self.resume_break)
    
    def resume_break(self) -> None:
        """Resume the break timer."""
        if not self.break_timer_running:
            self.break_timer_running = True
            self.start_button.configure(text="Pause", command=self.pause_break)
            
            # Restart timer thread
            self.break_timer_thread = threading.Thread(target=self.break_timer_loop, daemon=True)
            self.break_timer_thread.start()
    
    def stop_break(self) -> None:
        """Stop the break timer."""
        self.break_timer_running = False
        self.start_button.configure(text="Start Break", command=self.start_break)
        self.stop_button.configure(state="disabled")
        self.break_remaining = self.break_slot.duration * 60 if self.break_slot else 0
        self.update_timer_display()
        self.progress_bar.set(0)
    
    def snooze_break(self) -> None:
        """Snooze the break for 5 minutes."""
        if self.break_slot:
            # Add 5 minutes to break duration
            self.break_slot.duration += 5
            self.break_remaining = self.break_slot.duration * 60
            
            # Update display
            self.break_info_label.configure(
                text=f"Time for your {self.break_slot.duration}-minute break!"
            )
            self.update_timer_display()
            
            # Update end time if timer is running
            if self.break_timer_running and self.break_start_time:
                end_time = (self.break_start_time + timedelta(minutes=self.break_slot.duration)).strftime("%H:%M")
                self.end_time_label.configure(text=f"End: {end_time}")
    
    def break_timer_loop(self) -> None:
        """Break timer loop running in separate thread."""
        while self.break_timer_running and self.break_remaining > 0:
            time.sleep(1)
            self.break_remaining -= 1
            # Update UI in main thread
            if self.break_timer_running:
                self.after(0, self.update_timer_display)
        if self.break_timer_running:
            # Break timer finished
            self.after(0, self.break_finished)

    def update_timer_display(self) -> None:
        """Update timer display."""
        try:
            minutes = self.break_remaining // 60
            seconds = self.break_remaining % 60
            timer_text = f"{minutes:02d}:{seconds:02d}"
            # Check if widget still exists before updating
            if hasattr(self, 'timer_label') and self.timer_label.winfo_exists():
                self.timer_label.configure(text=timer_text)
            # Update progress bar
            if self.break_slot and hasattr(self, 'progress_bar') and self.progress_bar.winfo_exists():
                total_seconds = self.break_slot.duration * 60
                progress = 1 - (self.break_remaining / total_seconds)
                self.progress_bar.set(progress)
            # Debug output for first few seconds and every 30 seconds
            if self.break_remaining > 0:
                if self.break_remaining <= 60 or self.break_remaining % 30 == 0:
                    print(f"DEBUG: Break timer: {timer_text} remaining ({self.break_remaining} seconds)")
        except Exception as e:
            print(f"DEBUG: Error updating timer display: {e}")
            self.break_timer_running = False

    def break_finished(self) -> None:
        """Handle break completion."""
        print("DEBUG: Break timer finished")
        self.break_timer_running = False
        self.break_completed = True
        # Only update widgets if they still exist
        if hasattr(self, 'start_button') and self.start_button.winfo_exists():
            self.start_button.configure(text="Break Again", command=self.start_break, state="normal")
        if hasattr(self, 'stop_button') and self.stop_button.winfo_exists():
            self.stop_button.configure(state="disabled")
        if hasattr(self, 'break_info_label') and self.break_info_label.winfo_exists():
            self.break_info_label.configure(text="Break completed!")
        if hasattr(self, 'timer_label') and self.timer_label.winfo_exists():
            self.timer_label.configure(text="00:00")
        if hasattr(self, 'progress_bar') and self.progress_bar.winfo_exists():
            self.progress_bar.set(1.0)
        # Change skip button to OK and ensure both buttons visible
        self.set_skip_button_to_ok()
        if hasattr(self, 'close_button') and self.close_button.winfo_exists():
            self.close_button.grid()
        # Play alert sound
        try:
            if hasattr(self.controller, 'play_notification_sound'):
                self.controller.play_notification_sound()
        except Exception as e:
            print(f"DEBUG: Could not play break end sound: {e}")

    def on_window_close(self):
        """Handle window close event (X button)."""
        print("DEBUG: on_window_close called")
        self._close_popup()

    def skip_break(self):
        """Handle skip button click."""
        print("DEBUG: skip_break called")
        self._close_popup()

    def close_break(self):
        """Handle close/OK button click."""
        print("DEBUG: close_break called")
        self._close_popup()

    def _close_popup(self):
        """Unified method to close the popup safely."""
        try:
            # Stop the break timer
            self.break_timer_running = False
            print("DEBUG: Stopping break timer")
            
            # Release grab if we have it
            try:
                self.grab_release()
                print("DEBUG: Released grab")
            except Exception as e:
                print(f"DEBUG: Could not release grab: {e}")
            
            # Handle post-break logic before destroying
            self.handle_post_break_close()
            
            # Destroy the window
            self.destroy()
            print("DEBUG: Popup destroyed successfully")
            
        except Exception as e:
            print(f"DEBUG: Exception in _close_popup: {e}")
            # Force destroy as last resort
            try:
                self.after_idle(self.destroy)
            except Exception as e2:
                print(f"DEBUG: Could not force destroy: {e2}")

    def should_auto_start(self):
        """Return True if auto start next session is enabled in settings."""
        if hasattr(self.controller, 'get_settings'):
            settings = self.controller.get_settings()
            return bool(settings.get('auto_start', False))
        return False

    def handle_post_break_close(self):
        """Handle logic after break popup is closed (manual or default break)."""
        try:
            # Only auto-start if auto-start is enabled AND the work timer was actually interrupted by this break
            if self.should_auto_start() and getattr(self, 'was_timer_running', False):
                print("DEBUG: Auto-starting work session after break popup close (timer was interrupted).")
                self.start_work_timer()
            else:
                if not getattr(self, 'was_timer_running', False):
                    print("DEBUG: Not auto-starting; work timer was not running when break started.")
                else:
                    print("DEBUG: Not auto-starting; auto-start disabled in settings.")
                # Ensure main window is reset to work session
                if hasattr(self.controller, 'main_window') and hasattr(self.controller.main_window, 'reset_timer'):
                    try:
                        self.controller.main_window.reset_timer()
                    except Exception as e:
                        print(f"DEBUG: Could not reset timer after break popup close: {e}")
        except Exception as e:
            print(f"DEBUG: Error in handle_post_break_close: {e}")

    def dismiss(self) -> None:
        """Dismiss the popup (legacy, for compatibility)."""
        self.close_break()

    def start_work_timer(self):
        """Start the work timer in the main window."""
        if hasattr(self.controller, 'main_window') and hasattr(self.controller.main_window, 'start_timer'):
            try:
                self.controller.main_window.start_timer()
            except Exception as e:
                print(f"DEBUG: Could not start work timer: {e}")
