#!/usr/bin/env python3
"""
DEB package build script for Break Assistant
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

def create_deb_package():
    """Create a DEB package for Break Assistant."""
    
    # Create build directory
    build_dir = Path("build_deb")
    build_dir.mkdir(exist_ok=True)
    
    # Create package structure
    package_name = "break-assistant"
    package_version = "1.0.0"
    package_dir = build_dir / f"{package_name}-{package_version}"
    
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Create DEBIAN control file
    debian_dir = package_dir / "DEBIAN"
    debian_dir.mkdir()
    
    control_content = f"""Package: {package_name}
Version: {package_version}
Section: utils
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.8), python3-tk, python3-pygame
Maintainer: Break Assistant Team <support@breakassistant.app>
Description: Smart break reminder application
 Break Assistant is a world-class cross-platform break reminder 
 application designed to help users maintain healthy work habits 
 through smart break scheduling and customizable notifications.
 .
 Features:
  * Smart break scheduling with timeline management
  * Customizable work and break durations
  * Sound alerts and theme support
  * Cross-platform compatibility
  * Progress visualization
Homepage: https://github.com/hmjahid/break-assistant
"""
    
    with open(debian_dir / "control", "w") as f:
        f.write(control_content)
    
    # Create desktop file
    applications_dir = package_dir / "usr" / "share" / "applications"
    applications_dir.mkdir(parents=True, exist_ok=True)
    
    desktop_content = """[Desktop Entry]
Name=Break Assistant
Comment=Smart break reminder application
Exec=break-assistant
Icon=break-assistant
Type=Application
Categories=Utility;Office;
"""
    
    with open(applications_dir / "break-assistant.desktop", "w") as f:
        f.write(desktop_content)
    
    # Create icon directory
    icon_dir = package_dir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps"
    icon_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy icon
    icon_source = "break-assistant.png"
    if os.path.exists(icon_source):
        shutil.copy(icon_source, icon_dir / "break-assistant.png")
        print("✓ Icon copied to package")
    else:
        print(f"Warning: {icon_source} not found")
    
    # Create binary directory
    bin_dir = package_dir / "usr" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    
    # Create launcher script
    launcher_content = """#!/bin/bash
cd /usr/share/break-assistant
exec python3 main.py "$@"
"""
    
    with open(bin_dir / "break-assistant", "w") as f:
        f.write(launcher_content)
    
    # Make launcher executable
    os.chmod(bin_dir / "break-assistant", 0o755)
    
    # Create application directory
    app_dir = package_dir / "usr" / "share" / "break-assistant"
    app_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy source files
    src_dir = Path("src")
    if src_dir.exists():
        shutil.copytree(src_dir, app_dir / "src", dirs_exist_ok=True)
        print("✓ Source files copied")
    
    # Ensure audio files are in the correct location for the DEB package
    # The audio manager expects audio files in resources/audio relative to src
    resources_dir = app_dir / "src" / "resources" / "audio"
    resources_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy audio files to the resources directory
    audio_src = Path("src/audio")
    if audio_src.exists():
        for audio_file in audio_src.glob("*"):
            if audio_file.is_file():
                shutil.copy(audio_file, resources_dir / audio_file.name)
                print(f"✓ Audio file copied: {audio_file.name}")
    else:
        print("Warning: src/audio directory not found")
    
    # Copy requirements
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        shutil.copy(requirements_file, app_dir / "requirements.txt")
        print("✓ Requirements file copied")
    
    # Copy README and documentation
    readme_file = Path("README.md")
    if readme_file.exists():
        shutil.copy(readme_file, app_dir / "README.md")
    
    docs_dir = Path("docs")
    if docs_dir.exists():
        shutil.copytree(docs_dir, app_dir / "docs", dirs_exist_ok=True)
        print("✓ Documentation copied")
    
    # Build DEB package
    print("Building DEB package...")
    
    # Check if dpkg-deb is available
    if not shutil.which("dpkg-deb"):
        print("Error: dpkg-deb not found. Please install dpkg-dev package.")
        return False
    
    # Build package
    deb_cmd = f"dpkg-deb --build {package_dir.name}"
    if not run_command(deb_cmd, cwd=build_dir):
        print("DEB package creation failed")
        return False
    
    # Copy package to current directory
    deb_file = build_dir / f"{package_name}-{package_version}.deb"
    if deb_file.exists():
        current_dir = os.getcwd()
        print(f"Current directory: {current_dir}")
        target_file = f"{package_name}_{package_version}_amd64.deb"
        shutil.copy(str(deb_file), target_file)
        print(f"✓ DEB package copied to: {current_dir}/{target_file}")
        return True
    else:
        print(f"❌ DEB package file not found at: {deb_file}")
        return False

def main():
    """Main function."""
    print("Building Break Assistant DEB package...")
    
    # Check if we're in the right directory
    if not Path("src/main.py").exists():
        print("Error: src/main.py not found. Please run from the project root.")
        return 1
    
    # Create DEB package
    if create_deb_package():
        print("\nDEB package built successfully!")
        print("You can install it with:")
        print("sudo dpkg -i break-assistant_1.0.0_amd64.deb")
        return 0
    else:
        print("\nDEB package build failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 