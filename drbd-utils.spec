%define major	8
%define minor	3
%define sub	0
%define pre	0
%define drbd_api_ver	88

Name:		drbd-utils
Version:	%{major}.%{minor}.%{sub}
%if %pre
Release:	%mkrel 0.%{pre}.1
%else
Release:	%mkrel 1
%endif
Summary:	Utilities to manage DRBD devices
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://www.drbd.org/
%if %pre
Source:		http://oss.linbit.com/drbd/%{major}/drbd-%{version}%{pre}.tar.gz
%else
Source:		http://oss.linbit.com/drbd/%{major}/drbd-%{version}.tar.gz
%endif
Patch:		drbd-8.3.0-usrsbin.patch
BuildRequires:	bison
BuildRequires:	flex
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(post):	initscripts
Requires:	drbd-api = %{drbd_api_ver}
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%package heartbeat
Summary:       Script to help integration with heartbeat
Group:         System/Kernel and hardware
Requires:      heartbeat
Requires:      %{name} = %{version}

%description
DRBD is a block device which is designed to build High Availability clusters.
This is done by mirroring a whole block device via (maybe dedicated) network.
You could see it as a network RAID 1. This package contains the tools to
manage DRBD devices.

%description heartbeat
Installs the datadisk script, designed to ease integration with heartbeat.

%prep
%if %pre
%setup -q -n drbd-%{version}%{pre}
%else
%setup -q -n drbd-%{version}
%endif
%patch -p1 -b .sbin

# non-arch executable in datadir, fix conf file
sed -i 's,/usr/lib/drbd/outdate-peer\.sh,%{_datadir}/drbd/outdate-peer.sh,g' scripts/drbd.conf

%build
make -j ${NRPROC:-1} tools

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
make PREFIX=%{buildroot} install-tools

install -d %{buildroot}%{_var}/lib/drbd
install -d %{buildroot}{%{_bindir},%{_sbindir}}

mkdir -p %{buildroot}%{_datadir}/drbd
mv -f %{buildroot}%{_prefix}/lib/drbd/notify.sh %{buildroot}%{_datadir}/drbd
mv -f %{buildroot}%{_prefix}/lib/drbd/notify-out-of-sync.sh %{buildroot}%{_datadir}/drbd
mv -f %{buildroot}%{_prefix}/lib/drbd/notify-split-brain.sh %{buildroot}%{_datadir}/drbd
mv -f %{buildroot}%{_prefix}/lib/drbd/outdate-peer.sh %{buildroot}%{_datadir}/drbd
mv -f %{buildroot}%{_prefix}/lib/drbd/snapshot-resync-target-lvm.sh %{buildroot}%{_datadir}/drbd
mv -f %{buildroot}%{_prefix}/lib/drbd/unsnapshot-resync-target-lvm.sh %{buildroot}%{_datadir}/drbd
# don't use rm -rf because we want to know if some new version
# installed something here we didn't know about
rmdir %{buildroot}%{_prefix}/lib/drbd/
rmdir %{buildroot}%{_prefix}/lib

%clean
rm -rf %{buildroot}

%post
%_post_service drbd

%preun
%_preun_service drbd

%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/drbd.conf
%dir %{_var}/lib/drbd
%{_sysconfdir}/rc.d/init.d/drbd
%{_sysconfdir}/xen/scripts/block-drbd
%{_sbindir}/drbd-overview.pl
%{_sbindir}/drbdadm
%{_sbindir}/drbdmeta
%{_sbindir}/drbdsetup
%dir %{_datadir}/cluster
%{_datadir}/cluster/drbd.metadata
%{_datadir}/cluster/drbd.sh
%dir %{_datadir}/drbd
%{_datadir}/drbd/notify.sh
%{_datadir}/drbd/notify-out-of-sync.sh
%{_datadir}/drbd/notify-split-brain.sh
%{_datadir}/drbd/outdate-peer.sh
%{_datadir}/drbd/snapshot-resync-target-lvm.sh
%{_datadir}/drbd/unsnapshot-resync-target-lvm.sh

%defattr(0644,root,root,0755)
%doc %{_mandir}/man5/drbd.conf.5*
%doc %{_mandir}/man8/drbd.8*
%doc %{_mandir}/man8/drbdadm.8*
%doc %{_mandir}/man8/drbdmeta.8*
%doc %{_mandir}/man8/drbddisk.8*
%doc %{_mandir}/man8/drbdsetup.8*

%files heartbeat
%defattr(-,root,root)
%{_sysconfdir}/ha.d/resource.d/drbddisk
%{_sysconfdir}/ha.d/resource.d/drbdupper
%defattr(0644,root,root,0755)

