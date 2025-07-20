import sys
import os

# Add the parent directory of src to sys.path
src_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(src_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.controllers.app_controller import AppController

def main() -> None:
    """Application entry point."""
    app = AppController()
    app.run()

if __name__ == "__main__":
    main() 