%define Werror_cflags %nil

%define _initddir %_sysconfdir/init.d
%define _vzdir /var/lib/vz
%define _lockdir %{_vzdir}/lock
%define _dumpdir %{_vzdir}/dump
%define _privdir %{_vzdir}/private
%define _rootdir %{_vzdir}/root
%define _templatedir %{_vzdir}/template/
%define _cachedir %{_templatedir}/cache
%define _vzctlvardir /var/lib/vzctl/
%define _veipdir %{_vzctlvardir}/veip
%define _pkglibdir %_libexecdir/vzctl
%define _scriptdir %_pkglibdir/scripts
%define _configdir %_sysconfdir/vz
%define _vpsconfdir %_sysconfdir/sysconfig/vz-scripts
%define _netdir	%_sysconfdir/sysconfig/network-scripts
%define _logrdir %_sysconfdir/logrotate.d
%define _distconfdir %{_configdir}/dists
%define _namesdir %{_configdir}/names
%define _distscriptdir %{_distconfdir}/scripts
%define _udevrulesdir %_sysconfdir/udev/rules.d
%define _bashcdir %_sysconfdir/bash_completion.d

Summary: OpenVZ containers control utility
Name: vzctl
Version: 4.1
Release: 4
License: GPLv2+
Group: System/Kernel and hardware
Source0: http://download.openvz.org/utils/%{name}/%{version}/src/%{name}-%{version}.tar.bz2
#Requires: vzkernel
URL: http://openvz.org/
# these reqs are for vz helper scripts
BuildRequires:	pkgconfig(libcgroup)
BuildRequires:	pkgconfig(libxml-2.0)
Requires: bash
Requires: gawk
Requires: sed
Requires: ed
Requires: grep
Requires: vzquota >= 2.7.0-4
Requires: tar
Requires: chkconfig
# requires for vzmigrate purposes
Requires: rsync
Requires: gawk
Requires: openssh

%description
This utility allows system administator to control OpenVZ containers,
i.e. create, start, shutdown, set various options and limits etc.

%prep
%setup -q

%build
autoreconf -fi
CFLAGS="$RPM_OPT_FLAGS" %configure \
	vzdir=%{_vzdir} \
	--enable-bashcomp \
	--enable-logrotate \
	--without-ploop \
	--disable-static


%make

%install
make DESTDIR=%{buildroot} vpsconfdir=%{_vpsconfdir} \
	install install-redhat-from-spec
ln -s ../sysconfig/vz-scripts %{buildroot}/%{_configdir}/conf
ln -s ../vz/vz.conf %{buildroot}/etc/sysconfig/vz

rm -f %{buildroot}/%{_libdir}/libvzctl.la
rm -f %{buildroot}/%{_libdir}/libvzctl.so
# Those are binaries that either are not ported to vzctl with Upstream Linux,
# or are not applicable to that case. "make install" will copy them over, so we
# just ignore them.
rm -f %{buildroot}/%{_sbindir}/vzsplit
rm -f %{buildroot}/%{_sbindir}/vzlist
rm -f %{buildroot}/%{_sbindir}/vzmemcheck
rm -f %{buildroot}/%{_sbindir}/vzcpucheck
rm -f %{buildroot}/%{_sbindir}/vznetcfg
rm -f %{buildroot}/%{_sbindir}/vznetaddbr
rm -f %{buildroot}/%{_sbindir}/vzcalc
rm -f %{buildroot}/%{_sbindir}/vzpid
rm -f %{buildroot}/%{_sbindir}/vzcfgvalidate
rm -f %{buildroot}/%{_sbindir}/vzifup-post
rm -f %{buildroot}/%{_sbindir}/vzeventd
rm -f %{buildroot}/%{_sbindir}/vzmigrate
rm -f %{buildroot}/%{_sbindir}/vzubc

rm -f %{buildroot}/%{_netdir}/ifup-venet
rm -f %{buildroot}/%{_netdir}/ifdown-venet
rm -f %{buildroot}/%{_netdir}/ifcfg-venet0

rm -f %{buildroot}/%{_initddir}/vz
rm -f %{buildroot}/%{_initddir}/vzeventd

