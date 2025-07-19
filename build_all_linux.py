#!/usr/bin/env python3
"""
Build all package types for Break Assistant
"""

import os
import sys
import subprocess
import shutil
import platform
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

def build_appimage():
    """Build AppImage package."""
    print("\n" + "="*50)
    print("Building AppImage...")
    print("="*50)
    
    if not run_command("python build_appimage.py"):
        print("❌ AppImage build failed")
        return False
    
    print("✅ AppImage built successfully")
    return True

def build_deb():
    """Build DEB package."""
    print("\n" + "="*50)
    print("Building DEB package...")
    print("="*50)
    
    if not run_command("python build_deb.py"):
        print("❌ DEB package build failed")
        return False
    
    print("✅ DEB package built successfully")
    return True

def build_rpm():
    """Build RPM package."""
    print("\n" + "="*50)
    print("Building RPM package...")
    print("="*50)
    
    # Create source tarball
    print("Creating source tarball...")
    temp_dir = Path("temp_rpm_build")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    source_dir = temp_dir / "break-assistant-1.0.0"
    source_dir.mkdir()
    
    # Copy source files
    for item in ["src", "requirements.txt", "README.md", "LICENSE", "docs", "break-assistant.png"]:
        if Path(item).exists():
            if Path(item).is_dir():
                shutil.copytree(item, source_dir / item)
            else:
                shutil.copy(item, source_dir / item)
    
    # Create tarball
    if not run_command(f"tar -czf break-assistant-1.0.0.tar.gz -C {temp_dir} break-assistant-1.0.0"):
        print("❌ Failed to create source tarball")
        return False
    
    # Copy to RPM sources
    rpm_sources_dir = os.path.expanduser("~/rpmbuild/SOURCES")
    os.makedirs(rpm_sources_dir, exist_ok=True)
    shutil.copy("break-assistant-1.0.0.tar.gz", rpm_sources_dir)
    print(f"✓ Tarball copied to {rpm_sources_dir}")
    
    # Build RPM
    if not run_command("rpmbuild -bb break-assistant.spec"):
        print("❌ RPM package build failed")
        return False
    
    # Copy RPM to current directory
    rpm_build_dir = os.path.expanduser("~/rpmbuild/RPMS/noarch")
    rpm_file = os.path.join(rpm_build_dir, "break-assistant-1.0.0-1.fc41.noarch.rpm")
    
    if os.path.exists(rpm_file):
        current_dir = os.getcwd()
        print(f"Current directory: {current_dir}")
        shutil.copy(rpm_file, current_dir)
        print(f"✅ RPM package copied to: {current_dir}")
        return True
    else:
        print(f"❌ RPM package file not found at: {rpm_file}")
        return False

def build_windows():
    """Build Windows packages."""
    print("\n" + "="*50)
    print("Building Windows packages...")
    print("="*50)
    
    if not run_command("python build_windows.py"):
        print("❌ Windows build failed")
        return False
    
    print("✅ Windows packages built successfully")
    return True

def build_macos():
    """Build macOS packages."""
    print("\n" + "="*50)
    print("Building macOS packages...")
    print("="*50)
    
    if not run_command("python build_macos.py"):
        print("❌ macOS build failed")
        return False
    
    print("✅ macOS packages built successfully")
    return True

def main():
    """Main function."""
    print("Building all Break Assistant packages...")
    
    # Check if we're in the right directory
    if not Path("src/main.py").exists():
        print("Error: src/main.py not found. Please run from the project root.")
        return 1
    
    success_count = 0
    total_count = 0
    
    # Build AppImage
    total_count += 1
    if build_appimage():
        success_count += 1
    
    # Build DEB
    total_count += 1
    if build_deb():
        success_count += 1
    
    # Build RPM
    total_count += 1
    if build_rpm():
        success_count += 1
    
    # Build Windows (if on Windows)
    if platform.system() == "Windows":
        total_count += 1
        if build_windows():
            success_count += 1
    
    # Build macOS (if on macOS)
    if platform.system() == "Darwin":
        total_count += 1
        if build_macos():
            success_count += 1
    
    # Summary
    print("\n" + "="*50)
    print("BUILD SUMMARY")
    print("="*50)
    print(f"Successfully built: {success_count}/{total_count} packages")
    
    if success_count == total_count:
        print("\n🎉 All packages built successfully!")
        print("\nAvailable packages:")
        print("- Break-Assistant-1.0.0-x86_64.AppImage (Linux AppImage)")
        print("- break-assistant_1.0.0_amd64.deb (Debian/Ubuntu)")
        print("- break-assistant-1.0.0-1.fc41.noarch.rpm (Fedora/RHEL)")
        
        if platform.system() == "Windows":
            print("- Break-Assistant-1.0.0.exe (Windows Executable)")
            print("- Break-Assistant-1.0.0.msi (Windows Installer)")
        
        if platform.system() == "Darwin":
            print("- Break Assistant.app (macOS App Bundle)")
            print("- Break-Assistant-1.0.0.dmg (macOS Installer)")
        
        print("\nInstallation commands:")
        print("# AppImage:")
        print("chmod +x Break-Assistant-1.0.0-x86_64.AppImage")
        print("./Break-Assistant-1.0.0-x86_64.AppImage")
        print("\n# DEB package:")
        print("sudo dpkg -i break-assistant_1.0.0_amd64.deb")
        print("\n# RPM package:")
        print("sudo rpm -i break-assistant-1.0.0-1.fc41.noarch.rpm")
        
        if platform.system() == "Windows":
            print("\n# Windows:")
            print("Double-click Break-Assistant-1.0.0.exe")
            print("Or: msiexec /i Break-Assistant-1.0.0.msi")
        
        if platform.system() == "Darwin":
            print("\n# macOS:")
            print("Drag 'Break Assistant.app' to Applications")
            print("Or: Double-click Break-Assistant-1.0.0.dmg")
        
        return 0
    else:
        print(f"\n⚠️  {total_count - success_count} package(s) failed to build")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 