# $Id$
# Authority: dag
# Upstream: <irssi-dev$dragoncat,net>

%{?dist: %{expand: %%define %dist 1}}

%define perl_vendorarch %(eval "`perl -V:installvendorarch`"; echo $installvendorarch)

Summary: Modular text-mode IRC client
Name: irssi
Version: 0.8.9
Release: 1
License: GPL
Group: Applications/Communications
URL: http://irssi.org/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://irssi.org/files/irssi-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: glib2-devel, ncurses-devel, libgc-devel

%description
Irssi is a modular IRC client that currently has only text mode user
interface, but 80-90% of the code isn't text mode specific so other UI
could be created pretty easily. Also, Irssi isn't really even IRC
specific anymore, there's already a working SILC module available.
Support for other protocols like ICQ could be created some day too.

%prep
%setup
%{?rh9:%{__perl} -pi.orig -e 's|^CFLAGS = |CFLAGS = -I/usr/kerberos/include |' src/core/Makefile.in}

%build
%configure \
	--with-plugins \
        --enable-ipv6 \
        --with-textui \
	--with-imlib \
        --with-bot \
        --with-proxy \
	--with-perl="yes" \
	--enable-ssl \
	--with-glib2 \
        --with-ncurses \
	--with-gc \
	--with-perl-lib="%{buildroot}%{perl_vendorarch}"
#	--with-perl-lib="vendor"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall \
	PREFIX="%{buildroot}%{_prefix}" \
	PERL_USE_LIB="%{buildroot}%{perl_vendorarch}"

### Clean up buildroot
%{__rm} -f %{buildroot}%{_libdir}/irssi/modules/*.{a,la} \
		%{buildroot}%{perl_vendorarch}/auto/Irssi/.packlist \
		%{buildroot}%{perl_vendorarch}/auto/Irssi/*/.packlist \
		%{buildroot}%{perl_vendorarch}/perllocal.pod
%{__rm} -rf %{buildroot}%{_docdir}/irssi/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%doc docs/*.txt docs/*.html
%doc %{_mandir}/man?/*
%config(noreplace) %{_sysconfdir}/*
%{_bindir}/*
%{_libdir}/irssi/
%{_datadir}/irssi/
%{perl_vendorarch}/*

%changelog
* Wed Mar 31 2004 Dag Wieers <dag@wieers.com> - 0.8.9-1
- Rebuild against new fc1 perl package. (Christopher Stone)

* Fri Dec 12 2003 Dag Wieers <dag@wieers.com> - 0.8.9-0
- Updated to release 0.8.9.

* Fri Dec 12 2003 Dag Wieers <dag@wieers.com> - 0.8.9-0
- Updated to release 0.8.9.

* Sun Nov 23 2003 Dag Wieers <dag@wieers.com> - 0.8.8-0
- Fixed the longstanding problem with the perl modules !! (Rudolf Kastl)
- Updated to release 0.8.8.

* Thu Apr 17 2003 Dag Wieers <dag@wieers.com> - 0.8.6-4
- Fixed compilation-errors for RH9.

* Mon Mar 10 2003 Dag Wieers <dag@wieers.com> - 0.8.6-3
- Fixed the Perl module problem.

* Fri Jan 17 2003 Dag Wieers <dag@wieers.com> - 0.8.6-0
- Initial package. (using DAR)
