Name:           break-assistant
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

# Create resources directory and copy audio files
mkdir -p $RPM_BUILD_ROOT/usr/share/break-assistant/src/resources/audio
cp $RPM_BUILD_DIR/break-assistant-1.0.0/src/audio/*.wav $RPM_BUILD_ROOT/usr/share/break-assistant/src/resources/audio/ 2>/dev/null || true
cp $RPM_BUILD_DIR/break-assistant-1.0.0/src/audio/*.mp3 $RPM_BUILD_ROOT/usr/share/break-assistant/src/resources/audio/ 2>/dev/null || true

# Copy icon to RPM package icons directory
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
%defattr(-,root,root,-)
/usr/bin/break-assistant
/usr/share/break-assistant/
/usr/share/applications/break-assistant.desktop
/usr/share/icons/hicolor/256x256/apps/break-assistant.png

%changelog
* Thu Jul 25 2025 Jahid Hasan <mdjahidhasan@gmail.com> - 1.0.0-1
- Initial RPM release
