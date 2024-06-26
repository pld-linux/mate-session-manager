#
# TODO
# - Terminal=true, depends on mate-terminal, but probably should take preferred terminal application
# mate-session[4970]: WARNING: Could not launch application 'nvidia-settings.desktop': Unable to start application: Failed to execute child process "xdg-terminal" (No such file or directory)

# Conditional build:
%bcond_without	apidocs	# DocBook docs
%bcond_without	systemd	# systemd support for default (when systemd is not running fallback to ConsoleKit)

Summary:	MATE Desktop session manager
Summary(pl.UTF-8):	Zarządca sesji środowiska MATE Desktop
Name:		mate-session-manager
Version:	1.28.0
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://pub.mate-desktop.org/releases/1.28/%{name}-%{version}.tar.xz
# Source0-md5:	69fe63145a1d66f7cd168f62b90244a2
URL:		https://wiki.mate-desktop.org/mate-desktop/components/mate-session-manager/
BuildRequires:	EGL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGLESv2-devel
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.50.0
BuildRequires:	gtk+3-devel >= 3.22.0
BuildRequires:	libepoxy-devel
BuildRequires:	libtool >= 1:1.4.3
%{?with_apidocs:BuildRequires:	libxslt-progs}
BuildRequires:	mate-common
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.596
%{?with_systemd:BuildRequires:	systemd-devel >= 1:183}
BuildRequires:	tar >= 1:1.22
%{?with_apidocs:BuildRequires:	xmlto}
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXau-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-xtrans-devel
BuildRequires:	xz
# needed to satisfy 'filemanager' component (may be changed if alternatives available)
Requires:	caja
Requires:	dbus-glib >= 0.76
Requires:	glib2 >= 1:2.50.0
Requires:	gsettings-desktop-schemas
Requires:	gtk+3 >= 3.22.0
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
# needed to satisfy 'windowmanager' component (may be changed if alternatives available)
Requires:	marco
# needed to satisfy 'panel' component (may be changed if alternatives available)
Requires:	mate-panel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE Desktop session manager.

%description -l pl.UTF-8
Zarządca sesji środowiska MATE Desktop.

%package apidocs
Summary:	MATE Session Manager D-Bus API Reference
Summary(pl.UTF-8):	Dokumentacja API D-Bus MATE Session Managera
Group:		Documentation
BuildArch:	noarch

%description apidocs
Session Manager D-Bus API Reference.

%description apidocs -l pl.UTF-8
Dokumentacja API D-Bus MATE Session Managera.

%prep
%setup -q

%build
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	%{!?with_apidocs:--disable-docbook-docs} \
	%{?with_apidocs:--enable-docbook-docs --docdir=%{_gtkdocdir}/%{name}} \
	--enable-ipv6 \
	--disable-silent-rules \
	--disable-static \
	--with-default-wm=marco \
	--with-gnu-ld \
	%{__with_without systemd}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{es_ES,frp,ie,jv,ku_IQ,pms,ur_PK}

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
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-session
%attr(755,root,root) %{_bindir}/mate-session-inhibit
%attr(755,root,root) %{_bindir}/mate-session-properties
%attr(755,root,root) %{_bindir}/mate-session-save
%attr(755,root,root) %{_bindir}/mate-wm
%attr(755,root,root) %{_libexecdir}/mate-session-check-accelerated
%attr(755,root,root) %{_libexecdir}/mate-session-check-accelerated-gl-helper
%attr(755,root,root) %{_libexecdir}/mate-session-check-accelerated-gles-helper
%{_mandir}/man1/mate-session-inhibit.1*
%{_mandir}/man1/mate-session-properties.1*
%{_mandir}/man1/mate-session-save.1*
%{_mandir}/man1/mate-session.1*
%{_mandir}/man1/mate-wm.1*
%{_datadir}/mate-session-manager
%{_datadir}/glib-2.0/schemas/org.mate.session.gschema.xml
%{_datadir}/xsessions/mate.desktop
%{_desktopdir}/mate-session-properties.desktop
%{_iconsdir}/hicolor/*x*/apps/mate-session-properties.png
%{_iconsdir}/hicolor/scalable/apps/mate-session-properties.svg

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}
%endif
