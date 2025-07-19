import customtkinter as ctk
import platform
import sys

class AboutPage(ctk.CTkFrame):
    """About page view."""
    def __init__(self, master, controller) -> None:
        super().__init__(master)
        self.controller = controller
        self.setup_ui()
        self.bind_all_mousewheel()
        self.master.bind('<Configure>', self._on_resize)
    
    def setup_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.scrollable = ctk.CTkScrollableFrame(self)
        self.scrollable.grid(row=0, column=0, sticky="nsew")
        self.scrollable.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(self.scrollable, text="About Break Assistant", 
                                  font=ctk.CTkFont(size=22, weight="bold"))
        title_label.grid(row=0, column=0, pady=(30, 10), sticky="ew")
        
        # Version info
        version_text = f"Version: 1.0.0\nPlatform: {platform.system()} {platform.release()}\nPython: {sys.version.split()[0]}"
        version_label = ctk.CTkLabel(self.scrollable, text=version_text, 
                                    font=ctk.CTkFont(size=12), 
                                    wraplength=500,
                                    justify="left")
        version_label.grid(row=1, column=0, pady=(0, 20), padx=20, sticky="ew")
        
        # Description
        description_text = """Break Assistant is a productivity tool designed to help you maintain a healthy work-life balance by reminding you to take regular breaks during your work sessions.

The app uses the Pomodoro Technique and customizable timelines to ensure you stay productive while taking care of your well-being."""
        
        description_label = ctk.CTkLabel(self.scrollable, text=description_text, 
                                        font=ctk.CTkFont(size=14), 
                                        wraplength=400,  # Reduced from 500 to 400
                                        justify="left")
        description_label.grid(row=2, column=0, pady=(0, 20), padx=20, sticky="ew")
        
        # Features section
        features_title = ctk.CTkLabel(self.scrollable, text="Features", 
                                     font=ctk.CTkFont(size=16, weight="bold"))
        features_title.grid(row=3, column=0, pady=(0, 5), padx=20, sticky="w")
        
        features_text = """• Smart break scheduling with customizable intervals
• Timeline-based break management  
• Sound and visual notifications
• Modern, responsive interface
• Cross-platform compatibility
• Settings persistence and customization
• Dynamic break popup with timer
• Instant break functionality
• Mouse wheel scrolling support

This application helps you stay productive while ensuring you take regular breaks to maintain your well-being."""
        
        features_label = ctk.CTkLabel(self.scrollable, text=features_text, 
                                     font=ctk.CTkFont(size=13), 
                                     wraplength=400,  # Reduced from 500 to 400
                                     justify="left")
        features_label.grid(row=4, column=0, pady=(0, 20), padx=30, sticky="ew")
        
        # Credits section
        credits_title = ctk.CTkLabel(self.scrollable, text="Credits", 
                                    font=ctk.CTkFont(size=16, weight="bold"))
        credits_title.grid(row=5, column=0, pady=(0, 5), padx=20, sticky="w")
        
        credits_text = """Developed by: Md Jahid Hasan
Email: mdjahidhasan919@gmail.com
GitHub: https://github.com/hmjahid/
Linkedin: https://www.linkedin.com/in/hmjahid/
Website: https://hmjahid.netlify.app/

Built with:
• CustomTkinter for the modern UI
• Python for the backend logic
• AppImage for cross-platform distribution"""
        
        credits_label = ctk.CTkLabel(self.scrollable, text=credits_text, 
                                    font=ctk.CTkFont(size=13), 
                                    wraplength=400,  # Reduced from 500 to 400
                                    justify="left")
        credits_label.grid(row=6, column=0, pady=(0, 20), padx=30, sticky="ew")
        
        # Close button
        close_button = ctk.CTkButton(self.scrollable, text="Close", 
                                    command=self.master.destroy, width=120)
        close_button.grid(row=7, column=0, pady=(10, 30))
    
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
    
    def _on_resize(self, event):
        """Handle window resize events."""
        pass 