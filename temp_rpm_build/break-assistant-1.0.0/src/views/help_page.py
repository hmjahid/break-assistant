import customtkinter as ctk

class HelpPage(ctk.CTkFrame):
    """Help page view."""
    def __init__(self, master, controller) -> None:
        super().__init__(master)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # Use a scrollable frame for all content
        self.scrollable = ctk.CTkScrollableFrame(self)
        self.scrollable.grid(row=0, column=0, sticky="nsew")
        self.scrollable.grid_columnconfigure(0, weight=1)
        self.bind_all_mousewheel()
        # Title
        title_label = ctk.CTkLabel(self.scrollable, text="Help & Support", font=ctk.CTkFont(size=22, weight="bold"))
        title_label.grid(row=0, column=0, pady=(30, 10), sticky="ew")
        # Usage instructions
        usage = (
            "Break Assistant helps you take regular breaks for better health and productivity.\n\n"
            "- Use the Preferences page to set your work/break intervals, notifications, and appearance.\n"
            "- Use the Timeline page to schedule custom breaks with repeat patterns.\n"
            "- The app will notify you when it's time for a break.\n"
            "- You can snooze or skip breaks as needed.\n"
        )
        usage_label = ctk.CTkLabel(self.scrollable, text=usage, font=ctk.CTkFont(size=14), justify="left", wraplength=500)
        usage_label.grid(row=1, column=0, pady=(0, 20), padx=20, sticky="ew")
        # FAQ
        faq_title = ctk.CTkLabel(self.scrollable, text="Frequently Asked Questions", font=ctk.CTkFont(size=16, weight="bold"))
        faq_title.grid(row=2, column=0, pady=(0, 5), padx=20, sticky="w")
        faq = (
            "Q: How do I change the break sound?\nA: Go to Preferences > Notifications.\n\n"
            "Q: Can I disable notifications?\nA: Yes, in Preferences > Notifications.\n\n"
            "Q: How do I reset all settings?\nA: Use the 'Reset to Defaults' button in Preferences.\n\n"
            "Q: Where are my settings saved?\nA: Settings are saved locally and persist between sessions.\n"
        )
        faq_label = ctk.CTkLabel(self.scrollable, text=faq, font=ctk.CTkFont(size=13), justify="left", wraplength=500)
        faq_label.grid(row=3, column=0, pady=(0, 20), padx=30, sticky="ew")
        # Support
        support_title = ctk.CTkLabel(self.scrollable, text="Support", font=ctk.CTkFont(size=16, weight="bold"))
        support_title.grid(row=4, column=0, pady=(0, 5), padx=20, sticky="w")
        support = (
            "For more help, contact: mdjahidhasan919@gmail.com\n"
            "Visit: https://github.com/hmjahid/break-assistant/ for updates and issues."
        )
        support_label = ctk.CTkLabel(self.scrollable, text=support, font=ctk.CTkFont(size=13), justify="left", wraplength=500, text_color="#3399ff")
        support_label.grid(row=5, column=0, pady=(0, 20), padx=30, sticky="ew")
        # Close button
        close_button = ctk.CTkButton(self.scrollable, text="Close", command=self.master.destroy, width=120)
        close_button.grid(row=6, column=0, pady=(10, 30))

    def bind_all_mousewheel(self):
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
        try:
            if event.num == 4:
                self.scrollable._parent_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.scrollable._parent_canvas.yview_scroll(1, "units")
        except Exception:
            pass 