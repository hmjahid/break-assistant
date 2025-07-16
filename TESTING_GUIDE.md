# Break Assistant Testing Guide

This guide covers how to test the Break Assistant application, including unit tests, integration tests, UI tests, and manual testing procedures.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Test Types](#test-types)
3. [Running Tests](#running-tests)
4. [Writing Tests](#writing-tests)
5. [Manual Testing](#manual-testing)
6. [Build Testing](#build-testing)
7. [Performance Testing](#performance-testing)
8. [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"
```

### Run All Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest -m unit
pytest -m integration
pytest -m ui
```

## Test Types

### 1. Unit Tests (`tests/unit/`)

Test individual components in isolation:

- **`test_timer.py`**: Timer model functionality
- **`test_settings.py`**: Settings management
- **`test_timeline_manager.py`**: Timeline and break slot management

### 2. Integration Tests (`tests/integration/`)

Test component interactions:

- **`test_app_controller.py`**: Application controller integration
- **`test_timeline_integration.py`**: Timeline with other components

### 3. UI Tests (`tests/ui/`)

Test user interface components:

- **`test_main_window.py`**: Main window functionality
- **`test_timeline_ui.py`**: Timeline interface components

## Running Tests

### Basic Test Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_timer.py

# Run specific test function
pytest tests/unit/test_timer.py::TestTimer::test_timer_initialization

# Run tests with coverage
pytest --cov=src --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=src --cov-report=html
```

### Test Categories

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# UI tests only
pytest -m ui

# Run all except UI tests (faster)
pytest -m "not ui"
```

### Test Configuration

```bash
# Run tests in parallel (faster)
pytest -n auto

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Run tests with specific markers
pytest -m "slow or critical"
```

## Writing Tests

### Test Structure

```python
import pytest
from src.models.timer import Timer

class TestTimer:
    """Test cases for Timer model."""
    
    def test_timer_initialization(self):
        """Test timer initialization."""
        timer = Timer(60)
        assert timer.duration == 60
        assert timer.remaining == 60
        assert not timer.running
    
    def test_timer_start(self):
        """Test starting the timer."""
        timer = Timer(60)
        timer.start()
        assert timer.running
```

### Using Fixtures

```python
@pytest.fixture
def sample_timer():
    """Create a sample timer for testing."""
    return Timer(60)

def test_timer_with_fixture(sample_timer):
    """Test using fixture."""
    assert sample_timer.duration == 60
```

### Testing Exceptions

```python
def test_invalid_duration():
    """Test that invalid duration raises exception."""
    with pytest.raises(ValueError, match="Duration must be positive"):
        Timer(-10)
```

### Mocking External Dependencies

```python
from unittest.mock import patch

def test_audio_playback():
    """Test audio playback with mocked pygame."""
    with patch('pygame.mixer.Sound') as mock_sound:
        audio_manager = AudioManager()
        audio_manager.play_sound("test.wav")
        mock_sound.assert_called_once()
```

## Manual Testing

### 1. Application Launch

```bash
# Run the application
python src/main.py

# Test basic functionality
# - Window should open
# - Timer should be visible
# - Settings button should work
# - Timeline button should work
```

### 2. Timeline Testing

1. **Open Timeline**:
   - Click "Timeline" button
   - Timeline window should open

2. **Add Break Slot**:
   - Click "Add Break"
   - Set time (e.g., 10:30 AM)
   - Set duration (e.g., 15 minutes)
   - Set repeat pattern (daily)
   - Add custom message
   - Click "Save"

3. **Edit Break Slot**:
   - Select a break slot
   - Click "Edit"
   - Modify time, duration, or message
   - Save changes

4. **Delete Break Slot**:
   - Select a break slot
   - Click "Delete"
   - Confirm deletion

5. **Validation Testing**:
   - Try to add overlapping slots
   - Try invalid durations (0 or >120 minutes)
   - Try invalid repeat patterns

### 3. Settings Testing

1. **Open Settings**:
   - Click "Settings" button
   - Settings window should open

2. **Test Theme Switching**:
   - Switch between Light, Dark, System themes
   - Verify UI changes

3. **Test Sound Settings**:
   - Enable/disable sound
   - Change sound file
   - Test sound playback

4. **Test Timer Settings**:
   - Change break interval
   - Change break duration
   - Change break type

### 4. Timer Testing

1. **Basic Timer**:
   - Click "Start"
   - Timer should count down
   - Progress bar should update
   - Click "Stop" to pause
   - Click "Reset" to reset

2. **Break Notifications**:
   - Set a break for 1 minute from now
   - Wait for notification
   - Test snooze functionality
   - Test skip functionality

### 5. Cross-Platform Testing

Test on different platforms:

```bash
# Linux
python src/main.py

# Windows (if available)
python src/main.py

# macOS (if available)
python src/main.py
```

## Build Testing

### 1. Test Build Scripts

```bash
# Test Windows build
python build/windows/build_windows.py

# Test Linux build
python build/linux/build_linux.py

# Test macOS build
python build/macos/build_macos.py

# Test all platforms
python build/build_all.py
```

### 2. Test Package Creation

```bash
# Test PyInstaller
pyinstaller --onefile --windowed src/main.py

# Test package installation
pip install -e .

# Test application entry point
break-assistant
```

### 3. Test Dependencies

```bash
# Check all dependencies are available
python -c "import customtkinter; import pygame; import PIL"

# Test with minimal dependencies
pip install --no-deps .
```

## Performance Testing

### 1. Startup Time

```bash
# Measure startup time
time python src/main.py

# Target: < 2 seconds
```

### 2. Memory Usage

```bash
# Monitor memory usage
python -m memory_profiler src/main.py

# Target: < 50MB RAM
```

### 3. CPU Usage

```bash
# Monitor CPU usage
top -p $(pgrep -f "python src/main.py")

# Target: < 1% CPU when idle
```

### 4. Battery Impact

```bash
# Monitor battery usage (macOS)
pmset -g batt

# Monitor power consumption (Linux)
powerstat -d 1
```

## Test Coverage

### Coverage Goals

- **Unit Tests**: 90%+ coverage
- **Integration Tests**: 80%+ coverage
- **UI Tests**: 70%+ coverage
- **Overall**: 85%+ coverage

### Generate Coverage Report

```bash
# Generate HTML report
pytest --cov=src --cov-report=html

# Open report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Coverage Analysis

```bash
# Check coverage for specific modules
pytest --cov=src.models --cov-report=term-missing

# Check uncovered lines
pytest --cov=src --cov-report=term-missing | grep "Missing"
```

## Continuous Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -e ".[dev]"
      - run: pytest --cov=src --cov-report=xml
      - run: pytest -m "not ui"  # Skip UI tests in CI
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   # Check Python path
   python -c "import sys; print(sys.path)"
   
   # Reinstall in development mode
   pip install -e .
   ```

2. **Test Failures**:
   ```bash
   # Run with verbose output
   pytest -v
   
   # Run specific failing test
   pytest tests/unit/test_timer.py::TestTimer::test_timer_initialization -v
   ```

3. **UI Test Issues**:
   ```bash
   # Skip UI tests if no display
   pytest -m "not ui"
   
   # Run with virtual display (Linux)
   xvfb-run pytest -m ui
   ```

4. **Coverage Issues**:
   ```bash
   # Clean coverage data
   coverage erase
   
   # Run tests with coverage
   pytest --cov=src
   ```

### Debug Mode

```bash
# Run with debug output
pytest -v --tb=long

# Run with print statements
pytest -s

# Run with pdb debugger
pytest --pdb
```

### Performance Debugging

```bash
# Profile test execution
pytest --durations=10

# Profile specific test
python -m cProfile -o profile.prof -m pytest tests/unit/test_timer.py
```

## Best Practices

### 1. Test Organization

- Group related tests in classes
- Use descriptive test names
- Add docstrings to test functions
- Use fixtures for common setup

### 2. Test Data

- Use realistic test data
- Test edge cases and error conditions
- Use factories for complex objects
- Clean up test data after tests

### 3. Test Isolation

- Each test should be independent
- Don't rely on test execution order
- Use temporary files and directories
- Mock external dependencies

### 4. Test Maintenance

- Keep tests up to date with code changes
- Refactor tests when code is refactored
- Remove obsolete tests
- Update test documentation

### 5. Test Documentation

- Document test purpose and scope
- Explain complex test scenarios
- Document test data requirements
- Keep testing guide updated

## Advanced Testing

### 1. Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(st.integers(min_value=1, max_value=120))
def test_timer_duration_property(duration):
    """Test timer with various durations."""
    timer = Timer(duration)
    assert timer.duration == duration
    assert timer.remaining == duration
```

### 2. Mutation Testing

```bash
# Install mutmut
pip install mutmut

# Run mutation testing
mutmut run

# Show mutations
mutmut results
```

### 3. Fuzz Testing

```python
import random

def test_timeline_fuzz():
    """Fuzz test timeline with random data."""
    timeline = TimelineManager()
    
    for _ in range(100):
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        duration = random.randint(1, 120)
        
        try:
            timeline.add_break_slot(time(hour, minute), duration)
        except ValueError:
            # Expected for invalid combinations
            pass
```

---

*For more information, see the [Developer Guide](docs/developer_guide.md) and [API Reference](docs/api_reference.md).* 