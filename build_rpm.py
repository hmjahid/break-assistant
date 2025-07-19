#!/usr/bin/env python3
"""
RPM package build script for Break Assistant
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
    
    # Use system RPM build directory
    rpm_build_dir = Path(os.path.expanduser("~/rpmbuild"))
    rpm_sources_dir = rpm_build_dir / "SOURCES"
    rpm_specs_dir = rpm_build_dir / "SPECS"
    
    # Create RPM build directories if they don't exist
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
BuildRequires:  python3-devel
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
rm -rf $RPM_BUILD_ROOT
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
cat > $RPM_BUILD_ROOT/usr/bin/break-assistant << 'EOF'
#!/bin/bash
cd /usr/share/break-assistant
exec python3 src/main.py "$@"
EOF
chmod 755 $RPM_BUILD_ROOT/usr/bin/break-assistant

# Create desktop file
cat > $RPM_BUILD_ROOT/usr/share/applications/break-assistant.desktop << 'EOF'
[Desktop Entry]
Name=Break Assistant
Comment=Smart break reminder application
Exec=break-assistant
Icon=break-assistant
Type=Application
Categories=Utility;Office;
EOF

%files
%license LICENSE
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
    
    spec_file = rpm_specs_dir / "break-assistant.spec"
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
    
    # Create tarball in current directory first
    tarball_cmd = f"tar -czf break-assistant-1.0.0.tar.gz -C {build_dir} break-assistant-1.0.0"
    if not run_command(tarball_cmd):
        print("Failed to create source tarball")
        return False
    
    # Copy tarball to RPM sources directory
    shutil.copy("break-assistant-1.0.0.tar.gz", rpm_sources_dir)
    print(f"✓ Tarball copied to {rpm_sources_dir}")
    
    # Build RPM package
    print("Building RPM package...")
    
    # Check if rpmbuild is available
    if not shutil.which("rpmbuild"):
        print("Error: rpmbuild not found. Please install rpm-build package.")
        return False
    
    # Build package using system RPM build directory
    rpm_cmd = f"rpmbuild -bb {spec_file}"
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