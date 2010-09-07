# define alphatag svn1211
%define buildtrunk 0
%{?alphatag: %define buildtrunk 1}
%{?_with_buildtrunk: %define buildtrunk 1}
%define major 4
%define libname %mklibname corosync %major
%define libnamedevel %mklibname -d corosync
#define _disable_ld_no_undefined 1

Name: corosync
Summary: The Corosync Cluster Engine and Application Programming Interfaces
Version: 1.2.8
Release: %mkrel 1
License: BSD
Group: System/Base
URL: http://www.corosync.org
Source0: ftp://ftp:downloads@ftp.corosync.org/downloads/corosync-%{version}/corosync-%{version}.tar.gz
Patch1:	corosync-fix-linking.patch

# Runtime bits
Requires: %{libname} >= %{version}-%{release}
Requires(pre): rpm-helper
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(postun): rpm-helper
Conflicts: openais <= 0.89, openais-devel <= 0.89

%if %{buildtrunk}
BuildRequires: autoconf automake
%endif
BuildRequires: nss-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description 
This package contains the Corosync Cluster Engine Executive, several default
APIs and libraries, default configuration files, and an init script.

%package -n %{libname}
Summary: The Corosync Cluster Engine Libraries
Group: System/Libraries
Conflicts: corosync < 0.92-7
Obsoletes: corosynclib < 1.1.0

%description -n %{libname}
This package contains corosync libraries.

%package -n %{libnamedevel}
Summary: The Corosync Cluster Engine Development Kit
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Requires: pkgconfig
Provides: corosync-devel = %{version} corosynclibs-devel = %{version}
Obsoletes: corosync-devel < 0.92-7
Obsoletes: corosynclibs-devel < 1.1.0

%description -n %{libnamedevel}
This package contains include files and man pages used to develop using
The Corosync Cluster Engine APIs.

%prep
%setup -q -n corosync-%{version}
%patch1 -p1 -b .linkrt

#if %{buildtrunk}
./autogen.sh
#endif

#%{_configure}	CFLAGS="$(echo '%{optflags}')" \
#		--prefix=%{_prefix} \
#		--sysconfdir=%{_sysconfdir} \
#		--localstatedir=%{_localstatedir} \
#		--with-lcrso-dir=%{_libexecdir}/lcrso \
#		--libdir=%{_libdir}
%configure --with-lcrso-dir=%{_libexecdir}/lcrso

%build
%make

%install
rm -rf %{buildroot}

#make install DESTDIR=%{buildroot}
%makeinstall_std
install -d %{buildroot}%{_initddir}
mv %{buildroot}/etc/init.d/* %{buildroot}/%{_initddir}
#install -m 755 init/generic %{buildroot}%{_initddir}/corosync

## tree fixup
# drop static libs
rm -f %{buildroot}%{_libdir}/*.a
# drop docs and html docs for now
rm -rf %{buildroot}%{_docdir}/*

%clean
rm -rf %{buildroot}
%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
[ "$1" -ge "1" ] && /sbin/service corosync condrestart &>/dev/null || :

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files 
%defattr(-,root,root,-)
%doc LICENSE SECURITY
%{_sbindir}/corosync*
%dir %{_sysconfdir}/corosync
%dir %{_sysconfdir}/corosync/uidgid.d
%config(noreplace) %{_sysconfdir}/corosync/corosync.conf.example
%{_initddir}/corosync
%dir %{_libexecdir}/lcrso
%{_libexecdir}/lcrso/*.lcrso
%dir %{_localstatedir}/lib/corosync
%{_mandir}/man8/corosync_overview.8*
%{_mandir}/man8/corosync-*.8*
%{_mandir}/man8/corosync.8*
%{_mandir}/man5/corosync.conf.5*

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*

%files -n %{libnamedevel}
%defattr(-,root,root,-)
%doc LICENSE README.devmap
%{_includedir}/corosync/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3*
%{_mandir}/man8/cpg_overview.8*
%{_mandir}/man8/evs_overview.8*
%{_mandir}/man8/confdb_overview.8*
%{_mandir}/man8/logsys_overview.8*
%{_mandir}/man8/votequorum_overview.8*
%{_mandir}/man8/coroipc_overview.8*
%{_mandir}/man8/sam_overview.8*
