# $Id$

# Authority: dag
# Upstream: Nigel Wetters <nigel$wetters,net>

%define real_name Geography-Countries

Summary: Classes for 2-letter, 3-letter, and numerical codes for countries
Name: perl-Geography-Countries
Version: 1.4
Release: 1
License: distributable
Group: Applications/CPAN
URL: http://search.cpan.org/dist/Geography-Countries/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://search.cpan.org/CPAN/authors/id/A/AB/ABIGAIL/%{real_name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: perl >= 0:5.00503
Requires: perl >= 0:5.00503
Obsoletes: perl(IP::Country) <= 2.08

%description
This module maps country names, and their 2-letter, 3-letter and
numerical codes, as defined by the ISO-3166 maintenance agency [1],
and defined by the UNSD.

%prep
%setup -n %{real_name}-%{version}

%build
CFLAGS="%{optflags}" %{__perl} Makefile.PL \
	PREFIX="%{buildroot}%{_prefix}" \
	INSTALLDIRS="vendor"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall

### Clean up buildroot
%{__rm} -rf %{buildroot}%{_libdir}/perl5/*/*-linux-thread-multi/ \
                %{buildroot}%{_libdir}/perl5/vendor_perl/*/*-linux-thread-multi/ \
                %{buildroot}%{_libdir}/perl5/vendor_perl/*/*-linux/

%clean 
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc MANIFEST
%doc %{_mandir}/man?/*
%{_libdir}/perl5/vendor_perl/*/*

%changelog
* Fri Jan 02 2004 Dag Wieers <dag@wieers.com> - 1.4-1
- Obsolete older perl-IP-Country package.

* Wed Dec 03 2003 Dag Wieers <dag@wieers.com> - 1.4-0
- Initial package. (using DAR)
