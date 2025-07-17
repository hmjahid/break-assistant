#!/usr/bin/env python3
"""
Simple AppImage build script for Break Assistant
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"Success: {result.stdout}")
    return True

def create_appimage():
    """Create an AppImage for Break Assistant."""
    
    # Create build directory
    build_dir = Path("build_appimage")
    build_dir.mkdir(exist_ok=True)
    
    # Create AppDir structure
    appdir = build_dir / "Break-Assistant.AppDir"
    if appdir.exists():
        shutil.rmtree(appdir)
    appdir.mkdir()
    
    # Create desktop file
    desktop_content = """[Desktop Entry]
Name=Break Assistant
Comment=Smart break reminder application
Exec=break-assistant
Icon=break-assistant
Type=Application
Categories=Utility;Office;
"""
    
    with open(appdir / "break-assistant.desktop", "w") as f:
        f.write(desktop_content)
    
    # Build with PyInstaller
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=break-assistant",
        "--distpath", str(appdir),
        "--workpath", str(build_dir / "build"),
        "--specpath", str(build_dir),
        "--hidden-import=src.settings_page",
        "src/main.py"
    ]
    
    if not run_command(" ".join(pyinstaller_cmd)):
        print("PyInstaller build failed")
        return False
    
    # Copy executable to AppDir
    executable = appdir / "break-assistant"
    if not executable.exists():
        print("Executable not found")
        return False
    
    # Create icon (placeholder)
    icon_dir = appdir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps"
    icon_dir.mkdir(parents=True, exist_ok=True)
    
    # --- Removed SVG icon creation code ---
    # Only use user-provided PNG icon

    # Copy PNG icon to AppDir root (required by appimagetool)
    icon_source = "break-assistant.png"
    if os.path.exists(icon_source):
        shutil.copy(icon_source, appdir / "break-assistant.png")
        print("✓ Custom icon copied to AppDir root")
        # Also copy to standard icon directory for desktop integration
        shutil.copy(icon_source, icon_dir / "break-assistant.png")
        print("✓ Custom icon copied to usr/share/icons/hicolor/256x256/apps/")
    else:
        print(f"ERROR: {icon_source} not found. Please provide the icon in the project root.")
        return False

    # Copy src/audio directory to AppDir
    audio_src = Path("src/audio")
    audio_dst = appdir / "resources" / "audio"
    if audio_src.exists():
        shutil.copytree(audio_src, audio_dst, dirs_exist_ok=True)
        print("✓ Audio resources copied to AppDir")
    else:
        print(f"ERROR: {audio_src} not found. Please provide the audio resources.")
        return False
    
    # Create AppRun script
    apprun_content = """#!/bin/bash
cd "$(dirname "$0")"
exec ./break-assistant "$@"
"""
    
    with open(appdir / "AppRun", "w") as f:
        f.write(apprun_content)
    
    # Make AppRun executable
    os.chmod(appdir / "AppRun", 0o755)
    
    # Create AppImage using appimagetool
    print("Creating AppImage...")
    
    # Check if appimagetool is available
    if not shutil.which("appimagetool"):
        print("appimagetool not found. Installing...")
        if not run_command("wget -c 'https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage' -O appimagetool"):
            print("Failed to download appimagetool")
            return False
        os.chmod("appimagetool", 0o755)
        appimagetool = "./appimagetool"
    else:
        appimagetool = "appimagetool"
    
    # Create AppImage
    appimage_cmd = f"{appimagetool} {appdir} Break-Assistant-1.0.0-x86_64.AppImage"
    if not run_command(appimage_cmd):
        print("AppImage creation failed")
        return False
    
    print("AppImage created successfully!")
    print("File: Break-Assistant-1.0.0-x86_64.AppImage")
    
    return True

def main():
    """Main function."""
    print("Building Break Assistant AppImage...")
    
    # Check if we're in the right directory
    if not Path("src/main.py").exists():
        print("Error: src/main.py not found. Please run from the project root.")
        return 1
    
    # Create AppImage
    if create_appimage():
        print("\nBuild completed successfully!")
        print("You can now test the AppImage:")
        print("chmod +x Break-Assistant-1.0.0-x86_64.AppImage")
        print("./Break-Assistant-1.0.0-x86_64.AppImage")
        return 0
    else:
        print("\nBuild failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 