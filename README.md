# Break Assistant

A world-class cross-platform break reminder application designed to help users maintain healthy work habits through smart break scheduling and customizable notifications.

![Break Assistant](docs/images/break-assistant-screenshot.png)

## 🌟 Features

### Core Functionality
- **Smart Break Scheduling**: Custom timeline-based break scheduling with repeat patterns
- **Customizable Intervals**: Set break duration and frequency to match your workflow
- **Snooze & Skip**: Flexible break management with snooze and skip options
- **Sound Alerts**: Customizable notification sounds for break reminders
- **Theme Support**: Light, Dark, and System theme options
- **Progress Visualization**: Real-time progress bars and visual indicators
- **Settings Persistence**: Automatic saving of user preferences and timeline

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
│   └── utils/             # Utility modules
├── tests/                 # Test suite
├── build/                 # Build scripts
├── docs/                  # Documentation
└── resources/             # Assets and resources
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

#### Linux AppImage
```bash
python build/linux/build_linux.py
```

#### Windows Executable
```bash
python build/windows/build_windows.py
```

#### macOS DMG
```bash
python build/macos/build_macos.py
```

#### All Platforms
```bash
python build/build_all.py
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

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

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
- **PyInstaller**: Application packaging
- **AppImage**: Linux distribution format

## 📞 Support

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/your-username/break-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/break-assistant/discussions)
- **Documentation**: [Wiki](https://github.com/your-username/break-assistant/wiki)

### Reporting Bugs
Please include:
- Operating system and version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

## 🗺️ Roadmap

### Version 1.1
- [ ] Cloud sync for settings and timeline
- [ ] Mobile companion app
- [ ] Advanced analytics and insights
- [ ] Integration with calendar apps

### Version 1.2
- [ ] Team collaboration features
- [ ] Break reminder sharing
- [ ] Advanced notification options
- [ ] Plugin system

### Version 2.0
- [ ] AI-powered break optimization
- [ ] Health tracking integration
- [ ] Cross-device synchronization
- [ ] Enterprise features

---

**Made with ❤️ for better work-life balance** 