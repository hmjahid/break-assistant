from typing import Callable, Optional

class Timer:
    """Timer logic for work/break intervals."""
    def __init__(self, duration: int, callback: Optional[Callable[[], None]] = None) -> None:
        self.duration = duration
        self.callback = callback
        self.remaining = duration
        self.running = False

    def start(self) -> None:
        self.running = True

    def stop(self) -> None:
        self.running = False

    def reset(self) -> None:
        self.remaining = self.duration 