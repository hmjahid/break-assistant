# Break Assistant

A world-class cross-platform break reminder application designed to help users maintain healthy work habits through smart break scheduling and customizable notifications.

## 🌟 Features

### Core Functionality
- **Smart Break Scheduling**: Custom timeline-based break scheduling with repeat patterns
- **Manual Break Duration**: Set custom break duration (default: 15 minutes)
- **Customizable Intervals**: Set work duration (default: 20 minutes) and break duration (default: 1 minute)
- **Snooze & Skip**: Flexible break management with snooze and skip options
- **Sound Alerts**: Customizable notification sounds for break reminders
- **Theme Support**: Light, Dark, and System theme options
- **Progress Visualization**: Real-time progress bars and visual indicators
- **Settings Persistence**: Automatic saving of user preferences and timeline
- **Break Popup**: Enhanced break notification with countdown and next break time

### Advanced Timeline Management
- **Multiple Break Slots**: Define unlimited break times throughout the day
- **Repeat Patterns**: Daily, weekdays, weekends, or one-time breaks
- **Overlap Prevention**: Intelligent validation prevents conflicting break times
- **Visual Timeline**: Easy-to-use interface for managing break schedules
- **Real-time Monitoring**: Continuous monitoring of upcoming breaks

### Cross-Platform Support
- **Linux**: Native support with AppImage packaging
- **Windows**: Executable and installer packages
- **macOS**: DMG installer with code signing

## 🚀 Quick Start

### Installation

#### Linux (AppImage)
```bash
# Download and run AppImage
chmod +x Break-Assistant-1.0.0-x86_64.AppImage
./Break-Assistant-1.0.0-x86_64.AppImage
```

#### From Source
```bash
# Clone repository
git clone https://github.com/break-assistant/break-assistant.git
cd break-assistant

# Install dependencies
pip install -r requirements.txt

# Run application
python src/main.py
```

### Basic Usage

1. **Launch the Application**
   - Start Break Assistant from your applications menu or command line

2. **Set Up Your Timeline**
   - Click "Timeline" to open the timeline manager
   - Add break slots with your preferred times
   - Set duration and repeat patterns
   - Save your timeline

3. **Configure Settings**
   - Click "Settings" to customize the application
   - Choose your preferred theme
   - Enable/disable sound notifications
   - Adjust timer settings

4. **Start Monitoring**
   - The application will automatically monitor your timeline
   - Receive notifications when breaks are due
   - Use snooze or skip options as needed

## 📋 Requirements

### System Requirements
- **OS**: Linux, Windows 10+, macOS 10.14+
- **Python**: 3.8 or higher
- **RAM**: 50MB minimum
- **Storage**: 10MB available space

### Dependencies
- **CustomTkinter**: Modern UI framework
- **Pygame**: Audio playback
- **Pillow**: Image processing
- **PyInstaller**: Application packaging

## 🛠️ Development

### Project Structure
```
break-assistant/
├── src/                    # Source code
│   ├── controllers/        # Application controllers
│   ├── models/            # Data models
│   ├── views/             # UI components
│   ├── utils/             # Utility modules
│   ├── audio/             # Audio resources
│   ├── settings_page.py   # Settings page
│   └── main.py            # Application entry point
├── tests/                 # Test suite
├── docs/                  # Documentation
├── resources/             # Assets and resources
├── build_appimage/        # AppImage build files
├── build_all_linux.py     # Linux build system
├── build_appimage.py      # Linux AppImage
├── build_deb.py           # Linux DEB package
├── build_rpm_final.py     # Linux RPM package
├── build_windows.py       # Windows executable/MSI
├── build_macos.py         # macOS app bundle/DMG
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
└── setup.py               # Package setup
```

### Development Setup
```bash
# Clone repository
git clone https://github.com/hmjahid/break-assistant.git
cd break-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Run tests
pytest

# Run application
python src/main.py
```

### Building Packages

#### All Linux Packages (Recommended)
```bash
# Build all Linux package types (AppImage, DEB, RPM)
python build_all_linux.py
```

#### Individual Package Types

##### Linux AppImage
```bash
python build_appimage.py
```

##### Linux DEB Package
```bash
python build_deb.py
```

##### Linux RPM Package
```bash
python build_rpm_final.py
```

##### Windows Executable & Installer
```bash
python build_windows.py
```

##### macOS App Bundle & DMG
```bash
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

#### Installation Commands

**Linux:**
```bash
# AppImage
chmod +x Break-Assistant-1.0.0-x86_64.AppImage
./Break-Assistant-1.0.0-x86_64.AppImage

# DEB package
sudo dpkg -i break-assistant_1.0.0_amd64.deb

# RPM package
sudo rpm -i break-assistant-1.0.0-1.fc41.noarch.rpm
```

**Windows:**
```bash
# Executable
Break-Assistant-1.0.0.exe

# MSI Installer
msiexec /i Break-Assistant-1.0.0.msi
```

**macOS:**
```bash
# App Bundle
# Drag 'Break Assistant.app' to Applications folder

# DMG Installer
# Double-click Break-Assistant-1.0.0.dmg
```

## 🧪 Testing

### Run All Tests
```bash
pytest --cov=src --cov-report=html
```

### Test Categories
- **Unit Tests**: `pytest -m unit`
- **Integration Tests**: `pytest -m integration`
- **UI Tests**: `pytest -m ui`

### Coverage Report
```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html  # View report
```

## 📖 Documentation

- **[User Manual](docs/user_manual.md)**: Complete user guide
- **[Developer Guide](docs/developer_guide.md)**: Development documentation
- **[API Reference](docs/api_reference.md)**: Code documentation
- **[Testing Guide](TESTING_GUIDE.md)**: Testing procedures

## 🤝 Contributing

We welcome contributions! Please see our [Developer Guide](docs/developer_guide.md) for development guidelines.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings
- Maintain 85%+ test coverage

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CustomTkinter**: Modern UI framework
- **Pygame**: Audio functionality
- **PyInstaller**: Cross-platform application packaging
- **AppImage**: Linux distribution format
- **cx_Freeze**: Windows MSI installer creation
- **create-dmg**: macOS DMG installer creation

## 📞 Support

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/your-username/break-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/break-assistant/discussions)
- **Documentation**: [Wiki](https://github.com/hmjahid/break-assistant/wiki)

### Reporting Bugs
Please include:
- Operating system and version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

---

**Made with ❤️ for better work-life balance** 