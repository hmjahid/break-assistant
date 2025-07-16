import pytest
from src.models.timer import Timer


class TestTimer:
    """Test cases for Timer model."""

    def test_timer_initialization(self):
        """Test timer initialization with default values."""
        timer = Timer(60)
        assert timer.duration == 60
        assert timer.remaining == 60
        assert not timer.running
        assert timer.callback is None

    def test_timer_with_callback(self):
        """Test timer initialization with callback."""
        callback_called = False

        def callback():
            nonlocal callback_called
            callback_called = True

        timer = Timer(30, callback)
        assert timer.callback == callback

    def test_timer_start(self):
        """Test starting the timer."""
        timer = Timer(60)
        timer.start()
        assert timer.running

    def test_timer_stop(self):
        """Test stopping the timer."""
        timer = Timer(60)
        timer.start()
        timer.stop()
        assert not timer.running

    def test_timer_reset(self):
        """Test resetting the timer."""
        timer = Timer(60)
        timer.remaining = 30
        timer.reset()
        assert timer.remaining == 60 