%define major	4
%define maj5	5
%define maj6	6
%define	libcmap		%mklibname cmap %{major}
%define	libname_common	%mklibname corosync_common %{major}
%define	libcpg		%mklibname cpg %{major}
%define	libsam		%mklibname sam %{major}
%define	libcfg		%mklibname cfg %{maj6}
%define	libquorum	%mklibname quorum %{maj5}
%define	libtotem_pg	%mklibname totem_pg %{maj5}
%define	libvotequorum	%mklibname votequorum %{maj6}
%define devname %mklibname -d corosync

Summary:	The Corosync Cluster Engine and Application Programming Interfaces
Name:		corosync
Version:	2.3.3
Release:	2
License:	BSD
Group:		System/Base
Url:		http://www.corosync.org
Source0:	http://build.clusterlabs.org/corosync/releases/corosync-%{version}.tar.gz

BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(libqb)
Requires(post,preun):	rpm-helper

%description 
This package contains the Corosync Cluster Engine Executive, several default
APIs and libraries, default configuration files, and an init script.

%package	-n %{libcmap}
Summary:	The Corosync Cluster Engine Libraries
Group:		System/Libraries
Conflicts:	%{_lib}corosync4 > 2.3.0-0

%description	-n %{libcmap}
This package contains corosync libraries.

%package	-n %{libname_common}
Summary:	The Corosync Cluster Engine Libraries
Group:		System/Libraries
Obsoletes:	%{_lib}corosync4 > 2.3.0-0

%description	-n %{libname_common}
This package contains corosync libraries.

%package	-n %{libcpg}
Summary:	The Corosync Cluster Engine Libraries
Group:		System/Libraries
Conflicts:	%{_lib}corosync4 > 2.3.0-0

%description	-n %{libcpg}
This package contains corosync libraries.

%package	-n %{libsam}
Summary:	The Corosync Cluster Engine Libraries
Group:		System/Libraries
Conflicts:	%{_lib}corosync4 > 2.3.0-0

%description	-n %{libsam}
This package contains corosync libraries.

%package	-n %{libcfg}
Summary:	The Corosync Cluster Engine Libraries
Group:		System/Libraries
Conflicts:	%{_lib}corosync4 > 2.3.0-0

%description	-n %{libcfg}
This package contains corosync libraries.

%package	-n %{libquorum}
Summary:	The Corosync Cluster Engine Libraries
Group:		System/Libraries
Conflicts:	%{_lib}corosync4 > 2.3.0-0

%description	-n %{libquorum}
This package contains corosync libraries.

%package	-n %{libtotem_pg}
Summary:	The Corosync Cluster Engine Libraries
Group:		System/Libraries
Conflicts:	%{_lib}corosync4 > 2.3.0-0

%description	-n %{libtotem_pg}
This package contains corosync libraries.

%package	-n %{libvotequorum}
Summary:	The Corosync Cluster Engine Libraries
Group:		System/Libraries
Conflicts:	%{_lib}corosync4 > 2.3.0-0

%description	-n %{libvotequorum}
This package contains corosync libraries.

%package	-n %{devname}
Summary:	The Corosync Cluster Engine Development Kit
Group:		Development/C
Requires:	%{libcmap} = %{version}-%{release}
Requires:	%{libname_common} = %{version}-%{release}
Requires:	%{libcpg} = %{version}-%{release}
Requires:	%{libsam} = %{version}-%{release}
Requires:	%{libcfg} = %{version}-%{release}
Requires:	%{libquorum} = %{version}-%{release}
Requires:	%{libtotem_pg} = %{version}-%{release}
Requires:	%{libvotequorum} = %{version}-%{release}
Provides:	%{name}-devel = %{version}

%description	-n %{devname}
This package contains include files and man pages used to develop using
The Corosync Cluster Engine APIs.

%prep
%setup -q

./autogen.sh
%configure2_5x \
	--disable-static \
	--enable-systemd \
	--with-systemddir=%{_unitdir}

%build
%make

%install
%makeinstall_std

## tree fixup
# drop static libs
rm -f %{buildroot}%{_libdir}/*.a
# drop docs and html docs for now
rm -rf %{buildroot}%{_docdir}/*

#add logs directory
install -d %{buildroot}/var/log/%{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
[ "$1" -ge "1" ] && /sbin/service corosync condrestart &>/dev/null || :

%files 
%doc LICENSE SECURITY
%{_sbindir}/corosync*
%{_bindir}/corosync*
%dir %{_sysconfdir}/corosync
%dir %{_sysconfdir}/corosync/service.d
%dir %{_sysconfdir}/corosync/uidgid.d
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%config(noreplace) %{_sysconfdir}/corosync/corosync.conf.example
%config(noreplace) %{_sysconfdir}/corosync/corosync.conf.example.udpu
%dir %{_localstatedir}/lib/corosync
%{_mandir}/man8/corosync_overview.8*
%{_mandir}/man8/corosync-*.8*
%{_mandir}/man8/corosync.8*
%{_mandir}/man8/cmap_keys.8*
%{_mandir}/man8/cmap_overview.8*
%{_mandir}/man8/quorum_overview.8*
%{_mandir}/man5/corosync.conf.5*
%{_mandir}/man5/votequorum.5*
%{_unitdir}/corosync-notifyd.service
%{_unitdir}/corosync.service
%dir /var/log/%{name}

%files -n %{libcmap}
%{_libdir}/libcmap.so.%{major}*

%files -n %{libname_common}
%{_libdir}/libcorosync_common.so.%{major}*

%files -n %{libcpg}
%{_libdir}/libcpg.so.%{major}*

%files -n %{libsam}
%{_libdir}/libsam.so.%{major}*

%files -n %{libcfg}
%{_libdir}/libcfg.so.%{maj6}*

%files -n %{libquorum}
%{_libdir}/libquorum.so.%{maj5}*

%files -n %{libtotem_pg}
%{_libdir}/libtotem_pg.so.%{maj5}*

%files -n %{libvotequorum}
%{_libdir}/libvotequorum.so.%{maj6}*

%files -n %{devname}
%doc LICENSE README.recovery
%{_includedir}/corosync/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3*
%{_mandir}/man8/cpg_overview.8*
%{_mandir}/man8/votequorum_overview.8*
%{_mandir}/man8/sam_overview.8*
