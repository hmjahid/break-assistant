import customtkinter as ctk
from datetime import datetime, timedelta
import threading
import time

class BreakPopup(ctk.CTkToplevel):
    """Break notification popup."""
    
    def __init__(self, master, controller) -> None:
        super().__init__(master)
        self.controller = controller
        self.title("Break Time!")
        self.geometry("500x500")  # Increased height from 400 to 500
        self.resizable(False, False)
        
        # Make modal but don't grab immediately
        self.transient(master)
        
        # Center the window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)  # Updated for new height
        self.geometry(f"500x500+{x}+{y}")  # Updated height
        
        # Make visible first, then grab
        self.deiconify()
        self.lift()
        self.focus_force()
        
        # Now try to grab after window is visible
        try:
            self.grab_set()
        except Exception as e:
            print(f"Warning: Could not grab popup: {e}")
        
        self.break_slot = None
        self.occurrence_time = None
        self.break_timer_running = False
        self.break_timer_thread = None
        self.break_start_time = None
        self.break_remaining = 0
        
        self.setup_ui()
    
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
        self.break_info_label.pack(pady=20)
        
        # Timer display
        timer_frame = ctk.CTkFrame(main_frame)
        timer_frame.pack(pady=10, fill="x", padx=20)
        
        self.timer_label = ctk.CTkLabel(timer_frame, text="--:--", 
                                       font=ctk.CTkFont(size=32, weight="bold"))
        self.timer_label.pack(pady=10)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(timer_frame)
        self.progress_bar.pack(pady=(0, 10), padx=20, fill="x")
        self.progress_bar.set(0)
        
        # Time details
        time_frame = ctk.CTkFrame(main_frame)
        time_frame.pack(pady=10, fill="x", padx=20)
        
        self.start_time_label = ctk.CTkLabel(time_frame, text="Start: --:--", 
                                           font=ctk.CTkFont(size=12))
        self.start_time_label.pack(pady=5)
        
        self.end_time_label = ctk.CTkLabel(time_frame, text="End: --:--", 
                                         font=ctk.CTkFont(size=12))
        self.end_time_label.pack(pady=5)
        
        # Buttons frame
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=15, fill="x", padx=20)  # Reduced pady from 20 to 15
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        
        # Start break button
        self.start_button = ctk.CTkButton(button_frame, text="Start Break", 
                                         command=self.start_break)
        self.start_button.grid(row=0, column=0, padx=5, pady=8, sticky="ew")  # Reduced pady from 10 to 8
        
        # Stop button
        self.stop_button = ctk.CTkButton(button_frame, text="Stop", 
                                        command=self.stop_break, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5, pady=8, sticky="ew")  # Reduced pady from 10 to 8
        
        # Snooze button
        self.snooze_button = ctk.CTkButton(button_frame, text="Snooze", 
                                          command=self.snooze_break)
        self.snooze_button.grid(row=0, column=2, padx=5, pady=8, sticky="ew")  # Reduced pady from 10 to 8
        
        # OK button
        ok_button = ctk.CTkButton(main_frame, text="OK", command=self.dismiss)
        ok_button.pack(pady=8, padx=20, fill="x")  # Reduced pady from 10 to 8
    
    def set_break_info(self, break_slot, occurrence_time) -> None:
        self.break_slot = break_slot
        self.occurrence_time = occurrence_time
        if break_slot:
            message = getattr(break_slot, 'message', None)
            if message:
                self.break_info_label.configure(
                    text=message
                )
            else:
                self.break_info_label.configure(
                    text=f"Time for your {break_slot.duration}-minute break!"
                )
            self.break_remaining = break_slot.duration * 60
            self.update_timer_display()
            self.after(500, self.auto_start_break)
        else:
            self.break_info_label.configure(text="Time for your break!")
    
    def auto_start_break(self) -> None:
        """Automatically start the break timer when popup opens."""
        if self.break_slot and not self.break_timer_running:
            print("DEBUG: Auto-starting break timer")
            self.start_break()
        else:
            print(f"DEBUG: Cannot auto-start - break_slot: {self.break_slot}, timer_running: {self.break_timer_running}")
    
    def start_break(self) -> None:
        """Start the break timer."""
        if self.break_slot and not self.break_timer_running:
            print("DEBUG: Starting break timer")
            self.break_timer_running = True
            self.break_start_time = datetime.now()
            self.start_button.configure(text="Pause", command=self.pause_break)
            self.stop_button.configure(state="normal")
            
            # Update time labels
            start_time = self.break_start_time.strftime("%H:%M")
            end_time = (self.break_start_time + timedelta(minutes=self.break_slot.duration)).strftime("%H:%M")
            self.start_time_label.configure(text=f"Start: {start_time}")
            self.end_time_label.configure(text=f"End: {end_time}")
            
            # Start timer thread
            self.break_timer_thread = threading.Thread(target=self.break_timer_loop, daemon=True)
            self.break_timer_thread.start()
        else:
            print(f"DEBUG: Cannot start break - break_slot: {self.break_slot}, timer_running: {self.break_timer_running}")
    
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
                if self.break_remaining <= 60 or self.break_remaining % 30 == 0:  # First minute or every 30 seconds
                    print(f"DEBUG: Break timer: {timer_text} remaining ({self.break_remaining} seconds)")
                    
        except Exception as e:
            print(f"DEBUG: Error updating timer display: {e}")
            # Stop the timer if there's an error
            self.break_timer_running = False
    
    def break_finished(self) -> None:
        """Handle break completion."""
        print("DEBUG: Break timer finished")
        self.break_timer_running = False
        self.start_button.configure(text="Start Break", command=self.start_break)
        self.stop_button.configure(state="disabled")
        self.break_info_label.configure(text="Break completed!")
        self.timer_label.configure(text="00:00")
        self.progress_bar.set(1.0)
    
    def dismiss(self) -> None:
        """Dismiss the popup."""
        if self.break_timer_running:
            self.break_timer_running = False
        self.destroy() 