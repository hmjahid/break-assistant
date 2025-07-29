import customtkinter as ctk
from typing import Optional
from datetime import datetime, timedelta
import threading
import time


class MainWindow(ctk.CTk):
    def show_break_notification(self):
        """Show break popup when timer finishes (default break), always using duration from preferences/settings."""
        try:
            from src.views.break_popup import BreakPopup
            settings = self.controller.get_settings() if hasattr(self.controller, 'get_settings') else {}
            break_duration = int(settings.get('break_duration', 1))
            break_message = settings.get('default_break_message', 'Time for your break!')
            
            # Show system notification if enabled
            system_notifications = settings.get('system_notifications', True)
            if system_notifications:
                try:
                    platform_utils = self.controller.get_platform_utils()
                    platform_utils.show_system_notification("Break Time!", break_message)
                    print("DEBUG: System notification shown for default break")
                except Exception as e:
                    print(f"DEBUG: Could not show system notification: {e}")
            
            class DefaultBreakSlot:
                duration = break_duration
                scheduled = False
                message = break_message
            break_slot = DefaultBreakSlot()
            occurrence_time = datetime.now()
            popup = BreakPopup(self, self.controller)
            popup.set_break_info(break_slot, occurrence_time, manual_break=False, was_timer_running=self.timer_running)
        except Exception as e:
            print(f"Error in show_break_notification: {e}")
    def start_break_now(self) -> None:
        """
        Trigger a manual break popup immediately, always using duration and custom message from preferences/settings. Also pause work timer.
        """
        try:
            from src.views.break_popup import BreakPopup
            settings = self.controller.get_settings() if hasattr(self.controller, 'get_settings') else {}
            break_duration = int(settings.get('manual_break_duration', 15))
            break_message = settings.get('break_message', 'Time for a break!')
            
            # Show system notification if enabled
            system_notifications = settings.get('system_notifications', True)
            if system_notifications:
                try:
                    platform_utils = self.controller.get_platform_utils()
                    platform_utils.show_system_notification("Manual Break", break_message)
                    print("DEBUG: System notification shown for manual break")
                except Exception as e:
                    print(f"DEBUG: Could not show system notification: {e}")
            
            # Pause work timer if running
            was_timer_running = self.timer_running
            self.stop_timer()
            class ManualBreakSlot:
                duration = break_duration
                scheduled = False
                message = break_message
            break_slot = ManualBreakSlot()
            occurrence_time = datetime.now()
            popup = BreakPopup(self, self.controller)
            popup.set_break_info(break_slot, occurrence_time, manual_break=True, was_timer_running=was_timer_running)
        except Exception as e:
            print(f"Error in start_break_now: {e}")
    """Main application window."""
    
    def __init__(self, controller) -> None:
        """Initialize main window.
        
        Args:
            controller: Application controller
        """
        super().__init__()
        self.controller = controller
        self.title("Break Assistant")
        self.geometry("500x464")  # Match break popup width
        self.minsize(500, 464)  # Keep min width at 500
        
        # Timer variables
        self.timer_running = False
        self.timer_thread = None
        self.current_break_slot = None
        self.next_break_time = None
        
        self.setup_ui()
        self.setup_timer()
        
        # Start timeline monitoring
        self.start_timeline_monitor()
    
    def setup_ui(self) -> None:
        """Setup user interface."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Menu bar
        self.setup_menu()

        # Title
        title_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=1, column=0, padx=10, pady=(0, 0), sticky="ew")

        # Main content frame
        main_frame = ctk.CTkFrame(self, fg_color=("gray85", "gray17"))
        main_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)

        # Timer Display Group
        timer_display_frame = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray17"))
        timer_display_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        timer_display_frame.grid_columnconfigure(0, weight=1)

        # Status Label
        self.status_label = ctk.CTkLabel(timer_display_frame, text="🎯 Ready", font=ctk.CTkFont(size=18, weight="bold"), text_color=("#2E7D32", "#66BB6A"))
        self.status_label.grid(row=0, column=0, pady=(10, 5), padx=20, sticky="ew")

        # Main Timer Display
        self.timer_label = ctk.CTkLabel(timer_display_frame, text="--:--", font=ctk.CTkFont(size=48, weight="bold"), text_color=("#1565C0", "#42A5F5"))
        self.timer_label.grid(row=1, column=0, pady=(5, 10), padx=20, sticky="ew")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(timer_display_frame, height=12, progress_color=("#4CAF50", "#66BB6A"))
        self.progress_bar.grid(row=2, column=0, padx=40, pady=(0, 15), sticky="ew")
        self.progress_bar.set(0)

        # Button frame
        button_frame = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray17"))
        button_frame.grid(row=3, column=0, pady=(10, 4), padx=20, sticky="ew")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        # Start/Stop button
        self.start_button = ctk.CTkButton(button_frame, text="▶️ Start Work", command=self.toggle_timer, width=140, height=35, font=ctk.CTkFont(size=13, weight="bold"), fg_color=("#2E7D32", "#4CAF50"), hover_color=("#1B5E20", "#388E3C"))
        self.start_button.grid(row=0, column=0, padx=5, pady=4, sticky="ew")

        # Reset button
        reset_button = ctk.CTkButton(button_frame, text="🔄 Reset", command=self.reset_timer, width=140, height=35, font=ctk.CTkFont(size=13, weight="bold"), fg_color=("#F57C00", "#FF9800"), hover_color=("#E65100", "#F57C00"))
        reset_button.grid(row=0, column=1, padx=5, pady=4, sticky="ew")

        # Break Now button
        break_now_button = ctk.CTkButton(main_frame, text="🚨 Break Now", command=self.start_break_now, height=40, font=ctk.CTkFont(size=14, weight="bold"), fg_color=("#D32F2F", "#F44336"), hover_color=("#B71C1C", "#D32F2F"))
        break_now_button.grid(row=4, column=0, padx=25, pady=4, sticky="ew")

        # Settings button frame
        settings_button_frame = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray17"))
        settings_button_frame.grid(row=5, column=0, pady=4, padx=20, sticky="ew")
        settings_button_frame.grid_columnconfigure((0, 1), weight=1)

        # Timeline button
        timeline_button = ctk.CTkButton(settings_button_frame, text="📅 Timeline", command=self.open_timeline, width=140, height=35, font=ctk.CTkFont(size=13, weight="bold"), fg_color=("#7B1FA2", "#9C27B0"), hover_color=("#4A148C", "#7B1FA2"))
        timeline_button.grid(row=0, column=0, padx=5, pady=2, sticky="ew")

        # Preferences button
        preferences_button = ctk.CTkButton(settings_button_frame, text="⚙️ Preferences", command=self.open_preferences, width=140, height=35, font=ctk.CTkFont(size=13, weight="bold"), fg_color=("#455A64", "#607D8B"), hover_color=("#263238", "#455A64"))
        preferences_button.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        # Next Break Label
        self.next_break_label = ctk.CTkLabel(main_frame, text="No breaks scheduled", font=ctk.CTkFont(size=12), text_color=("#1565C0", "#42A5F5"))
        self.next_break_label.grid(row=6, column=0, pady=(15, 10), padx=20, sticky="ew")
    
    def setup_menu(self) -> None:
        """Setup menu bar."""
        menubar = ctk.CTkFrame(self, height=30)
        menubar.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))

        # About menu
        about_menu = ctk.CTkButton(menubar, text="About", width=60, height=25, command=self.open_about)
        about_menu.pack(side="left", padx=2)

        # Settings menu
        settings_menu = ctk.CTkButton(menubar, text="Settings", width=80, height=25, command=self.open_settings)
        settings_menu.pack(side="left", padx=2)

        # Help menu
        help_menu = ctk.CTkButton(menubar, text="Help", width=60, height=25, command=self.open_help)
        help_menu.pack(side="left", padx=2)

    def setup_timer(self) -> None:
        """Setup timer functionality."""
        settings = self.controller.get_settings() if hasattr(self.controller, 'get_settings') else {}
        try:
            work_duration_raw = settings.get('work_duration', 20)
            print(f"DEBUG: work_duration value: {work_duration_raw}, type: {type(work_duration_raw)}")
            work_duration = int(work_duration_raw)
        except (ValueError, TypeError):
            work_duration = 20
        self.timer_duration = work_duration * 60  # in seconds
        self.timer_remaining = self.timer_duration
        self.timer_start_time = None
    
    def refresh_timer_settings(self) -> None:
        """Refresh timer settings from saved preferences."""
        print("DEBUG: Refreshing timer settings...")
        settings = self.controller.get_settings()
        try:
            work_duration_raw = settings.get('work_duration', 25)
            print(f"DEBUG: Refreshing work_duration: {work_duration_raw}, type: {type(work_duration_raw)}")
            work_duration = int(work_duration_raw)
            
            # Update timer duration
            self.timer_duration = work_duration * 60  # in seconds
            
            # If timer is not running, reset to new duration
            if not self.timer_running:
                self.timer_remaining = self.timer_duration
                self.update_timer_display()
                print(f"DEBUG: Timer reset to {work_duration} minutes")
            else:
                print("DEBUG: Timer is running, duration will be updated on next reset")
                
        except (ValueError, TypeError) as e:
            print(f"DEBUG: Error refreshing timer settings: {e}")
            # Keep current settings if there's an error
        self.refresh_next_break_label()
    
    def toggle_timer(self) -> None:
        """Toggle timer start/stop."""
        if self.timer_running:
            self.stop_timer()
        else:
            self.start_timer()
    
    def start_timer(self) -> None:
        """Start the timer."""
        if not self.timer_running:
            self.timer_running = True
            self.timer_start_time = datetime.now()
            self.start_button.configure(text="⏸️ Stop")
            self.status_label.configure(text="💼 Working...", text_color=("#1565C0", "#42A5F5"))
            
            # Start timer thread
            self.timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
            self.timer_thread.start()
    
    def stop_timer(self) -> None:
        """Stop the timer."""
        if self.timer_running:
            self.timer_running = False
            self.start_button.configure(text="▶️ Start Work")
            self.status_label.configure(text="⏸️ Paused", text_color=("#F57C00", "#FF9800"))
    
    def reset_timer(self) -> None:
        """Reset the timer."""
        self.stop_timer()
        self.timer_remaining = self.timer_duration
        self.update_timer_display()
        self.progress_bar.set(0)
        self.status_label.configure(text="🎯 Ready", text_color=("#2E7D32", "#4CAF50"))
    
    def timer_loop(self) -> None:
        """Timer loop running in separate thread."""
        while self.timer_running and int(self.timer_remaining) > 0:
            time.sleep(1)
            self.timer_remaining -= 1
            
            # Update UI in main thread
            self.after(0, self.update_timer_display)
        
        if self.timer_running:
            # Timer finished
            self.after(0, self.timer_finished)
    
    def update_timer_display(self) -> None:
        """Update timer display."""
        if not self.winfo_exists():  # Check if the window exists
            return
        timer_remaining = int(self.timer_remaining)
        timer_duration = int(self.timer_duration)
        minutes = timer_remaining // 60
        seconds = timer_remaining % 60
        self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
        
        # Update progress bar
        if timer_duration > 0:
            progress = 1 - (timer_remaining / timer_duration)
            self.progress_bar.set(progress)
        else:
            self.progress_bar.set(0)
    
    def timer_finished(self) -> None:
        """Handle timer completion."""
        self.timer_running = False
        self.start_button.configure(text="▶️ Start Work")
        self.status_label.configure(text="🎉 Break time!", text_color=("#D32F2F", "#F44336"))
        
        # Reset timer to prevent continuous triggering
        self.timer_remaining = self.timer_duration
        self.update_timer_display()
        self.progress_bar.set(0)
        
        # Show break notification
        self.show_break_notification()
    
    def refresh_next_break_label(self):
        """Show only: Next Scheduled break: Today/Tomorrow at xx:xx (xmin/mins) or 'No break scheduled'."""
        try:
            next_break = self.controller.get_next_break()
            if next_break:
                break_slot, occurrence_time = next_break
                now = datetime.now()
                if occurrence_time.date() == now.date():
                    date_str = "Today"
                elif occurrence_time.date() == now.date() + timedelta(days=1):
                    date_str = "Tomorrow"
                else:
                    date_str = occurrence_time.strftime("%Y-%m-%d")
                mins = int(getattr(break_slot, 'duration', 0))
                min_label = "min" if mins == 1 else "mins"
                time_str = occurrence_time.strftime("%H:%M")
                self.next_break_label.configure(
                    text=f"Next Scheduled break: {date_str} at {time_str} ({mins} {min_label})"
                )
            else:
                self.next_break_label.configure(text="No break scheduled")
        except Exception as e:
            print(f"DEBUG: Error in refresh_next_break_label: {e}")

    def start_timeline_monitor(self) -> None:
        """Start monitoring timeline for upcoming breaks (scheduled breaks)."""
        if not self.controller:
            print("DEBUG: Controller not available, timeline monitor not started.")
            return
        def monitor_loop():
            last_popup_timestamp = None
            last_occurrence_time = None
            last_break_id = None
            
            print("DEBUG: Timeline monitor started")
            
            while True:
                try:
                    # Get next break from timeline
                    next_break = self.controller.get_next_break()
                    
                    if next_break:
                        orig_break_slot, occurrence_time = next_break
                        self.current_break_slot = orig_break_slot
                        self.next_break_time = occurrence_time
                        now = datetime.now()
                        
                        # Generate unique break ID
                        break_id = getattr(orig_break_slot, 'id', None) or f"{occurrence_time.timestamp()}_{orig_break_slot.duration}"
                        
                        print(f"DEBUG: Next break found - ID: {break_id}, Time: {occurrence_time}, Now: {now}")
                        
                        # Reset popup tracking if this is a new break
                        if last_occurrence_time is None or occurrence_time != last_occurrence_time or last_break_id != break_id:
                            last_popup_timestamp = None
                            last_occurrence_time = occurrence_time
                            last_break_id = break_id
                            print(f"DEBUG: New break detected, reset popup tracking")
                        
                        # Check if it's time to show the break (with 30-second tolerance)
                        time_diff = (occurrence_time - now).total_seconds()
                        if time_diff <= 30 and time_diff >= -30:  # Show break within 30 seconds of scheduled time
                            occ_ts = occurrence_time.timestamp()
                            if last_popup_timestamp != occ_ts:
                                print(f"DEBUG: Time to show scheduled break! Time diff: {time_diff} seconds")
                                
                                # Prepare break slot with proper duration
                                duration = getattr(orig_break_slot, 'duration', None)
                                if duration is None or duration <= 0:
                                    settings = self.controller.get_settings() if hasattr(self.controller, 'get_settings') else {}
                                    duration = int(settings.get('break_duration', 5))
                                
                                # Create a copy of the break slot with proper attributes
                                class ScheduledBreakSlot:
                                    def __init__(self):
                                        self.scheduled = True
                                
                                break_slot = ScheduledBreakSlot()
                                
                                # Copy all attributes from original break slot
                                for attr in ['start_time', 'duration', 'message', 'repeat_pattern', 'enabled', 'id']:
                                    if hasattr(orig_break_slot, attr):
                                        setattr(break_slot, attr, getattr(orig_break_slot, attr))
                                
                                # Ensure duration is set
                                break_slot.duration = duration
                                
                                # For scheduled breaks, preserve the timeline custom message if it exists
                                # Only use preferences message as fallback if no timeline message is set
                                timeline_message = getattr(orig_break_slot, 'message', None)
                                if timeline_message and timeline_message.strip():
                                    # Use the custom message from timeline
                                    break_slot.message = timeline_message
                                    print(f"DEBUG: Using timeline custom message: {timeline_message}")
                                else:
                                    # No timeline message, use preferences message as fallback
                                    settings = self.controller.get_settings() if hasattr(self.controller, 'get_settings') else {}
                                    preferences_message = settings.get('break_message', None)
                                    if preferences_message and preferences_message.strip():
                                        break_slot.message = preferences_message
                                        print(f"DEBUG: Using preferences message as fallback: {preferences_message}")
                                    else:
                                        # No custom messages, use default
                                        break_slot.message = f"Time for your {duration}-minute break!"
                                        print(f"DEBUG: Using default message")
                                
                                # Show the scheduled break popup
                                def show_scheduled_break():
                                    try:
                                        print("DEBUG: Creating scheduled BreakPopup")
                                        
                                        # Show system notification if enabled
                                        settings = self.controller.get_settings() if hasattr(self.controller, 'get_settings') else {}
                                        system_notifications = settings.get('system_notifications', True)
                                        if system_notifications:
                                            try:
                                                platform_utils = self.controller.get_platform_utils()
                                                # Use the custom message from the scheduled break if available
                                                notification_message = getattr(break_slot, 'message', None)
                                                if not notification_message or not notification_message.strip():
                                                    notification_message = f"Time for your {break_slot.duration}-minute break!"
                                                platform_utils.show_system_notification("Scheduled Break", notification_message)
                                                print("DEBUG: System notification shown for scheduled break")
                                            except Exception as e:
                                                print(f"DEBUG: Could not show system notification: {e}")
                                        
                                        # Pause work timer if it's running when scheduled break appears
                                        was_timer_running = self.timer_running
                                        if self.timer_running:
                                            print("DEBUG: Pausing work timer for scheduled break")
                                            self.stop_timer()
                                        
                                        from src.views.break_popup import BreakPopup
                                        popup = BreakPopup(self, self.controller)
                                        popup.set_break_info(break_slot, occurrence_time, manual_break=False, was_timer_running=was_timer_running)
                                        print("DEBUG: Scheduled BreakPopup created successfully")
                                    except Exception as e:
                                        print(f"DEBUG: Error creating scheduled break popup: {e}")
                                
                                # Schedule popup creation on main thread
                                self.after(0, show_scheduled_break)
                                last_popup_timestamp = occ_ts
                                print(f"DEBUG: Scheduled break popup queued for display")
                        else:
                            if time_diff > 30:
                                print(f"DEBUG: Break scheduled in {time_diff:.0f} seconds")
                    else:
                        print("DEBUG: No scheduled breaks found")
                    
                    # Update the next break label
                    self.after(0, self.refresh_next_break_label)
                    
                    # Sleep for 5 seconds before checking again
                    time.sleep(5)
                    
                except Exception as e:
                    print(f"DEBUG: Timeline monitor error: {e}")
                    import traceback
                    traceback.print_exc()
                    time.sleep(30)  # Wait longer on error
        
        print("DEBUG: Starting timeline monitor thread for scheduled breaks")
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def force_refresh_next_break(self) -> None:
        """Force an immediate refresh of the next break label."""
        try:
            next_break = self.controller.get_next_break()
            if next_break:
                break_slot, occurrence_time = next_break
                time_str = occurrence_time.strftime("%H:%M")
                # Ensure scheduled attribute is present for timeline breaks
                if not hasattr(break_slot, 'scheduled'):
                    break_slot.scheduled = True
                label_type = 'scheduled' if getattr(break_slot, 'scheduled', False) else 'default'
                
                # Check if the break is today or tomorrow
                now = datetime.now()
                if occurrence_time.date() == now.date():
                    date_str = "Today"
                elif occurrence_time.date() == now.date() + timedelta(days=1):
                    date_str = "Tomorrow"
                else:
                    date_str = occurrence_time.strftime("%Y-%m-%d")
                
                display_text = f"Next {label_type} break: {date_str} {time_str} ({break_slot.duration}min)"
                self.next_break_label.configure(text=display_text)
                print(f"DEBUG: Force refreshed next break label: {display_text}")
            else:
                self.next_break_label.configure(text="No breaks scheduled")
                print("DEBUG: Force refreshed - no breaks scheduled")
        except Exception as e:
            print(f"DEBUG: Error in force_refresh_next_break: {e}")
    
    def refresh_next_break_label(self):
        """Show only scheduled break: Today at xx:xx (xmin/mins) or 'No break scheduled'."""
        try:
            next_break = self.controller.get_next_break()
            if next_break:
                break_slot, occurrence_time = next_break
                now = datetime.now()
                if occurrence_time.date() == now.date():
                    date_str = "Today"
                elif occurrence_time.date() == now.date() + timedelta(days=1):
                    date_str = "Tomorrow"
                else:
                    date_str = occurrence_time.strftime("%Y-%m-%d")
                mins = int(getattr(break_slot, 'duration', 0))
                min_label = "min" if mins == 1 else "mins"
                time_str = occurrence_time.strftime("%H:%M")
                self.next_break_label.configure(
                    text=f"Next Scheduled Break: {date_str} at {time_str} ({mins} {min_label})"
                )
            else:
                self.next_break_label.configure(text="No break scheduled")
        except Exception as e:
            print(f"DEBUG: Error in refresh_next_break_label: {e}")
    
    def open_settings(self) -> None:
        """Open settings dialog."""
        try:
            self.deiconify()
            self.lift()
            self.focus_force()
            from src.settings_page import SettingsPage
            settings_window = ctk.CTkToplevel(self)
            settings_window.title("Settings")
            settings_window.transient(self)
            width = 500
            height = 500
            settings_window.geometry(f"{width}x{height}")
            settings_window.update_idletasks()
            x = (settings_window.winfo_screenwidth() // 2) - (width // 2)
            y = (settings_window.winfo_screenheight() // 2) - (height // 2)
            settings_window.geometry(f"{width}x{height}+{x}+{y}")
            try:
                settings_window.grab_set()
            except Exception as e:
                print(f"Warning: Could not make settings window modal: {e}")
            settings_page = SettingsPage(settings_window, self.controller)
            settings_page.pack(fill="both", expand=True, padx=20, pady=20)
        except Exception as e:
            print(f"Error opening settings: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Failed to open settings: {e}")
    
    def open_preferences(self) -> None:
        try:
            self.deiconify()
            self.lift()
            self.focus_force()
            from src.views.preferences_page import PreferencesPage
            preferences_window = ctk.CTkToplevel(self)
            preferences_window.title("Preferences")
            preferences_window.transient(self)
            
            # Set initial size to ensure all content is visible
            width = 500
            height = 590  # Increased height to accommodate all content
            preferences_window.geometry(f"{width}x{height}")
            preferences_window.minsize(width, 590)  # Minimum height
            preferences_window.resizable(True, True)
            
            # Center the window
            preferences_window.update_idletasks()
            x = (preferences_window.winfo_screenwidth() // 2) - (width // 2)
            y = (preferences_window.winfo_screenheight() // 2) - (height // 2)
            preferences_window.geometry(f"{width}x{height}+{x}+{y}")
            
            # Create and pack the preferences page
            preferences_page = PreferencesPage(preferences_window, self.controller)
            preferences_page.pack(fill="both", expand=True, padx=20, pady=20)
            
            try:
                preferences_window.grab_set()
            except Exception as e:
                print(f"Warning: Could not make preferences window modal: {e}")
        except Exception as e:
            print(f"Error opening preferences: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Failed to open preferences: {e}")
    
    def open_timeline(self) -> None:
        """Open timeline dialog."""
        try:
            # Ensure main window is visible and focused
            self.deiconify()
            self.lift()
            self.focus_force()
            
            from src.views.timeline_page import TimelinePage
            
            timeline_window = ctk.CTkToplevel(self)
            timeline_window.title("Custom Break Timeline")
            timeline_window.geometry("800x600")
            timeline_window.transient(self)
            
            # Center the window
            timeline_window.update_idletasks()
            x = (timeline_window.winfo_screenwidth() // 2) - (800 // 2)
            y = (timeline_window.winfo_screenheight() // 2) - (600 // 2)
            timeline_window.geometry(f"800x600+{x}+{y}")
            
            # Make modal after positioning
            try:
                timeline_window.grab_set()
            except Exception as e:
                print(f"Warning: Could not make timeline window modal: {e}")
            
            timeline_page = TimelinePage(timeline_window, self.controller)
            timeline_page.pack(fill="both", expand=True, padx=20, pady=20)
            
        except Exception as e:
            print(f"Error opening timeline: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Failed to open timeline: {e}")
    
    def open_about(self) -> None:
        """Open about dialog."""
        try:
            # Ensure main window is visible and focused
            self.deiconify()
            self.lift()
            self.focus_force()
            
            from src.views.about_page import AboutPage
            
            about_window = ctk.CTkToplevel(self)
            about_window.title("About Break Assistant")
            about_window.geometry("500x400")
            about_window.transient(self)
            
            # Center the window
            about_window.update_idletasks()
            x = (about_window.winfo_screenwidth() // 2) - (500 // 2)
            y = (about_window.winfo_screenheight() // 2) - (400 // 2)
            about_window.geometry(f"500x400+{x}+{y}")
            
            # Make modal after positioning
            try:
                about_window.grab_set()
            except Exception as e:
                print(f"Warning: Could not make about window modal: {e}")
            
            about_page = AboutPage(about_window, self.controller)
            about_page.pack(fill="both", expand=True, padx=20, pady=20)
            
        except Exception as e:
            print(f"Error opening about: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Failed to open about: {e}")
    
    def minimize_to_tray(self) -> None:
        """Minimize window to system tray."""
        self.withdraw()
        # Tray functionality would be implemented here
    
    def restore_from_tray(self) -> None:
        """Restore window from system tray."""
        self.deiconify()
        self.lift()
        self.focus_force() 

    def open_help(self) -> None:
        """Open help dialog."""
        try:
            self.deiconify()
            self.lift()
            self.focus_force()
            from src.views.help_page import HelpPage
            help_window = ctk.CTkToplevel(self)
            help_window.title("Help & Support")
            help_window.geometry("600x600")
            help_window.transient(self)
            help_window.update_idletasks()
            x = (help_window.winfo_screenwidth() // 2) - (600 // 2)
            y = (help_window.winfo_screenheight() // 2) - (600 // 2)
            help_window.geometry(f"600x600+{x}+{y}")
            try:
                help_window.grab_set()
            except Exception as e:
                print(f"Warning: Could not make help window modal: {e}")
            help_page = HelpPage(help_window, self.controller)
            help_page.pack(fill="both", expand=True, padx=20, pady=20)
        except Exception as e:
            print(f"Error opening help: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Failed to open help: {e}")

    def new_file(self):
        import tkinter.messagebox as messagebox
        messagebox.showinfo("New File", "New file functionality coming soon.")

    def open_file(self):
        import tkinter.messagebox as messagebox
        messagebox.showinfo("Open File", "Open file functionality coming soon.")

    def save_file(self):
        import tkinter.messagebox as messagebox
        messagebox.showinfo("Save File", "Save file functionality coming soon.")