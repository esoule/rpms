# $Id$
# Authority: dag
# Upstream: Pedro L. Orso <orso$onda,com,br>
# Upstream: <orso$yahoogroups,com>

Summary: Squid usage report generator per user/ip/name
Name: sarg
Version: 1.4.1
Release: 4
License: GPL
Group: System Environment/Daemons
URL: http://sarg.sf.net/sarg.php

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://dl.sf.net/sarg/sarg-%{version}.tar.gz
Patch0: sarg-1.4.1-indexsort.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: perl
Requires: squid
Obsoletes: sqmgrlog

%description
Squid Analysis Report Generator is a tool that allows you to view "where"
your users are going to on the Internet. Sarg generate reports in html
showing users, IP Addresses, bytes, sites and times. 

%prep
%setup
%patch0 -p1

### FIXME: Make Makefile use autotool directory standard. (Please fix upstream)
%{__perl} -pi.orig -e '
		s|= \@BINDIR\@|= \$(bindir)|g;
		s|= \@MANDIR\@|= \$(mandir)/man1|g;
		s|= \@SYSCONFDIR\@|= \$(sysconfdir)/sarg|g;
		s|\@BINDIR\@|%{_bindir}|g;
		s|\@SYSCONFDIR\@|%{_sysconfdir}/sarg|g;
	' Makefile.in

%{__perl} -pi.orig -e '
		s|^#(access_log) (.+)$|#$1 $2\n$1 %{_localstatedir}/log/squid/access.log|;
		s|^#(output_dir) (.+)$|#$1 $2\n$1 %{_localstatedir}/www/sarg/ONE-SHOT|;
		s|^#(resolve_ip) (.+)$|#$1 $2\n$1 yes|;
		s|^#(show_successful_message) (.+)$|#$1 $2\n$1 no|;
		s|^#(mail_utility) (.+)$|#$1 $2\n$1 mail|;
	' sarg.conf

%{__cat} <<'EOF' >sarg.daily
#!/bin/bash
exec %{_bindir}/sarg \
	-o %{_localstatedir}/www/sarg/daily \
	-d "$(date --date "1 day ago" +%d/%m/%Y)"
EOF

%{__cat} <<'EOF' >sarg.weekly
#!/bin/bash
exec %{_bindir}/sarg \
	-o %{_localstatedir}/www/sarg/weekly \
	-d "$(date --date "1 day ago" +%d/%m/%Y)-$(date --date "1 week ago" +%d/%m/%Y)"
EOF

%{__cat} <<'EOF' >sarg.monthly
#!/bin/bash
exec %{_bindir}/sarg \
	-o %{_localstatedir}/www/sarg/monthly \
	-d "$(date --date "1 day ago" +%d/%m/%Y)-$(date --date "1 month ago" +%d/%m/%Y)"
EOF

%{__cat} <<EOF >sarg-index.html
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
	<title>Squid User's Access Report</title>
</head>
<body>
	<center><table cellpadding="0" cellspacing="0">
		<tbody><tr>
		<th align="center"><b><font color="green" size="+1">Squid User's Access Report</font></b></th>
		</tr></tbody>
	</table></center>
	<center><table cellpadding="1" cellspacing="1">
		<tbody><tr>
			<th bgcolor="blanchedalmond"><font size="-1" color="darkblue">DIRECTORY</font></th>
			<th bgcolor="blanchedalmond"><font size="-1" color="darkblue">DESCRIPTION</font></th>
		</tr><tr>
			<td bgcolor="beige"><font size="-1"><a href="ONE-SHOT/index.html">ONE-SHOT</a></font></td>
			<td bgcolor="beige"><font size="-1">One shot reports</font></td>
		</tr><tr>
			<td bgcolor="beige"><font size="-1"><a href="daily/index.html">daily</a></font></td>
			<td bgcolor="beige"><font size="-1">Daily reports</font></td>
		</tr><tr>
			<td bgcolor="beige"><font size="-1"><a href="weekly/index.html">weekly</a></font></td>
			<td bgcolor="beige"><font size="-1">Weekly reports</font></td>
		</tr><tr>
			<td bgcolor="beige"><font size="-1"><a href="monthly/index.html">monthly</a></font></td>
			<td bgcolor="beige"><font size="-1">Monthly reports</font></td>
		</tr></tbody>
	</table></center><br><br>
	<center><font size="-2">Generated by <a href="http://web.onda.com.br/orso/sarg.html">sarg</a>.</font></center>
</body>
</html>
EOF

%{__cat} <<EOF >sarg-http.conf
Alias /sarg %{_localstatedir}/www/sarg

<Directory %{_localstatedir}/www/sarg>
	DirectoryIndex index.html
	order deny,allow
	deny from all
	allow from 127.0.0.1
</Directory>
EOF

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

### FIXME: Makefile doesn't create target directories (Please fix upstream)
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/sarg/ \
			%{buildroot}%{_bindir} \
			%{buildroot}%{_mandir}/man1/
%makeinstall

%{__install} -d -m0755 %{buildroot}%{_localstatedir}/www/sarg/{ONE-SHOT,daily,weekly,monthly}/
%{__install} -D -m0644 sarg-http.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/sarg.conf
%{__install} -D -m0755 sarg.daily %{buildroot}%{_sysconfdir}/cron.daily/sarg
%{__install} -D -m0755 sarg.weekly %{buildroot}%{_sysconfdir}/cron.weekly/sarg
%{__install} -D -m0755 sarg.monthly %{buildroot}%{_sysconfdir}/cron.monthly/sarg
%{__install} -D -m0644 sarg-index.html %{buildroot}%{_localstatedir}/www/sarg/index.html

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc ChangeLog CONTRIBUTORS copying DONATIONS README sarg.html
%doc %{_mandir}/man?/*
%dir %{_sysconfdir}/sarg/
%config(noreplace) %{_sysconfdir}/sarg/sarg.conf
%config(noreplace) %{_sysconfdir}/sarg/exclude_codes
%config(noreplace) %{_sysconfdir}/httpd/conf.d/sarg.conf
%config(noreplace) %{_sysconfdir}/cron.*/sarg
%{_sysconfdir}/sarg/languages/
%{_bindir}/*
%{_localstatedir}/www/sarg/

%changelog
* Wed Jun 30 2004 Dag Wieers <dag@wieers.com> - 1.4.1-4
- Fixed default mail_utility. (John Florian)

* Sat Apr 10 2004 Dag Wieers <dag@wieers.com> - 1.4.1-3
- Fixed problem with inline cron-scripts. (Luigi Iotti)

* Tue Apr 06 2004 Dag Wieers <dag@wieers.com> - 1.4.1-2
- Fixed missing directories in sarg. (William Hooper)

* Wed Mar 17 2004 Dag Wieers <dag@wieers.com> - 1.4.1-1
- Initial package. (using DAR)
