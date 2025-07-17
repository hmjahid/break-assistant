import sys
try:
    from plyer import notification as plyer_notification
except ImportError:
    plyer_notification = None
import subprocess

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

    @staticmethod
    def show_system_notification(title: str, message: str):
        """Show a system notification in a cross-platform way."""
        if plyer_notification:
            plyer_notification.notify(title=title, message=message, app_name="Break Assistant")
        else:
            platform = PlatformUtils.get_platform()
            if platform == "linux":
                try:
                    subprocess.run(["notify-send", title, message])
                except Exception as e:
                    print(f"Failed to show notification: {e}")
            elif platform == "macos":
                try:
                    subprocess.run(["osascript", "-e", f'display notification "{message}" with title "{title}"'])
                except Exception as e:
                    print(f"Failed to show notification: {e}")
            elif platform == "windows":
                print("System notifications require plyer on Windows.")
            else:
                print("System notifications not supported on this platform.") 