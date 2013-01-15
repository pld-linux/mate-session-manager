#
# Conditional build:
%bcond_with	apidocs		# DocBook docs (incomplete)

Summary:	MATE Desktop session manager
Name:		mate-session-manager
Version:	1.5.0
Release:	3
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	64090402b0df99f874ca1cb2cc499745
URL:		http://wiki.mate-desktop.org/mate-session-manager
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+2-devel >= 2:2.14.0
BuildRequires:	icon-naming-utils
BuildRequires:	intltool >= 0.40.0
BuildRequires:	mate-common
BuildRequires:	mate-icon-theme
BuildRequires:	mate-polkit-devel
BuildRequires:	polkit-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	upower-devel >= 0.9.0
%{?with_apidocs:BuildRequires:	xmlto}
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xz
Requires:	glib2 >= 1:2.26.0
Requires:	gsettings-desktop-schemas
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	mate-desktop >= 1.5
# needed to satisfy 'filemanager' component (may be changed if alternatives available)
Requires:	mate-file-manager
# needed to satisfy 'panel' component (may be changed if alternatives available)
Requires:	mate-panel
# needed to satisfy 'windowmanager' component (may be changed if alternatives available)
Requires:	mate-window-manager
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE Desktop session manager.

%package apidocs
Summary:	Session Manager D-Bus API Reference
Summary(pl.UTF-8):	Dokumentacja API Session Manager
Group:		Documentation

%description apidocs
Session Manager D-Bus API Reference.

%description apidocs -l pl.UTF-8
Dokumentacja API Session Manager.

%prep
%setup -q

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
	--disable-static \
	%{!?with_apidocs:--disable-docbook-docs} \
	%{?with_apidocs:--enable-docbook-docs --docdir=%{_gtkdocdir}/%{name}} \
	--enable-ipv6 \
	--with-gtk=2.0 \
	--with-gnu-ld \
	--with-default-wm=marco \
	--with-x
%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-install \
	--remove-category="MATE" \
	--add-category="X-Mate" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
$RPM_BUILD_ROOT%{_desktopdir}/mate-session-properties.desktop

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_icon_cache hicolor
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_bindir}/mate-session
%attr(755,root,root) %{_bindir}/mate-session-properties
%attr(755,root,root) %{_bindir}/mate-session-save
%attr(755,root,root) %{_bindir}/mate-wm
%{_mandir}/man1/mate-session-properties.1*
%{_mandir}/man1/mate-session-save.1*
%{_mandir}/man1/mate-session.1*
%{_mandir}/man1/mate-wm.1*
%{_desktopdir}/mate-session-properties.desktop
%{_datadir}/mate-session
%{_iconsdir}/hicolor/*/apps/*.png
%{_iconsdir}/hicolor/scalable/apps/mate-session-properties.svg
%{_datadir}/glib-2.0/schemas/org.mate.session.gschema.xml
%{_datadir}/xsessions/mate.desktop

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}
%endif
