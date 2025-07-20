# Break Assistant Developer Guide

## Table of Contents

1. [Development Setup](#development-setup)
2. [Project Architecture](#project-architecture)
3. [Code Standards](#code-standards)
4. [Testing Guidelines](#testing-guidelines)
5. [Building and Packaging](#building-and-packaging)
6. [Contributing Guidelines](#contributing-guidelines)
7. [API Reference](#api-reference)

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Environment Setup

```bash
# Clone the repository
git clone https://github.com/break-assistant/break-assistant.git
cd break-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"
```

### IDE Configuration

#### VS Code
Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"]
}
```

#### PyCharm
- Set project interpreter to virtual environment
- Configure code style to PEP 8
- Enable type checking with mypy

## Project Architecture

### MVC Pattern

Break Assistant follows the Model-View-Controller pattern:

```
src/
├── models/          # Data and business logic
├── views/           # UI components
├── controllers/     # Application coordination
└── utils/           # Shared utilities
```

### Key Components

#### Models (`src/models/`)
- **SettingsManager**: Configuration persistence
- **Timer**: Timer logic and state management
- **BreakManager**: Break scheduling and logic

#### Views (`src/views/`)
- **MainWindow**: Primary application interface
- **SettingsPage**: Configuration interface
- **AboutPage**: Application information
- **BreakPopup**: Break notifications

#### Controllers (`src/controllers/`)
- **AppController**: Main application coordination
- **TimerController**: Timer state management

#### Utils (`src/utils/`)
- **AudioManager**: Sound playback
- **ThemeManager**: UI theming
- **PlatformUtils**: Cross-platform utilities

### Data Flow

1. **User Action** → View
2. **View** → Controller
3. **Controller** → Model
4. **Model** → Controller (state change)
5. **Controller** → View (UI update)

## Code Standards

### Python Style Guide

We follow PEP 8 with these tools:

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Additional linting
pylint src/
```

### Type Hints

All functions must include type hints:

```python
from typing import Optional, List, Dict, Any

def process_data(data: List[str], config: Optional[Dict[str, Any]] = None) -> bool:
    """Process the given data with optional configuration."""
    pass
```

### Documentation

#### Docstrings
Use Google-style docstrings:

```python
def calculate_timer_remaining(duration: int, elapsed: int) -> int:
    """Calculate remaining time for a timer.
    
    Args:
        duration: Total duration in seconds
        elapsed: Elapsed time in seconds
        
    Returns:
        Remaining time in seconds
        
    Raises:
        ValueError: If elapsed time exceeds duration
    """
    if elapsed > duration:
        raise ValueError("Elapsed time cannot exceed duration")
    return duration - elapsed
```

#### Comments
- Use comments for complex logic
- Explain "why" not "what"
- Keep comments up to date

### Error Handling

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def safe_operation() -> Optional[str]:
    """Perform operation with proper error handling."""
    try:
        result = perform_operation()
        return result
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return None
    except Exception as e:
        logger.exception("Unexpected error during operation")
        return None
```

## Testing Guidelines

### Test Structure

```
tests/
├── unit/           # Unit tests for models and utilities
├── integration/    # Integration tests for controllers
└── ui/            # UI tests for views
```

### Writing Tests

#### Unit Tests
```python
import pytest
from src.models.timer import Timer

class TestTimer:
    def test_timer_initialization(self):
        """Test timer initialization."""
        timer = Timer(60)
        assert timer.duration == 60
        assert timer.remaining == 60
        assert not timer.running
```

#### Integration Tests
```python
import pytest
from src.controllers.app_controller import AppController

class TestAppController:
    def test_app_initialization(self):
        """Test app controller initialization."""
        controller = AppController()
        assert controller is not None
        assert hasattr(controller, 'main_window')
```

#### UI Tests
```python
import pytest
import customtkinter as ctk
from src.views.main_window import MainWindow

class TestMainWindow:
    def test_window_creation(self):
        """Test main window creation."""
        controller = None  # Mock controller
        window = MainWindow(controller)
        assert isinstance(window, ctk.CTk)
        assert window.title() == "Break Assistant"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest -m unit
pytest -m integration
pytest -m ui

# Run specific test file
pytest tests/unit/test_timer.py
```

### Test Coverage

- Minimum 90% code coverage
- 100% coverage for critical paths
- Mock external dependencies
- Test edge cases and error conditions

## Building and Packaging

### Development Build

```bash
# Install in development mode
pip install -e .

# Run application
python src/main.py
```

### Production Build

#### All Linux Packages (Recommended)
```bash
# Build all Linux package types (AppImage, DEB, RPM)
python build_all_linux.py
```

#### Individual Package Types

##### Linux AppImage
```bash
# Create AppImage
python build_appimage.py
```

##### Linux DEB Package
```bash
# Create Debian package
python build_deb.py
```

##### Linux RPM Package
```bash
# Create RPM package
python build_rpm_final.py
```

##### Windows Executable & Installer
```bash
# Create Windows packages
python build_windows.py
```

##### macOS App Bundle & DMG
```bash
# Create macOS packages
python build_macos.py
```

#### Package Output
All built packages are automatically copied to the current directory:

**Linux Packages:**
- **AppImage**: `Break-Assistant-1.0.0-x86_64.AppImage`
- **DEB**: `break-assistant_1.0.0_amd64.deb`
- **RPM**: `break-assistant-1.0.0-1.fc41.noarch.rpm`

**Windows Packages:**
- **Executable**: `Break-Assistant-1.0.0.exe`
- **Installer**: `Break-Assistant-1.0.0.msi` (requires cx_Freeze)

**macOS Packages:**
- **App Bundle**: `Break Assistant.app`
- **DMG**: `Break-Assistant-1.0.0.dmg` (requires create-dmg)

#### Build Features
- **Automatic Package Copying**: All packages copied to current directory
- **Enhanced Logging**: Detailed build progress and copy locations
- **Error Handling**: Comprehensive error reporting with file paths
- **Dependency Management**: Automatic tool detection and installation
- **Cross-Platform Support**: Windows, macOS, and Linux builds
- **Platform Detection**: Automatic platform-specific builds

#### Build Requirements

**Windows Requirements:**
- Windows 10+ operating system
- Python 3.8+
- PyInstaller: `pip install pyinstaller`
- cx_Freeze (optional): `pip install cx_Freeze`
- Windows icon: `resources/icons/icon.ico`

**macOS Requirements:**
- macOS 10.14+ operating system
- Python 3.8+
- PyInstaller: `pip install pyinstaller`
- create-dmg (optional): `brew install create-dmg`
- macOS icon: `resources/icons/icon.icns`

**Linux Requirements:**
- Linux distribution (Ubuntu, Fedora, etc.)
- Python 3.8+
- PyInstaller: `pip install pyinstaller`
- rpmbuild (for RPM): `sudo dnf install rpm-build`
- dpkg-deb (for DEB): `sudo apt install dpkg-dev`

### CI/CD Pipeline

The project uses GitHub Actions for automated testing and building:

```yaml
# .github/workflows/ci.yml
name: CI

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
      - run: pytest --cov=src
      - run: black --check src/ tests/
      - run: flake8 src/ tests/
      - run: mypy src/
```

## Contributing Guidelines

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Commit** with clear messages
6. **Push** to your fork
7. **Submit** a pull request

### Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat(timer): add snooze functionality`
- `fix(settings): resolve configuration loading issue`
- `docs(readme): update installation instructions`

### Pull Request Process

1. **Title**: Clear, descriptive title
2. **Description**: Detailed explanation of changes
3. **Testing**: Include test cases
4. **Documentation**: Update relevant docs
5. **Screenshots**: For UI changes

### Code Review

All changes require review:

- **Functionality**: Does it work as expected?
- **Code Quality**: Follows style guidelines?
- **Testing**: Adequate test coverage?
- **Documentation**: Updated appropriately?
- **Performance**: No performance regressions?

## API Reference

### Models

#### SettingsManager
```python
class SettingsManager:
    def load(self) -> None:
        """Load settings from file."""
        
    def save(self) -> None:
        """Save settings to file."""
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value."""
        
    def set(self, key: str, value: Any) -> None:
        """Set setting value."""
```

#### Timer
```python
class Timer:
    def __init__(self, duration: int, callback: Optional[Callable] = None):
        """Initialize timer with duration and optional callback."""
        
    def start(self) -> None:
        """Start the timer."""
        
    def stop(self) -> None:
        """Stop the timer."""
        
    def reset(self) -> None:
        """Reset timer to initial duration."""
```

### Controllers

#### AppController
```python
class AppController:
    def __init__(self):
        """Initialize application controller."""
        
    def run(self) -> None:
        """Start the application."""
        
    def quit(self) -> None:
        """Quit the application."""
```

### Utils

#### AudioManager
```python
class AudioManager:
    def play_sound(self, file_path: str) -> None:
        """Play sound from file."""
        
    def stop_sound(self) -> None:
        """Stop currently playing sound."""
```

#### ThemeManager
```python
class ThemeManager:
    def apply_theme(self, theme_name: str) -> None:
        """Apply theme by name."""
        
    def get_available_themes(self) -> List[str]:
        """Get list of available themes."""
```

## Performance Guidelines

### Memory Management
- Use weak references for callbacks
- Clean up resources in destructors
- Avoid circular references

### CPU Optimization
- Use efficient data structures
- Minimize UI updates
- Profile performance-critical code

### Battery Impact
- Minimize background processing
- Use efficient timers
- Optimize for mobile devices

## Security Considerations

### Input Validation
- Validate all user inputs
- Sanitize file paths
- Check file permissions

### File Operations
- Use secure file handling
- Validate file types
- Implement proper error handling

### Network Operations
- Use HTTPS for downloads
- Validate SSL certificates
- Implement timeout handling

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall in development mode
pip install -e .
```

#### Test Failures
```bash
# Run tests with verbose output
pytest -v

# Run specific failing test
pytest tests/unit/test_timer.py::TestTimer::test_timer_initialization -v
```

#### Build Issues
```bash
# Clean build artifacts
rm -rf build/ dist/ *.egg-info/

# Reinstall dependencies
pip install -r requirements.txt
```

### Debugging

#### Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

#### Profiling
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
# Your code here
profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats()
```

---

*Last updated: Version 1.0.0* 

## Settings Application
- The 'Always on Top' setting is now applied to the main window immediately after it is created in AppController, ensuring persistence across restarts.

## Break Popup Thread Safety
- All UI updates in the break popup are now guarded with winfo_exists() checks to prevent TclError if the popup is closed while the timer thread is running. 