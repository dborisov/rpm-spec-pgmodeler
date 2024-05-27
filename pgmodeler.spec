%define debug_package %{nil}

Name:           pgmodeler
Version:        1.1.3
Release:        1%{?dist}
Summary:        Open-source data modeling tool designed for PostgreSQL

License:        GPL-3.0-only
URL:            https://pgmodeler.io/
Source0:        https://github.com/pgmodeler/pgmodeler/archive/refs/tags/v%{version}.tar.gz
Source1:        %{name}.desktop
Source2:        application-dbm.xml

BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  libappstream-glib
BuildRequires:  ImageMagick
BuildRequires:  desktop-file-utils
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  libpq-devel
BuildRequires:  libXext-devel
Requires:       hicolor-icon-theme
Requires:       shared-mime-info
Requires:       desktop-file-utils

%description
An open-source, multiplatform database modeler for PostgreSQL. This project aims to be a reference database design tool when it comes to FOSS in the PostgreSQL ecosystem. Its feature-rich interface allows quick data modeling and fast code deployment on a server. It also supports reverse engineering by creating a visual representation of existing databases. Besides, pgModeler can also generate SQL scripts to sync a model and a database through the process called diff. This tool is not about modeling only, it also counts with a minimalist but functional database server administration module that allows the execution of any sort of SQL commands, and provides database browsing and data handling in a simple and intuitive UI.

%prep
%autosetup


%build
%qmake_qt6 pgmodeler.pro PREFIX=%{_prefix} BINDIR=%{_bindir} PRIVATEBINDIR=%{_libexecdir} PRIVATELIBDIR=%{_libdir}/%{name} PLUGINSDIR=%{_libdir}/%{name}/plugins
%make_build


%install
rm -rf %{buildroot}
%make_install INSTALL_ROOT=%{buildroot}

install -d -p -m 755 %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/
convert -resize 256x256 assets/conf/pgmodeler_logo.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
desktop-file-install --mode 644 --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

install -D -p -m 644 %{SOURCE2} %{buildroot}%{_datadir}/mime/packages/%{name}.xml
# https://gitlab.gnome.org/GNOME/nautilus/-/issues/2190
install -d -p -m 755 %{buildroot}%{_datadir}/icons/Adwaita/32x32/mimetypes/
install -d -p -m 755 %{buildroot}%{_datadir}/icons/Adwaita/48x48/mimetypes/
install -d -p -m 755 %{buildroot}%{_datadir}/icons/Adwaita/64x64/mimetypes/
install -d -p -m 755 %{buildroot}%{_datadir}/icons/Adwaita/96x96/mimetypes/
install -d -p -m 755 %{buildroot}%{_datadir}/icons/Adwaita/256x256/mimetypes/
convert -resize 32x32 assets/conf/pgmodeler_dbm.png %{buildroot}%{_datadir}/icons/Adwaita/32x32/mimetypes/application-dbm.png
convert -resize 48x48 assets/conf/pgmodeler_dbm.png %{buildroot}%{_datadir}/icons/Adwaita/48x48/mimetypes/application-dbm.png
convert -resize 64x64 assets/conf/pgmodeler_dbm.png %{buildroot}%{_datadir}/icons/Adwaita/64x64/mimetypes/application-dbm.png
convert -resize 96x96 assets/conf/pgmodeler_dbm.png %{buildroot}%{_datadir}/icons/Adwaita/96x96/mimetypes/application-dbm.png
convert -resize 256x256 assets/conf/pgmodeler_dbm.png %{buildroot}%{_datadir}/icons/Adwaita/256x256/mimetypes/application-dbm.png

install -D -p -m 644 %{name}.appdata.xml %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml


%check
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml


%post
update-desktop-database %{_datadir}/applications &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/icons/Adwaita &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &>/dev/null || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/Adwaita &>/dev/null || :
fi


%postun
update-desktop-database %{_datadir}/applications &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/icons/Adwaita &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &>/dev/null || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/Adwaita &>/dev/null || :
fi


%files
%license LICENSE
%doc README.md CHANGELOG.md RELEASENOTES.md
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{_libexecdir}/%{name}-ch
%{_libexecdir}/%{name}-se
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/icons/Adwaita/*/mimetypes/application-dbm.png
%{_datadir}/appdata/%{name}.appdata.xml


%changelog
* Sun May 26 2024 Denis Borisov <dborisov86@gmail.com> - 1.1.3-1
- Initial
