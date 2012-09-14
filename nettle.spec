%define nettlemajor 4
%define hogweedmajor 2
%define libnettlename %mklibname nettle %nettlemajor
%define libhogweedname %mklibname hogweed %hogweedmajor
%define develname %mklibname -d nettle

Name:		nettle
Summary:	Nettle cryptographic library
Epoch:		1
Version:	2.5
Release:	2
License:	LGPLv2
Group:		System/Libraries
URL:		http://www.lysator.liu.se/~nisse/nettle/
Source0:	http://www.lysator.liu.se/~nisse/archive/%name-%{version}.tar.gz
BuildRequires:	autoconf
BuildRequires:	openssl-devel
BuildRequires:	libgmp-devel
BuildRequires:	recode
Requires:       %{libnettlename} = %{EVRD}
Requires:       %{libhogweedname} = %{EVRD}

%description
Nettle is a cryptographic library that is designed to fit easily in more or
less any context: 
In crypto toolkits for object-oriented languages (C++, Python, Pike, ...),
in applications like LSH or GNUPG, or even in kernel space. 

%package -n %{libnettlename}
Group:		System/Libraries
Summary:	Nettle shared library

%description -n %{libnettlename}
This is the shared library part of the Nettle library.

%package -n %{libhogweedname}
Group:          System/Libraries
Summary:        Hogweed shared library

%description -n %{libhogweedname}
This is the shared library part of the Hogweed library.

%package -n %develname
Group:		Development/C++
Summary:	Header files for compiling against Nettle library
Provides:	%name-devel = %{EVRD}
Requires:	%{libnettlename} = %{EVRD}
Requires:	%{libhogweedname} = %{EVRD}
Obsoletes:	%mklibname -d nettle 0

%description -n %develname
This is the development package of nettle. Install it if you want to 
compile programs using this library.

%prep
%setup -q

%build
%configure2_5x --enable-shared
%make

%check
%make check

%install
%makeinstall_std
recode ISO-8859-1..UTF-8 %buildroot%_infodir/*.info
recode ISO-8859-1..UTF-8 ChangeLog

# why are not libs stripped by spec-helper?
strip --strip-unneeded %{buildroot}%{_libdir}/libnettle.so.%{nettlemajor}.*
strip --strip-unneeded %{buildroot}%{_libdir}/libhogweed.so.%{hogweedmajor}.*

%files
%{_bindir}/*
%{_infodir}/*

%files -n %{libnettlename}
%{_libdir}/libnettle.so.%{nettlemajor}*

%files -n %{libhogweedname}
%{_libdir}/libhogweed.so.%{hogweedmajor}*

%files -n %develname
%doc AUTHORS TODO ChangeLog
%_libdir/libnettle.a
%_libdir/libhogweed.a
%_libdir/libnettle.so
%_libdir/libhogweed.so
%_libdir/pkgconfig/*.pc
%_includedir/nettle/