rm -f %{buildroot}/%{_udevrulesdir}/*

rm -f %{buildroot}/%{_scriptdir}/vzevent-reboot
rm -f %{buildroot}/%{_scriptdir}/vzevent-stop
rm -f %{buildroot}/%{_scriptdir}/initd-functions

rm -f %{buildroot}/%{_mandir}/man8/vzeventd.8
rm -f %{buildroot}/%{_mandir}/man8/vzubc.8
rm -f %{buildroot}/%{_mandir}/man8/vzcalc.8
rm -f %{buildroot}/%{_mandir}/man8/vzcfgvalidate.8
rm -f %{buildroot}/%{_mandir}/man8/vzcpucheck.8
rm -f %{buildroot}/%{_mandir}/man8/vzifup-post.8
rm -f %{buildroot}/%{_mandir}/man8/vzlist.8
rm -f %{buildroot}/%{_mandir}/man8/vzmemcheck.8
rm -f %{buildroot}/%{_mandir}/man8/vzmigrate.8
rm -f %{buildroot}/%{_mandir}/man8/vzpid.8
rm -f %{buildroot}/%{_mandir}/man8/vzsplit.8
ls %{buildroot}/%{_mandir}/man8/

%files
%doc COPYING
%dir %{_scriptdir}
%dir %{_pkglibdir}
%dir %{_lockdir}
%dir %{_dumpdir}
%dir %attr(700,root,root) %{_privdir}
%dir %attr(700,root,root) %{_rootdir}
%dir %{_templatedir}
%dir %{_cachedir}
%dir %{_vzctlvardir}
%dir %{_veipdir}
%dir %{_configdir}
%dir %{_namesdir}
%dir %{_vpsconfdir}
%dir %{_distconfdir}
%dir %{_distscriptdir}
%dir %{_vzdir}
%dir %{_sysconfdir}/vz/conf


%{_bashcdir}/*

%{_libdir}/libvzctl-*.so
%{_sbindir}/vzctl
%{_sbindir}/arpsend
%{_sbindir}/ndsend

%{_distscriptdir}/*.sh
%{_distscriptdir}/functions

%{_mandir}/man8/vzctl.8.*
%{_mandir}/man8/arpsend.8.*
%{_mandir}/man8/ndsend.8.*
%{_mandir}/man5/ctid.conf.5.*
%{_mandir}/man5/vz.conf.5.*

%{_scriptdir}/vps-functions
%{_scriptdir}/vps-net_add
%{_scriptdir}/vps-net_del
%{_scriptdir}/vps-netns_dev_add
%{_scriptdir}/vps-netns_dev_del
%{_scriptdir}/vps-create
%{_scriptdir}/vps-download
%{_scriptdir}/vps-pci

%config %{_sysconfdir}/sysconfig/vz
%config(noreplace) %{_configdir}/vz.conf
%config(noreplace) %{_configdir}/osrelease.conf
%config(noreplace) %{_configdir}/download.conf
%config(noreplace) %{_configdir}/oom-groups.conf
%config(noreplace) %{_distconfdir}/*.conf
%config(noreplace) %{_vpsconfdir}/0.conf
%config(noreplace) %{_logrdir}/vzctl
%config %{_distconfdir}/default
%config %{_distconfdir}/distribution.conf-template
%config %{_vpsconfdir}/ve-basic.conf-sample
%config %{_vpsconfdir}/ve-light.conf-sample
%config %{_vpsconfdir}/ve-unlimited.conf-sample
%config %{_vpsconfdir}/ve-vswap-256m.conf-sample
%config %{_vpsconfdir}/ve-vswap-512m.conf-sample
%config %{_vpsconfdir}/ve-vswap-1024m.conf-sample
%config %{_vpsconfdir}/ve-vswap-1g.conf-sample
%config %{_vpsconfdir}/ve-vswap-2g.conf-sample
%config %{_vpsconfdir}/ve-vswap-4g.conf-sample


%post
/bin/rm -rf /dev/vzctl
/bin/mknod -m 600 /dev/vzctl c 126 0
if [ -f %{_configdir}/vz.conf ]; then
	if ! grep "IPTABLES=" %{_configdir}/vz.conf >/dev/null 2>&1; then
		echo 'IPTABLES="ipt_REJECT ipt_tos ipt_limit ipt_multiport iptable_filter iptable_mangle ipt_TCPMSS ipt_tcpmss ipt_ttl ipt_length"' >> %{_configdir}/vz.conf
	fi
fi
/sbin/chkconfig --add vz > /dev/null 2>&1

if [ -f /etc/SuSE-release ]; then
	NET_CFG='ifdown-venet ifup-venet'
	if ! grep -q -E "^alias venet0" /etc/modprobe.conf; then
		echo "alias venet0 vznet" >> /etc/modprobe.conf
	fi
	ln -f /etc/sysconfig/network-scripts/ifcfg-venet0 /etc/sysconfig/network/ifcfg-venet0
	for file in ${NET_CFG}; do
		ln -sf /etc/sysconfig/network-scripts/${file} /etc/sysconfig/network/scripts/${file}
	done
fi

%preun
if [ $1 = 0 ]; then
	/sbin/chkconfig --del vz >/dev/null 2>&1
fi
