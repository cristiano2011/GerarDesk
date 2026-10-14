Name:       gerardesk
Version:    1.5.1
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://gerarservicos.com.br/
Vendor:     GerarDesk
Requires:   gtk3 libxcb libXfixes alsa-lib libva2 gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo
Conflicts: rustdesk
Obsoletes: rustdesk

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/gerardesk/
mkdir -p %{buildroot}/usr/share/gerardesk/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/gerardesk %{buildroot}/usr/bin/gerardesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/gerardesk/libsciter-gtk.so
install $HBB/res/gerardesk.service %{buildroot}/usr/share/gerardesk/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/gerardesk.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/gerardesk.svg
install $HBB/res/gerardesk.desktop %{buildroot}/usr/share/gerardesk/files/
install $HBB/res/gerardesk-link.desktop %{buildroot}/usr/share/gerardesk/files/

%files
/usr/bin/gerardesk
/usr/share/gerardesk/libsciter-gtk.so
/usr/share/gerardesk/files/gerardesk.service
/usr/share/icons/hicolor/256x256/apps/gerardesk.png
/usr/share/icons/hicolor/scalable/apps/gerardesk.svg
/usr/share/gerardesk/files/gerardesk.desktop
/usr/share/gerardesk/files/gerardesk-link.desktop
/usr/share/gerardesk/files/__pycache__/*

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop gerardesk || true
  ;;
esac

%post
cp /usr/share/gerardesk/files/gerardesk.service /etc/systemd/system/gerardesk.service
cp /usr/share/gerardesk/files/gerardesk.desktop /usr/share/applications/
cp /usr/share/gerardesk/files/gerardesk-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable gerardesk
systemctl start gerardesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop gerardesk || true
    systemctl disable gerardesk || true
    rm /etc/systemd/system/gerardesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/gerardesk.desktop || true
    rm /usr/share/applications/gerardesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
