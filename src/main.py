import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import src.settings_page
from src.controllers.app_controller import AppController

def main() -> None:
    """Application entry point."""
    app = AppController()
    app.run()

if __name__ == "__main__":
    main() 