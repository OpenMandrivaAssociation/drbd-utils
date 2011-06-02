%define major	8
%define minor	3
%define sub	10
%define pre	0
%define drbd_api_ver	88

Name:		drbd-utils
Version:	%{major}.%{minor}.%{sub}
Release:	%mkrel 1
Summary:	Utilities to manage DRBD devices
License:	GPLv2+
Group:		System/Kernel and hardware
URL:		http://www.drbd.org/
Source:		http://oss.linbit.com/drbd/%{major}.%{minor}/drbd-%{version}.tar.gz
Patch:		drbd-8.3.7-usrsbin.patch
# Install bash completion file on Mandriva
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
%setup -q -n drbd-%{version}
%patch -p1 -b .sbin

# non-arch executable in datadir, fix conf file
sed -i 's,%{_libdir}/drbd/outdate-peer\.sh,%{_datadir}/drbd/outdate-peer.sh,g' scripts/drbd.conf

%build
./configure \
	--sysconfdir=%{_sysconfdir} \
	--localstatedir=%{_var} \
	--prefix=%{_exec_prefix} \
	--with-utils \
	--with-heartbeat\
	--without-xen
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


install -d %{buildroot}%{_var}/lib/drbd
install -d %{buildroot}{%{_bindir},%{_sbindir}}

mkdir -p %{buildroot}%{_datadir}/drbd
mkdir -p %{buildroot}%{_sysconfdir}

%clean
rm -rf %{buildroot}


%post
%_post_service drbd

%preun
%_preun_service drbd

%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/drbd.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/drbd.d/global_common.conf
%dir %{_var}/lib/drbd
%{_sysconfdir}/bash_completion.d/drbdadm
%{_sysconfdir}/rc.d/init.d/drbd
%{_sysconfdir}/udev/rules.d/65-drbd.rules
%{_sbindir}/drbd-overview
%{_sbindir}/drbdadm
%{_sbindir}/drbdmeta
%{_sbindir}/drbdsetup
%dir %{_datadir}/drbd
/usr/lib/drbd/crm-fence-peer.sh
/usr/lib/drbd/crm-unfence-peer.sh
/usr/lib/drbd/notify.sh
/usr/lib/drbd/notify-emergency-reboot.sh
/usr/lib/drbd/notify-emergency-shutdown.sh
/usr/lib/drbd/notify-io-error.sh
/usr/lib/drbd/notify-out-of-sync.sh
/usr/lib/drbd/notify-pri-lost-after-sb.sh
/usr/lib/drbd/notify-pri-lost.sh
/usr/lib/drbd/notify-pri-on-incon-degr.sh
/usr/lib/drbd/notify-split-brain.sh
/usr/lib/drbd/outdate-peer.sh
/usr/lib/drbd/snapshot-resync-target-lvm.sh
/usr/lib/drbd/unsnapshot-resync-target-lvm.sh

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
%dir /usr/lib/ocf/resource.d/linbit
/usr/lib/ocf/resource.d/linbit/drbd
%defattr(0644,root,root,0755)
