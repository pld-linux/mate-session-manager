#
# TODO
# - Terminal=true, depends on mate-terminal, but probably should take preferred terminal application
# mate-session[4970]: WARNING: Could not launch application 'nvidia-settings.desktop': Unable to start application: Failed to execute child process "xdg-terminal" (No such file or directory)

# Conditional build:
%bcond_without	apidocs	# DocBook docs
%bcond_with	gtk3	# use GTK+ 3.x instead of 2.x
%bcond_without	systemd	# systemd support for default (when systemd is not running fallback to ConsoleKit)
%bcond_with	upower	# UPower suspend/hibernate support (0.9.x only)

Summary:	MATE Desktop session manager
Summary(pl.UTF-8):	Zarządca sesji środowiska MATE Desktop
Name:		mate-session-manager
Version:	1.14.0
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.14/%{name}-%{version}.tar.xz
# Source0-md5:	41b0b5dfd4a2978546119ed9721c95e1
Patch0:		%{name}-en_us_suspend_hotkey.patch
URL:		http://wiki.mate-desktop.org/mate-session-manager
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	desktop-file-utils
BuildRequires:	glib2-devel >= 1:2.36.0
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.24.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	intltool >= 0.50.1
BuildRequires:	libtool >= 1:1.4.3
%{?with_apidocs:BuildRequires:	libxslt-progs}
BuildRequires:	mate-common
BuildRequires:	pango-devel
BuildRequires:	pangox-compat-devel
BuildRequires:	pkgconfig
%{?with_systemd:BuildRequires:	systemd-devel >= 1:183}
BuildRequires:	tar >= 1:1.22
%{?with_upower:BuildRequires:	upower-devel >= 0.9.0}
%{?with_apidocs:BuildRequires:	xmlto}
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXau-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xz
# needed to satisfy 'filemanager' component (may be changed if alternatives available)
Requires:	caja
Requires:	dbus-glib >= 0.76
Requires:	glib2 >= 1:2.36.0
Requires:	gsettings-desktop-schemas
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.24.0}
%{?with_gtk3:Requires:	gtk+3 >= 3.0.0}
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
# needed to satisfy 'windowmanager' component (may be changed if alternatives available)
Requires:	marco
# needed to satisfy 'panel' component (may be changed if alternatives available)
Requires:	mate-panel
%{?with_upower:Requires:	upower-libs >= 0.9.0}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE Desktop session manager.

%description -l pl.UTF-8
Zarządca sesji środowiska MATE Desktop.

%package apidocs
Summary:	MATE Session Manager D-Bus API Reference
Summary(pl.UTF-8):	Dokumentacja API D-Bus MATE Session Managera
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
Session Manager D-Bus API Reference.

%description apidocs -l pl.UTF-8
Dokumentacja API D-Bus MATE Session Managera.

%prep
%setup -q
%patch0 -p1

%build
%{__intltoolize}
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
	%{!?with_upower:--disable-upower} \
	--with-default-wm=marco \
	--with-gnu-ld \
	%{?with_gtk3:--with-gtk=3.0} \
	%{__with_without systemd} \
	--with-x

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{frp,jv}

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
%doc AUTHORS ChangeLog MAINTAINERS NEWS README
%attr(755,root,root) %{_bindir}/mate-session
%attr(755,root,root) %{_bindir}/mate-session-inhibit
%attr(755,root,root) %{_bindir}/mate-session-properties
%attr(755,root,root) %{_bindir}/mate-session-save
%attr(755,root,root) %{_bindir}/mate-wm
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
