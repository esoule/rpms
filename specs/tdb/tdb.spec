# $Id$
# Authority: dag
# Upstream: Andrew Tridgell <tridge$samba,org>

Summary: Trivial Database
Name: tdb
Version: 1.0.6
Release: 3
License: GPL
Group: System Environment/Libraries
URL: http://sf.net/projects/tdb/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://dl.sf.net/tdb/tdb-%{version}.tar.gz
Patch: tdb-1.0.6-gcc33.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gdbm-devel

%description
TDB is a Trivial Database. In concept, it is very much like GDBM, 
and BSD's DB except that it allows multiple simultaneous writers 
and uses locking internally to keep writers from trampling on 
each other. TDB is also extremely small.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup
%patch0 -b .gcc3

%build
%{__libtoolize} --force --copy
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall

### FIXME: tdbdump is also shipped with samba. (Please fix upstream)
%{__rm} -f %{buildroot}%{_bindir}/tdbdump

%post
/sbin/ldconfig &>/dev/null

%postun
/sbin/ldconfig &>/dev/null

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
%doc %{_mandir}/man?/*
%{_libdir}/*.a
%exclude %{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/*.h 

%changelog
* Mon Feb 16 2004 Dag Wieers <dag@wieers.com> - 1.0.6-3
- Remove tdbdump from this package, conflicts with RHFC1 samba. (Bert de Bruijn)

* Fri Nov 21 2003 Dag Wieers <dag@wieers.com> - 1.0.6-2
- Patch to build with gcc-3.3.

* Fri May 02 2003 Dag Wieers <dag@wieers.com> - 1.0.6-0
- Initial package. (using DAR)
