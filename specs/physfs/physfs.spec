# $Id: $
# Authority: newrpms
# Upstream: <physfs$icculus,org>

Summary: Library to provide abstract access to various archives
Name: physfs
Version: 0.1.9
Release: 0
License: zlib License 
Group: System Environment/Libraries
URL: http://www.icculus.org/physfs/

Packager: Rudolf Kastl <che666 at uni.de>

Source: http://www.icculus.org/physfs/downloads/physfs-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: ncurses-devel, readline-devel, zlib-devel

%description
A library to provide abstract access to various archives. 
It is intended for use in video games. 
The programmer defines a "write directory" on the physical filesystem. 
No file writing done through the PhysicsFS API can leave that write directory.

%package devel
Summary: Headers for developing programs that will use physfs
Group:   Development/Libraries
Requires: %{name} = %{version} zlib-devel

%description devel
This package contains the headers that programmers will need to develop
applications which will use physfs

%prep
%setup

%build
%configure

%install
%{__rm} -rf %{buildroot}
%{__make} install \
	DESTDIR="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig 2>/dev/null

%postun
/sbin/ldconfig 2>/dev/null

%files
%defattr(-, root, root, 0755)
%doc CHANGELOG CREDITS INSTALL LICENSE TODO
%{_libdir}/*.so.*

%files -n %{name}-devel
%defattr(-, root, root, 0755)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.a
%exclude %{_libdir}/lib%{name}.la
%{_libdir}/*.so
 
%changelog
* Sun Oct 12 2003 Che
- initial rpm release 
