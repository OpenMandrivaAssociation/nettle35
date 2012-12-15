# Just a hack because rpmlint rejects build with unstripped libs
%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define major 4
%define hogweedmajor 2
%define libname %mklibname nettle %{major}
%define libhogweedname %mklibname hogweed %{hogweedmajor}
%define devname %mklibname -d nettle

Name:		nettle
Summary:	Nettle cryptographic library
Epoch:		1
Version:	2.5
Release:	1
License:	LGPLv2
Group:		System/Libraries
URL:		http://www.lysator.liu.se/~nisse/nettle/
Source0:	http://www.lysator.liu.se/~nisse/archive/%{name}-%{version}.tar.gz
Source1:	http://www.lysator.liu.se/~nisse/archive/%{name}-%{version}.tar.gz.sig
BuildRequires:	recode
BuildRequires:	gmp-devel
BuildRequires:	pkgconfig(openssl)

%description
Nettle is a cryptographic library that is designed to fit easily in more or
less any context:
In crypto toolkits for object-oriented languages (C++, Python, Pike, ...),
in applications like LSH or GNUPG, or even in kernel space. 

%package -n %{libname}
Group:		System/Libraries
Summary:	Nettle shared library

%description -n %{libname}
This is the shared library part of the Nettle library.

%package -n %{libhogweedname}
Group:		System/Libraries
Summary:	Hogweed shared library

%description -n %{libhogweedname}
This is the shared library part of the Hogweed library.

%package -n %{devname}
Group:		Development/C++
Summary:	Header files for compiling against Nettle library
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	%{libhogweedname} = %{EVRD}

%description -n %{devname}
This is the development package of nettle. Install it if you want to 
compile programs using this library.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
	--enable-shared

%make

%check
%make check

%install
%makeinstall_std
recode ISO-8859-1..UTF-8 %{buildroot}%{_infodir}/*.info
recode ISO-8859-1..UTF-8 ChangeLog

%files
%{_bindir}/*
%{_infodir}/*

%files -n %{libname}
%{_libdir}/libnettle.so.%{major}*

%files -n %{libhogweedname}
%{_libdir}/libhogweed.so.%{hogweedmajor}*

%files -n %{devname}
%doc AUTHORS TODO ChangeLog
%{_libdir}/libnettle.so
%{_libdir}/libhogweed.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/nettle/



%changelog
* Mon Mar 19 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1:2.4-1
+ Revision: 785708
- Update to 2.4, improve spec file

* Wed Oct 27 2010 Funda Wang <fwang@mandriva.org> 1:2.1-1mdv2011.0
+ Revision: 589577
- new version 2.1

* Sat Jul 25 2009 Crispin Boylan <crisb@mandriva.org> 1:2.0-1mdv2010.0
+ Revision: 399777
- Initial package for mandriva
- create nettle

