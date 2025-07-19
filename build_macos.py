#!/usr/bin/env python3
"""
macOS Build Script for Break Assistant

Creates macOS app bundle and DMG installer packages.
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
    
    # Check if we're on macOS
    if platform.system() != "Darwin":
        print("❌ This script should be run on macOS")
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
    icon_path = Path("resources/icons/icon.icns")
    if not icon_path.exists():
        print("❌ macOS icon not found: resources/icons/icon.icns")
        return False
    
    # Check for create-dmg (optional)
    try:
        result = subprocess.run(["which", "create-dmg"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ create-dmg found")
        else:
            print("⚠️  create-dmg not found. Install with: brew install create-dmg")
            print("   DMG creation will be skipped")
    except FileNotFoundError:
        print("⚠️  create-dmg not found. Install with: brew install create-dmg")
        print("   DMG creation will be skipped")
    
    print("✅ All requirements met")
    return True

def build_app_bundle():
    """Build macOS app bundle using PyInstaller."""
    print("🔨 Building macOS app bundle...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--icon=resources/icons/icon.icns",
        "--name=Break Assistant",
        "--add-data=resources;resources",
        "--hidden-import=customtkinter",
        "--hidden-import=pygame",
        "--hidden-import=PIL",
        "src/main.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ App bundle built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_dmg():
    """Create DMG installer (optional)."""
    print("🔨 Creating DMG installer...")
    
    # Check if create-dmg is available
    try:
        result = subprocess.run(["which", "create-dmg"], capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠️  create-dmg not found. Skipping DMG creation...")
            return False
    except FileNotFoundError:
        print("⚠️  create-dmg not found. Skipping DMG creation...")
        return False
    
    # Create DMG
    app_path = "dist/Break Assistant.app"
    if not os.path.exists(app_path):
        print("❌ App bundle not found")
        return False
    
    dmg_name = "Break-Assistant-1.0.0.dmg"
    
    try:
        cmd = [
            "create-dmg",
            "--volname", "Break Assistant",
            "--window-pos", "200", "120",
            "--window-size", "600", "400",
            "--icon-size", "100",
            "--icon", "Break Assistant.app", "175", "120",
            "--hide-extension", "Break Assistant.app",
            "--app-drop-link", "425", "120",
            dmg_name,
            "dist/"
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ DMG installer created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ DMG creation failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def copy_packages():
    """Copy built packages to current directory."""
    print("📦 Copying packages to current directory...")
    
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    # Copy app bundle
    app_source = "dist/Break Assistant.app"
    if os.path.exists(app_source):
        shutil.copytree(app_source, "Break Assistant.app", dirs_exist_ok=True)
        print("✅ App bundle copied: Break Assistant.app")
    else:
        print("❌ App bundle not found")
        return False
    
    # Copy DMG if it exists
    dmg_source = "Break-Assistant-1.0.0.dmg"
    if os.path.exists(dmg_source):
        shutil.copy(dmg_source, ".")
        print(f"✅ DMG copied: {dmg_source}")
    
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
    spec_file = "Break Assistant.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print("✅ Removed Break Assistant.spec")

def main():
    """Main build process."""
    print("🚀 Starting macOS build process...")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return False
    
    # Build app bundle
    if not build_app_bundle():
        return False
    
    # Try to create DMG (optional)
    create_dmg()
    
    # Copy packages
    if not copy_packages():
        return False
    
    # Cleanup
    cleanup()
    
    print("=" * 50)
    print("✅ macOS build completed successfully!")
    print("\n📦 Generated packages:")
    print("- Break Assistant.app")
    if os.path.exists("Break-Assistant-1.0.0.dmg"):
        print("- Break-Assistant-1.0.0.dmg")
    
    print("\n📋 Installation instructions:")
    print("1. Drag 'Break Assistant.app' to Applications folder")
    print("2. Or install via DMG: Double-click Break-Assistant-1.0.0.dmg")
    print("3. Run from Applications or Spotlight")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 