import sys

class PlatformUtils:
    """Platform-specific utilities."""
    @staticmethod
    def get_platform() -> str:
        if sys.platform.startswith("win"):
            return "windows"
        elif sys.platform.startswith("darwin"):
            return "macos"
        elif sys.platform.startswith("linux"):
            return "linux"
        return "unknown" 