#!/usr/bin/env python3
"""
Simple RPM package build script for Break Assistant
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
    
    # Create build directory
    build_dir = Path("build_rpm")
    build_dir.mkdir(exist_ok=True)
    
    # Create RPM build structure
    rpm_build_dir = build_dir / "rpmbuild"
    if rpm_build_dir.exists():
        shutil.rmtree(rpm_build_dir)
    
    # Create RPM build directories
    for subdir in ["BUILD", "BUILDROOT", "RPMS", "SOURCES", "SPECS"]:
        (rpm_build_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    # Create spec file
    spec_content = """Name:           break-assistant
Version:        1.0.0
Release:        1%{?dist}
Summary:        Smart break reminder application

License:        MIT
URL:            https://github.com/hmjahid/break-assistant
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
Requires:       python3 >= 3.8
Requires:       python3-tkinter
Requires:       python3-pygame

%description
Break Assistant is a world-class cross-platform break reminder 
application designed to help users maintain healthy work habits 
through smart break scheduling and customizable notifications.

Features:
* Smart break scheduling with timeline management
* Customizable work and break durations
* Sound alerts and theme support
* Cross-platform compatibility
* Progress visualization

%prep
%setup -q

%build
# No build step needed for Python application

%install
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/break-assistant
mkdir -p $RPM_BUILD_ROOT/usr/share/applications
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/256x256/apps

# Copy application files
cp -r src $RPM_BUILD_ROOT/usr/share/break-assistant/
cp requirements.txt $RPM_BUILD_ROOT/usr/share/break-assistant/
cp README.md $RPM_BUILD_ROOT/usr/share/break-assistant/
cp -r docs $RPM_BUILD_ROOT/usr/share/break-assistant/

# Copy icon
cp break-assistant.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/256x256/apps/break-assistant.png

# Create launcher script
echo '#!/bin/bash' > $RPM_BUILD_ROOT/usr/bin/break-assistant
echo 'cd /usr/share/break-assistant' >> $RPM_BUILD_ROOT/usr/bin/break-assistant
echo 'exec python3 src/main.py "$@"' >> $RPM_BUILD_ROOT/usr/bin/break-assistant
chmod 755 $RPM_BUILD_ROOT/usr/bin/break-assistant

# Create desktop file
echo '[Desktop Entry]' > $RPM_BUILD_ROOT/usr/share/applications/break-assistant.desktop
echo 'Name=Break Assistant' >> $RPM_BUILD_ROOT/usr/share/applications/break-assistant.desktop
echo 'Comment=Smart break reminder application' >> $RPM_BUILD_ROOT/usr/share/applications/break-assistant.desktop
echo 'Exec=break-assistant' >> $RPM_BUILD_ROOT/usr/share/applications/break-assistant.desktop
echo 'Icon=break-assistant' >> $RPM_BUILD_ROOT/usr/share/applications/break-assistant.desktop
echo 'Type=Application' >> $RPM_BUILD_ROOT/usr/share/applications/break-assistant.desktop
echo 'Categories=Utility;Office;' >> $RPM_BUILD_ROOT/usr/share/applications/break-assistant.desktop

%files
%doc README.md docs/
/usr/bin/break-assistant
/usr/share/break-assistant/
/usr/share/applications/break-assistant.desktop
/usr/share/icons/hicolor/256x256/apps/break-assistant.png

%changelog
* Mon Jan 01 2024 Break Assistant Team <support@breakassistant.app> - 1.0.0-1
- Initial RPM package release
- Smart break scheduling with timeline management
- Customizable work and break durations
- Sound alerts and theme support
"""
    
    spec_file = rpm_build_dir / "SPECS" / "break-assistant.spec"
    with open(spec_file, "w") as f:
        f.write(spec_content)
    
    # Create source tarball
    source_dir = build_dir / "break-assistant-1.0.0"
    if source_dir.exists():
        shutil.rmtree(source_dir)
    source_dir.mkdir()
    
    # Copy source files to tarball
    for item in ["src", "requirements.txt", "README.md", "LICENSE", "docs", "break-assistant.png"]:
        if Path(item).exists():
            if Path(item).is_dir():
                shutil.copytree(item, source_dir / item)
            else:
                shutil.copy(item, source_dir / item)
    
    # Create tarball
    tarball_cmd = f"tar -czf {rpm_build_dir}/SOURCES/break-assistant-1.0.0.tar.gz -C {build_dir} break-assistant-1.0.0"
    if not run_command(tarball_cmd):
        print("Failed to create source tarball")
        return False
    
    # Build RPM package
    print("Building RPM package...")
    
    # Check if rpmbuild is available
    if not shutil.which("rpmbuild"):
        print("Error: rpmbuild not found. Please install rpm-build package.")
        return False
    
    # Build package
    rpm_cmd = f"rpmbuild --define '_topdir {rpm_build_dir}' -bb {spec_file}"
    if not run_command(rpm_cmd):
        print("RPM package creation failed")
        return False
    
    # Find and copy RPM file
    rpm_files = list(rpm_build_dir.glob("RPMS/*/*.rpm"))
    if rpm_files:
        rpm_file = rpm_files[0]
        shutil.copy(rpm_file, "break-assistant-1.0.0-1.noarch.rpm")
        print(f"✓ RPM package created: break-assistant-1.0.0-1.noarch.rpm")
        return True
    else:
        print("RPM package file not found")
        return False

def main():
    """Main function."""
    print("Building Break Assistant RPM package...")
    
    # Check if we're in the right directory
    if not Path("src/main.py").exists():
        print("Error: src/main.py not found. Please run from the project root.")
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