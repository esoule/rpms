# $Id$
# Authority: dries
# Upstream: Michael G Schwern <mschwern$cpan,org>

%define perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`perl -V:installvendorarch`"; echo $installvendorarch)

%define real_name Class-Virtual

Summary: Base class for virtual base classes
Name: perl-Class-Virtual
Version: 0.05
Release: 1
License: Artistic/GPL
Group: Applications/CPAN
URL: http://search.cpan.org/dist/Class-Virtual/

Source: http://search.cpan.org/CPAN/authors/id/M/MS/MSCHWERN/Class-Virtual-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: perl

%description
This module contains a base class for virtual base classes.

%prep
%setup -n %{real_name}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall
%{__rm} -rf %{buildroot}%{perl_archlib} %{buildroot}%{perl_vendorarch}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc Changes
%doc %{_mandir}/man3/*
%{perl_vendorlib}/Class/Virtual.pm
%{perl_vendorlib}/Class/Virtually

%changelog
* Sat Apr  9 2005 Dries Verachtert <dries@ulyssis.org> - 0.05-1
- Initial package.
