#
# TODO
# - Terminal=true, depends in mate-terminal, but probably should take preferred terminal application
# mate-session[4970]: WARNING: Could not launch application 'nvidia-settings.desktop': Unable to start application: Failed to execute child process "xdg-terminal" (No such file or directory)

# Conditional build:
%bcond_with	apidocs		# DocBook docs (incomplete)
%bcond_without	systemd # enable systemd support for default (when systemd is not running fallback to ConsoleKit)

Summary:	MATE Desktop session manager
Name:		mate-session-manager
Version:	1.6.1
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	e841ff0917f8b64ad33267b0eb5f8364
URL:		http://wiki.mate-desktop.org/mate-session-manager
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	gtk+2-devel >= 2:2.14.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	mate-common
BuildRequires:	pangox-compat-devel
%{?with_systemd:BuildRequires:	systemd-devel >= 183}
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
%{__intltoolize}
%{?with_apidocs:%{__gtkdocize}}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	%{!?with_apidocs:--disable-docbook-docs} \
	%{?with_apidocs:--enable-docbook-docs --docdir=%{_gtkdocdir}/%{name}} \
	%{__enable_disable systemd systemd} \
	--enable-ipv6 \
	--with-gtk=2.0 \
	--with-gnu-ld \
	--with-default-wm=marco \
	--with-x

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# mate < 1.5 did not exist in pld, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/mate-session.convert

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
%{_datadir}/mate-session-manager
%{_iconsdir}/hicolor/*/apps/*.png
%{_iconsdir}/hicolor/scalable/apps/mate-session-properties.svg
%{_datadir}/glib-2.0/schemas/org.mate.session.gschema.xml
%{_datadir}/xsessions/mate.desktop

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}
%endif
