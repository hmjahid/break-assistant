#!/usr/bin/env python3
"""
Windows Build Script for Break Assistant

Creates Windows executable and MSI installer packages.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import platform

def check_requirements():
    """Check if required tools are available."""
    print("🔍 Checking build requirements...")
    
    # Check if we're on Windows
    if platform.system() != "Windows":
        print("❌ This script should be run on Windows")
        return False
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    # Check PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False
    
    # Check if icon exists
    icon_path = Path("resources/icons/icon.ico")
    if not icon_path.exists():
        print("❌ Windows icon not found: resources/icons/icon.ico")
        return False
    
    print("✅ All requirements met")
    return True

def build_executable():
    """Build Windows executable using PyInstaller."""
    print("🔨 Building Windows executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--icon=resources/icons/icon.ico",
        "--name=Break-Assistant",
        "--add-data=resources;resources",
        "--hidden-import=customtkinter",
        "--hidden-import=pygame",
        "--hidden-import=PIL",
        "src/main.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def build_msi():
    """Build MSI installer (optional)."""
    print("🔨 Building MSI installer...")
    
    # Check if cx_Freeze is available
    try:
        import cx_Freeze
        print("✅ cx_Freeze found")
    except ImportError:
        print("⚠️  cx_Freeze not found. Install with: pip install cx_Freeze")
        print("   Skipping MSI build...")
        return False
    
    # Create setup script for cx_Freeze
    setup_content = '''
import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["customtkinter", "pygame", "PIL"],
    "include_files": ["resources/"],
    "excludes": ["tkinter.test", "unittest"],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Break Assistant",
    version="1.0.0",
    description="Smart break reminder application",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/main.py", base=base, icon="resources/icons/icon.ico")]
)
'''
    
    # Write setup script
    with open("setup_windows.py", "w") as f:
        f.write(setup_content)
    
    try:
        # Build MSI
        result = subprocess.run(["python", "setup_windows.py", "bdist_msi"], 
                              check=True, capture_output=True, text=True)
        print("✅ MSI installer built successfully")
        
        # Clean up setup script
        os.remove("setup_windows.py")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ MSI build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def copy_packages():
    """Copy built packages to current directory."""
    print("📦 Copying packages to current directory...")
    
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    # Copy executable
    exe_source = "dist/Break-Assistant.exe"
    if os.path.exists(exe_source):
        shutil.copy(exe_source, "Break-Assistant-1.0.0.exe")
        print("✅ Executable copied: Break-Assistant-1.0.0.exe")
    else:
        print("❌ Executable not found")
        return False
    
    # Copy MSI if it exists
    msi_files = list(Path("dist").glob("*.msi"))
    if msi_files:
        msi_file = msi_files[0]
        shutil.copy(msi_file, "Break-Assistant-1.0.0.msi")
        print(f"✅ MSI copied: Break-Assistant-1.0.0.msi")
    
    return True

def cleanup():
    """Clean up build artifacts."""
    print("🧹 Cleaning up build artifacts...")
    
    # Remove build directories
    for dir_name in ["build", "dist", "__pycache__"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Removed {dir_name}/")
    
    # Remove spec file
    spec_file = "Break-Assistant.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print("✅ Removed Break-Assistant.spec")

def main():
    """Main build process."""
    print("🚀 Starting Windows build process...")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return False
    
    # Build executable
    if not build_executable():
        return False
    
    # Try to build MSI (optional)
    build_msi()
    
    # Copy packages
    if not copy_packages():
        return False
    
    # Cleanup
    cleanup()
    
    print("=" * 50)
    print("✅ Windows build completed successfully!")
    print("\n📦 Generated packages:")
    print("- Break-Assistant-1.0.0.exe")
    if os.path.exists("Break-Assistant-1.0.0.msi"):
        print("- Break-Assistant-1.0.0.msi")
    
    print("\n📋 Installation instructions:")
    print("1. Double-click Break-Assistant-1.0.0.exe to run")
    print("2. Or install via MSI: msiexec /i Break-Assistant-1.0.0.msi")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 