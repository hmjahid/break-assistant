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
    """Run a command and return the result, printing full stdout and stderr on failure."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print("\n===== COMMAND FAILED =====")
        print(f"Command: {cmd}")
        print(f"Exit code: {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        print("==========================\n")
        return False
    print(f"Success: {result.stdout}")
    return True

def create_pyinstaller_spec(build_dir):
    """Create PyInstaller spec file dynamically."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../src/audio', 'audio'),
    ],
    hiddenimports=[
        'customtkinter',
        'pygame',
        'PIL',
        'PIL._tkinter_finder',
        'tkinter',
        'tkinter.ttk',
        'threading',
        'json',
        'configparser',
        'pathlib',
        'datetime',
        'time',
        'os',
        'sys',
        'platform',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='break-assistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='break-assistant',
)
'''
    
    spec_file = build_dir / "break-assistant.spec"
    with open(spec_file, "w") as f:
        f.write(spec_content)
    
    print(f"✓ PyInstaller spec file created: {spec_file}")
    return spec_file

def create_appimage():
    """Create an AppImage for Break Assistant."""
    
    # Create build directory
    build_dir = Path("build_appimage")
    build_dir.mkdir(exist_ok=True)
    
    # Create PyInstaller spec file
    spec_file = create_pyinstaller_spec(build_dir)
    
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
    
    # Build with PyInstaller using spec file
    pyinstaller_cmd = [
        "pyinstaller",
        "--distpath", str(appdir),
        "--workpath", str(build_dir / "build"),
        str(spec_file)
    ]
    
    if not run_command(" ".join(pyinstaller_cmd)):
        print("PyInstaller build failed")
        return False
    
    # Copy executable to AppDir root
    pyinstaller_exe = appdir / "break-assistant" / "break-assistant"
    if not pyinstaller_exe.exists():
        print(f"Executable not found: {pyinstaller_exe}")
        return False
    print("✓ PyInstaller executable found in AppDir/break-assistant/break-assistant")
    
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
exec ./break-assistant/break-assistant "$@"
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
        if os.path.exists("appimagetool"):
            print("Using existing appimagetool")
            os.chmod("appimagetool", 0o755)
            appimagetool = "./appimagetool"
        elif not run_command("wget -c 'https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage' -O appimagetool"):
            print("Failed to download appimagetool")
            return False
        else:
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