# $Id: _template.spec 219 2004-04-09 06:21:45Z dag $
# Authority: dag
# Upstream: Simon Howard <fraggle$alkali,org>

%define dfi %(which desktop-file-install &>/dev/null; echo $?)

%define real_version sdl_sopwith

Summary: Classic sopwith game
Name: sopwith
Version: 1.7.1
Release: 1
Group: Amusements/Games
License: GPL
URL: http://sdl-sopwith.sf.net/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://dl.sf.net/sdl-sopwith/sdl_sopwith-%{version}.tar.gz
Source1: sopwith.png
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gtk2-devel, SDL-devel

%description
This is a port of the classic computer game "Sopwith" to run on modern 
computers and operating systems. 

%prep
%setup -n %{real_version}-%{version}

%{__cat} <<EOF >sopwith.desktop
[Desktop Entry]
Name=Sopwith
Comment=The classic sopwith game
Exec=gtksopwith
Type=Application
Terminal=false
Icon=sopwith.png
Categories=Application;Game;
EOF

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall

%if %{dfi}
        %{__install} -D -m0644 sopwith.desktop %{buildroot}%{_datadir}/gnome/apps/Games/sopwith.desktop
%else
        %{__install} -d -m0755 %{buildroot}%{_datadir}/applications/
        desktop-file-install --vendor gnome                \
                --add-category X-Red-Hat-Base              \
                --dir %{buildroot}%{_datadir}/applications \
                sopwith.desktop
%endif

%{__install} -D -m0644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/sopwith.png

%clean
%{__rm} -rf %{buildroot}

%files 
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING FAQ NEWS README TODO doc/*.txt
%doc %{_mandir}/man?/*
%{_bindir}/*
%{_bindir}/gtksopwith
%{_datadir}/pixmaps/*.png
%if %{dfi}
	%{_datadir}/gnome/apps/Games/*.desktop
%else
	%{_datadir}/applications/*.desktop
%endif
%exclude %{_docdir}/sopwith/

%changelog
* Thu Apr 29 2004 Dag Wieers <dag@wieers.com> - 1.7.1-1
- Initial package. (using DAR)
