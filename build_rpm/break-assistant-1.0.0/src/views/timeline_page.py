import customtkinter as ctk
from typing import Optional, List, Callable
from src.models.timeline_manager import TimelineManager, BreakSlot
from datetime import datetime, time
import tkinter.messagebox as messagebox


class TimelinePage(ctk.CTkFrame):
    """Timeline interface for managing custom break schedules."""
    
    def __init__(self, master, controller) -> None:
        print("DEBUG: Entering TimelinePage.__init__")
        super().__init__(master)
        self.controller = controller
        # Use the controller's timeline manager instead of creating a new one
        self.timeline_manager = controller.get_timeline_manager()
        self.selected_slot: Optional[BreakSlot] = None
        self.setup_ui()
        self.bind_all_mousewheel()
        self.refresh_timeline()
    
    def bind_all_mousewheel(self):
        # Windows/macOS
        self.scrollable.bind_all("<MouseWheel>", self._on_mousewheel)
        # Linux
        self.scrollable.bind_all("<Button-4>", self._on_mousewheel_linux)
        self.scrollable.bind_all("<Button-5>", self._on_mousewheel_linux)

    def _on_mousewheel(self, event):
        self.scrollable._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_mousewheel_linux(self, event):
        if event.num == 4:
            self.scrollable._parent_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.scrollable._parent_canvas.yview_scroll(1, "units")
    
    def setup_ui(self) -> None:
        """Setup timeline interface."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # Use a scrollable frame for all content
        self.scrollable = ctk.CTkScrollableFrame(self)
        self.scrollable.grid(row=0, column=0, sticky="nsew")
        self.scrollable.grid_columnconfigure(0, weight=1)
        self.scrollable.grid_columnconfigure(1, weight=1)
        self.scrollable.bind_all("<MouseWheel>", self._on_mousewheel)
        # Info section
        info_label = ctk.CTkLabel(self.scrollable, text="Manage your custom break schedule. Add, edit, or delete break slots and set repeat patterns. Validate to avoid overlaps.", font=ctk.CTkFont(size=13), justify="center", wraplength=700, text_color="gray")
        info_label.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky="ew")
        # Title
        title_label = ctk.CTkLabel(self.scrollable, text="Custom Break Timeline", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        # Left panel - Timeline list
        left_frame = ctk.CTkFrame(self.scrollable)
        left_frame.grid(row=2, column=0, padx=(20, 10), pady=20, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)
        # Timeline controls
        controls_frame = ctk.CTkFrame(left_frame)
        controls_frame.grid(row=0, column=0, pady=(0, 10), sticky="ew")
        add_button = ctk.CTkButton(controls_frame, text="Add Break", command=self.show_add_dialog)
        add_button.pack(side="left", padx=(10, 5), pady=10)
        edit_button = ctk.CTkButton(controls_frame, text="Edit", command=self.show_edit_dialog, state="disabled")
        edit_button.pack(side="left", padx=5, pady=10)
        delete_button = ctk.CTkButton(controls_frame, text="Delete", command=self.delete_selected_slot, state="disabled")
        delete_button.pack(side="left", padx=5, pady=10)
        self.edit_button = edit_button
        self.delete_button = delete_button
        # Timeline list
        list_frame = ctk.CTkFrame(left_frame)
        list_frame.grid(row=1, column=0, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        self.timeline_scroll = ctk.CTkScrollableFrame(list_frame)
        self.timeline_scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        # Right panel - Details and validation
        right_frame = ctk.CTkFrame(self.scrollable)
        right_frame.grid(row=2, column=1, padx=(10, 20), pady=20, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        details_label = ctk.CTkLabel(right_frame, text="Break Details", font=ctk.CTkFont(size=16, weight="bold"), wraplength=350)
        details_label.grid(row=0, column=0, pady=(20, 10), sticky="ew")
        self.details_text = ctk.CTkTextbox(right_frame, height=200, wrap="word")
        self.details_text.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        validation_label = ctk.CTkLabel(right_frame, text="Timeline Validation", font=ctk.CTkFont(size=16, weight="bold"), wraplength=350)
        validation_label.grid(row=2, column=0, pady=(20, 10), sticky="ew")
        self.validation_text = ctk.CTkTextbox(right_frame, height=150, wrap="word")
        self.validation_text.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        validate_button = ctk.CTkButton(right_frame, text="Validate Timeline", command=self.validate_timeline)
        validate_button.grid(row=4, column=0, pady=(0, 20))
    
    def refresh_timeline(self) -> None:
        """Refresh the timeline display."""
        # Store the currently selected slot ID
        selected_id = self.selected_slot.id if self.selected_slot else None
        
        # Clear existing items
        for widget in self.timeline_scroll.winfo_children():
            widget.destroy()
        
        # Add timeline items
        for slot in self.timeline_manager.get_all_break_slots():
            self.add_timeline_item(slot)
        
        # Restore selection if it still exists
        if selected_id:
            for slot in self.timeline_manager.get_all_break_slots():
                if slot.id == selected_id:
                    self.select_slot(slot)
                    break
        
        # Update details
        self.update_details()
        self.validate_timeline()
    
    def add_timeline_item(self, slot: BreakSlot) -> None:
        """Add a timeline item to the display.
        
        Args:
            slot: Break slot to display
        """
        item_frame = ctk.CTkFrame(self.timeline_scroll)
        item_frame.pack(fill="x", padx=5, pady=2)
        
        # Time and duration
        time_text = f"{slot.start_time.strftime('%H:%M')} ({slot.duration}min)"
        time_label = ctk.CTkLabel(item_frame, text=time_text, font=ctk.CTkFont(weight="bold"))
        time_label.pack(side="left", padx=10, pady=5)
        
        # Repeat pattern
        pattern_text = f"• {slot.repeat_pattern}"
        pattern_label = ctk.CTkLabel(item_frame, text=pattern_text, text_color="gray")
        pattern_label.pack(side="left", padx=10, pady=5)
        
        # Enabled/disabled indicator
        status_text = "✓" if slot.enabled else "✗"
        status_color = "green" if slot.enabled else "red"
        status_label = ctk.CTkLabel(item_frame, text=status_text, text_color=status_color)
        status_label.pack(side="right", padx=10, pady=5)
        
        # Message preview
        if slot.message:
            message_label = ctk.CTkLabel(item_frame, text=f"\"{slot.message}\"", 
                                       text_color="blue", font=ctk.CTkFont(size=12))
            message_label.pack(side="left", padx=10, pady=5)
        
        # Make item selectable
        item_frame.bind("<Button-1>", lambda e, s=slot: self.select_slot(s))
        for child in item_frame.winfo_children():
            child.bind("<Button-1>", lambda e, s=slot: self.select_slot(s))
        
        # Mouse hover highlight
        def on_enter(e, frame=item_frame):
            if self.selected_slot != slot:
                frame.configure(fg_color=("lightblue", "darkblue"))
        def on_leave(e, frame=item_frame):
            if self.selected_slot == slot:
                frame.configure(fg_color=("lightgreen", "darkgreen"))
            else:
                frame.configure(fg_color=("gray75", "gray25"))
        item_frame.bind("<Enter>", on_enter)
        item_frame.bind("<Leave>", on_leave)
        for child in item_frame.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)
        # Store reference to slot
        item_frame.slot = slot
    
    def select_slot(self, slot: BreakSlot) -> None:
        """Select a break slot.
        
        Args:
            slot: Break slot to select
        """
        # Deselect previous
        for widget in self.timeline_scroll.winfo_children():
            if hasattr(widget, 'slot'):
                widget.configure(fg_color=("gray75", "gray25"))
        
        # Select new
        for widget in self.timeline_scroll.winfo_children():
            if hasattr(widget, 'slot') and widget.slot == slot:
                widget.configure(fg_color=("lightgreen", "darkgreen"))
                break
        
        self.selected_slot = slot
        self.edit_button.configure(state="normal")
        self.delete_button.configure(state="normal")
        self.update_details()
    
    def update_details(self) -> None:
        """Update the details display."""
        if not self.selected_slot:
            self.details_text.delete("1.0", "end")
            self.details_text.insert("1.0", "Select a break slot to view details.")
            return
        
        slot = self.selected_slot
        details = f"""Break Slot Details:

Time: {slot.start_time.strftime('%H:%M')}
Duration: {slot.duration} minutes
Repeat Pattern: {slot.repeat_pattern}
Status: {'Enabled' if slot.enabled else 'Disabled'}

Message: {slot.message if slot.message else 'No custom message'}

ID: {slot.id}"""
        
        self.details_text.delete("1.0", "end")
        self.details_text.insert("1.0", details)
    
    def show_add_dialog(self) -> None:
        """Show dialog to add a new break slot."""
        dialog = BreakSlotDialog(self, "Add Break Slot", self.add_break_slot)
        dialog.grab_set()  # Make dialog modal
    
    def show_edit_dialog(self) -> None:
        """Show dialog to edit the selected break slot."""
        if not self.selected_slot:
            return
        
        dialog = BreakSlotDialog(self, "Edit Break Slot", self.edit_break_slot, self.selected_slot)
        dialog.grab_set()  # Make dialog modal
    
    def add_break_slot(self, start_time: time, duration: int, message: str, repeat_pattern: str) -> None:
        try:
            print(f"DEBUG: Adding break slot: {start_time}, {duration}, {message}, {repeat_pattern}")
            self.timeline_manager.add_break_slot(start_time, duration, message, repeat_pattern)
            self.refresh_timeline()
            if hasattr(self.controller, 'main_window_ref'):
                print("DEBUG: Calling main_window_ref.force_refresh_next_break() after add_break_slot")
                self.controller.main_window_ref.force_refresh_next_break()
        except ValueError as e:
            self.show_error("Error", str(e))
    
    def edit_break_slot(self, start_time: time, duration: int, message: str, repeat_pattern: str) -> None:
        if not self.selected_slot:
            return
        try:
            print(f"DEBUG: Editing break slot: {self.selected_slot.id}, {start_time}, {duration}, {message}, {repeat_pattern}")
            self.timeline_manager.edit_break_slot(
                self.selected_slot.id,
                start_time=start_time,
                duration=duration,
                message=message,
                repeat_pattern=repeat_pattern
            )
            self.refresh_timeline()
            if hasattr(self.controller, 'main_window_ref'):
                print("DEBUG: Calling main_window_ref.force_refresh_next_break() after edit_break_slot")
                self.controller.main_window_ref.force_refresh_next_break()
        except ValueError as e:
            self.show_error("Error", str(e))
    
    def delete_selected_slot(self) -> None:
        if not self.selected_slot:
            return
        result = self.show_confirm("Confirm Delete", f"Are you sure you want to delete the break at {self.selected_slot.start_time.strftime('%H:%M')}?")
        if result:
            print(f"DEBUG: Deleting break slot: {self.selected_slot.id}")
            self.timeline_manager.delete_break_slot(self.selected_slot.id)
            self.selected_slot = None
            self.edit_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")
            self.refresh_timeline()
            if hasattr(self.controller, 'main_window_ref'):
                print("DEBUG: Calling main_window_ref.force_refresh_next_break() after delete_selected_slot")
                self.controller.main_window_ref.force_refresh_next_break()
    
    def validate_timeline(self) -> None:
        """Validate the timeline and display results."""
        errors = self.timeline_manager.validate_timeline()
        
        if not errors:
            self.validation_text.delete("1.0", "end")
            self.validation_text.insert("1.0", "✓ Timeline is valid!\n\nNo issues found.")
        else:
            self.validation_text.delete("1.0", "end")
            self.validation_text.insert("1.0", "✗ Timeline has issues:\n\n")
            for error in errors:
                self.validation_text.insert("end", f"• {error}\n")
    
    def show_error(self, title: str, message: str) -> None:
        """Show error dialog.
        
        Args:
            title: Dialog title
            message: Error message
        """
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()
        
        label = ctk.CTkLabel(dialog, text=message, wraplength=350)
        label.pack(expand=True, fill="both", padx=20, pady=20)
        
        button = ctk.CTkButton(dialog, text="OK", command=dialog.destroy)
        button.pack(pady=(0, 20))
    
    def show_confirm(self, title: str, message: str) -> bool:
        """Show confirmation dialog."""
        result = [False]
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.transient(self)
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        # Make visible first, then grab
        dialog.deiconify()
        dialog.lift()
        dialog.focus_force()
        
        # Try to grab after a short delay to ensure window is visible
        try:
            dialog.after(100, dialog.grab_set)
        except Exception as e:
            print(f"Warning: Could not grab confirmation dialog: {e}")
        
        label = ctk.CTkLabel(dialog, text=message, wraplength=350)
        label.pack(expand=True, fill="both", padx=20, pady=20)
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=(0, 20))
        yes_button = ctk.CTkButton(button_frame, text="Yes", command=lambda: [result.__setitem__(0, True), dialog.destroy()])
        yes_button.pack(side="left", padx=5)
        no_button = ctk.CTkButton(button_frame, text="No", command=dialog.destroy)
        no_button.pack(side="left", padx=5)
        dialog.wait_window()
        return result[0]


class BreakSlotDialog(ctk.CTkToplevel):
    """Dialog for adding/editing break slots."""
    
    def __init__(self, parent, title: str, callback: Callable, slot: Optional[BreakSlot] = None) -> None:
        super().__init__(parent)
        self.title(title)
        self.geometry("500x400")
        self.transient(parent)
        self.callback = callback
        self.slot = slot
        self.setup_ui()
        self.bind_all_mousewheel()
        if slot:
            self.load_slot_data()

    def bind_all_mousewheel(self):
        # Windows/macOS
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
        try:
            if event.num == 4:
                self.scrollable._parent_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.scrollable._parent_canvas.yview_scroll(1, "units")
        except Exception:
            pass

    def setup_ui(self) -> None:
        """Setup dialog interface with vertical scrollable frame."""
        # Create scrollable frame
        self.scrollable = ctk.CTkScrollableFrame(self)
        self.scrollable.pack(fill="both", expand=True)
        self.scrollable.grid_columnconfigure(0, weight=1)
        # self.scrollable.bind_all("<MouseWheel>", self._on_mousewheel) # This line is now handled by bind_all_mousewheel

        # Time selection
        time_frame = ctk.CTkFrame(self.scrollable)
        time_frame.pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkLabel(time_frame, text="Start Time:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        time_input_frame = ctk.CTkFrame(time_frame)
        time_input_frame.pack(fill="x", padx=10, pady=(0, 10))
        # Hour selection
        self.hour_var = ctk.StringVar(value="09")
        hour_label = ctk.CTkLabel(time_input_frame, text="Hour:")
        hour_label.pack(side="left", padx=(0, 5))
        hour_spinbox = ctk.CTkEntry(time_input_frame, textvariable=self.hour_var, width=50)
        hour_spinbox.pack(side="left", padx=(0, 10))
        # Minute selection
        self.minute_var = ctk.StringVar(value="00")
        minute_label = ctk.CTkLabel(time_input_frame, text="Minute:")
        minute_label.pack(side="left", padx=(0, 5))
        minute_spinbox = ctk.CTkEntry(time_input_frame, textvariable=self.minute_var, width=50)
        minute_spinbox.pack(side="left")

        # Duration selection
        duration_frame = ctk.CTkFrame(self.scrollable)
        duration_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(duration_frame, text="Duration (minutes):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.duration_var = ctk.StringVar(value="15")
        duration_spinbox = ctk.CTkEntry(duration_frame, textvariable=self.duration_var, width=100)
        duration_spinbox.pack(anchor="w", padx=10, pady=(0, 10))

        # Repeat pattern selection
        pattern_frame = ctk.CTkFrame(self.scrollable)
        pattern_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(pattern_frame, text="Repeat Pattern:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.pattern_var = ctk.StringVar(value="daily")
        pattern_menu = ctk.CTkOptionMenu(pattern_frame, values=["daily", "weekdays", "weekends", "once"], variable=self.pattern_var)
        pattern_menu.pack(anchor="w", padx=10, pady=(0, 10))

        # Message input
        message_frame = ctk.CTkFrame(self.scrollable)
        message_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(message_frame, text="Custom Message (optional):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.message_text = ctk.CTkTextbox(message_frame, height=80)
        self.message_text.pack(fill="x", padx=10, pady=(0, 10))

        # Buttons
        button_frame = ctk.CTkFrame(self.scrollable)
        button_frame.pack(fill="x", padx=20, pady=20)
        save_button = ctk.CTkButton(button_frame, text="Save", command=self.save_slot)
        save_button.pack(side="right", padx=(5, 0))
        cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side="right")

    def load_slot_data(self) -> None:
        """Load existing slot data into the dialog."""
        if not self.slot:
            return
        
        self.hour_var.set(f"{self.slot.start_time.hour:02d}")
        self.minute_var.set(f"{self.slot.start_time.minute:02d}")
        self.duration_var.set(str(self.slot.duration))
        self.pattern_var.set(self.slot.repeat_pattern)
        self.message_text.delete("1.0", "end")
        self.message_text.insert("1.0", self.slot.message)

    def save_slot(self) -> None:
        """Save the break slot."""
        try:
            # Validate inputs
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            duration = int(self.duration_var.get())
            
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError("Invalid time format")
            
            if duration <= 0 or duration > 120:
                raise ValueError("Duration must be between 1 and 120 minutes")
            
            # Create time object
            start_time = time(hour, minute)
            
            # Get message
            message = self.message_text.get("1.0", "end").strip()
            
            # Get repeat pattern
            repeat_pattern = self.pattern_var.get()
            
            # Call callback
            self.callback(start_time, duration, message, repeat_pattern)
            
            # Close dialog
            self.destroy()
            
        except (ValueError, TypeError) as e:
            # Show error
            error_dialog = ctk.CTkToplevel(self)
            error_dialog.title("Error")
            error_dialog.geometry("300x150")
            error_dialog.transient(self)
            error_dialog.grab_set()
            
            label = ctk.CTkLabel(error_dialog, text=str(e), wraplength=250)
            label.pack(expand=True, fill="both", padx=20, pady=20)
            
            button = ctk.CTkButton(error_dialog, text="OK", command=error_dialog.destroy)
            button.pack(pady=(0, 20)) 