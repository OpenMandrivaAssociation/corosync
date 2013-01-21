# define alphatag svn1211
%define buildtrunk 0
%{?alphatag: %define buildtrunk 1}
%{?_with_buildtrunk: %define buildtrunk 1}
%define major 4
%define libname %mklibname corosync %major
%define libnamedevel %mklibname -d corosync
#define _disable_ld_no_undefined 1

Name:		corosync
Summary:	The Corosync Cluster Engine and Application Programming Interfaces
Version:	2.3.0
Release:	1
License:	BSD
Group:		System/Base
URL:		http://www.corosync.org
Source0:	ftp://ftp:downloads@ftp.corosync.org/downloads/corosync-%{version}/corosync-%{version}.tar.gz

Requires(post):	rpm-helper
Requires(preun): rpm-helper
# Runtime bits
Requires:	%{libname} >= %{version}-%{release}
Conflicts:	openais <= 0.89, openais-devel <= 0.89

%if %{buildtrunk}
BuildRequires: autoconf automake
%endif
BuildRequires: nss-devel
BuildRequires: pkgconfig(libqb)

%description 
This package contains the Corosync Cluster Engine Executive, several default
APIs and libraries, default configuration files, and an init script.

%package	-n %{libname}
Summary:	The Corosync Cluster Engine Libraries
Group:		System/Libraries
Conflicts:	corosync < 0.92-7
Obsoletes:	corosynclib < 1.1.0

%description	-n %{libname}
This package contains corosync libraries.

%package	-n %{libnamedevel}
Summary:	The Corosync Cluster Engine Development Kit
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	pkgconfig
Provides:	corosync-devel = %{version} corosynclibs-devel = %{version}
Obsoletes:	corosync-devel < 0.92-7
Obsoletes:	corosynclibs-devel < 1.1.0

%description	-n %{libnamedevel}
This package contains include files and man pages used to develop using
The Corosync Cluster Engine APIs.

%prep
%setup -q -n corosync-%{version}

#if %{buildtrunk}
./autogen.sh
#endif

#%{_configure}	CFLAGS="$(echo '%{optflags}')" \
#		--prefix=%{_prefix} \
#		--sysconfdir=%{_sysconfdir} \
#		--localstatedir=%{_localstatedir} \
#		--with-lcrso-dir=%{_libexecdir}/lcrso \
#		--libdir=%{_libdir}
%configure --enable-systemd \
		--with-systemddir=%{_unitdir}

%build
%make

%install
%makeinstall_std

## tree fixup
# drop static libs
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
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

%files -n %{libname}
%{_libdir}/lib*.so.*

%files -n %{libnamedevel}
%doc LICENSE README.recovery
%{_includedir}/corosync/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3*
%{_mandir}/man8/cpg_overview.8*
%{_mandir}/man8/votequorum_overview.8*
%{_mandir}/man8/sam_overview.8*
