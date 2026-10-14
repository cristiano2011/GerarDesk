Name:       gerardesk
Version:    1.5.1
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://gerarservicos.com.br/
Vendor:     GerarDesk
Requires:   gtk3 libxcb1 libXfixes3 alsa-utils libXtst6 libva2 gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1 xdotool
Conflicts: rustdesk
Obsoletes: rustdesk
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/gerardesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/gerardesk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/gerardesk.service -t "%{buildroot}/usr/share/gerardesk/files"
install -Dm 644 $HBB/res/gerardesk.desktop -t "%{buildroot}/usr/share/gerardesk/files"
install -Dm 644 $HBB/res/gerardesk-link.desktop -t "%{buildroot}/usr/share/gerardesk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/gerardesk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/gerardesk.svg"

%files
/usr/share/gerardesk/*
/usr/share/gerardesk/files/gerardesk.service
/usr/share/icons/hicolor/256x256/apps/gerardesk.png
/usr/share/icons/hicolor/scalable/apps/gerardesk.svg
/usr/share/gerardesk/files/gerardesk.desktop
/usr/share/gerardesk/files/gerardesk-link.desktop

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
ln -sf /usr/share/gerardesk/gerardesk /usr/bin/gerardesk
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
    rm /usr/bin/gerardesk || true
    rmdir /usr/lib/gerardesk || true
    rmdir /usr/local/gerardesk || true
    rmdir /usr/share/gerardesk || true
    rm /usr/share/applications/gerardesk.desktop || true
    rm /usr/share/applications/gerardesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/gerardesk || true
    rmdir /usr/local/gerardesk || true
  ;;
esac
