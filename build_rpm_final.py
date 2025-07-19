#!/usr/bin/env python3
"""
Final RPM package build script for Break Assistant
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

def create_rpm_package():
    """Create an RPM package for Break Assistant."""
    
    # Create source tarball
    print("Creating source tarball...")
    
    # Create temporary directory for tarball
    temp_dir = Path("temp_rpm_build")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    # Create source directory
    source_dir = temp_dir / "break-assistant-1.0.0"
    source_dir.mkdir()
    
    # Copy source files to tarball
    for item in ["src", "requirements.txt", "README.md", "LICENSE", "docs", "break-assistant.png"]:
        if Path(item).exists():
            if Path(item).is_dir():
                shutil.copytree(item, source_dir / item)
            else:
                shutil.copy(item, source_dir / item)
    
    # Create tarball
    tarball_cmd = f"tar -czf break-assistant-1.0.0.tar.gz -C {temp_dir} break-assistant-1.0.0"
    if not run_command(tarball_cmd):
        print("Failed to create source tarball")
        return False
    
    # Copy tarball to system RPM build directory
    print("Copying tarball to RPM build directory...")
    rpm_sources_dir = os.path.expanduser("~/rpmbuild/SOURCES")
    os.makedirs(rpm_sources_dir, exist_ok=True)
    shutil.copy("break-assistant-1.0.0.tar.gz", rpm_sources_dir)
    print(f"✓ Tarball copied to {rpm_sources_dir}")
    
    # Build RPM package
    print("Building RPM package...")
    
    # Check if rpmbuild is available
    if not shutil.which("rpmbuild"):
        print("Error: rpmbuild not found. Please install rpm-build package.")
        return False
    
    # Build package using the spec file
    rpm_cmd = "rpmbuild -bb break-assistant.spec"
    if not run_command(rpm_cmd):
        print("RPM package creation failed")
        return False
    
    # Copy RPM file to current directory
    rpm_build_dir = os.path.expanduser("~/rpmbuild/RPMS/noarch")
    rpm_file = os.path.join(rpm_build_dir, "break-assistant-1.0.0-1.fc41.noarch.rpm")
    
    if os.path.exists(rpm_file):
        current_dir = os.getcwd()
        print(f"Current directory: {current_dir}")
        shutil.copy(rpm_file, current_dir)
        print(f"✓ RPM package copied to: {current_dir}")
        return True
    else:
        print(f"❌ RPM package file not found at: {rpm_file}")
        return False

def main():
    """Main function."""
    print("Building Break Assistant RPM package...")
    
    # Check if we're in the right directory
    if not Path("src/main.py").exists():
        print("Error: src/main.py not found. Please run from the project root.")
        return 1
    
    # Check if spec file exists
    if not Path("break-assistant.spec").exists():
        print("Error: break-assistant.spec not found.")
        return 1
    
    # Create RPM package
    if create_rpm_package():
        print("\nRPM package built successfully!")
        print("You can install it with:")
        print("sudo rpm -i break-assistant-1.0.0-1.noarch.rpm")
        return 0
    else:
        print("\nRPM package build failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 