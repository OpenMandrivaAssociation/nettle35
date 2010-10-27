%define	name	nettle
%define	version	2.1
%define epoch 1 
%define nettlemajor 4
%define hogweedmajor 2
%define libnettlename %mklibname nettle %nettlemajor
%define libhogweedname %mklibname hogweed %hogweedmajor
%define develname %mklibname -d nettle

Name:		%{name}
Summary:	Nettle cryptographic library
Version:	%{version}
Release:	%mkrel 1
License:	GPL
Group:		System/Libraries
URL:		http://www.lysator.liu.se/~nisse/nettle/
Source:		http://www.lysator.liu.se/~nisse/archive/%name-%{version}.tar.gz
Epoch: %epoch
BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	autoconf
BuildRequires:	openssl-devel
BuildRequires:	libgmp-devel
Requires:       %{libnettlename} = %epoch:%version-%release
Requires:       %{libhogweedname} = %epoch:%version-%release

%description
Nettle is a cryptographic library that is designed to fit easily in more or less any context: 
In crypto toolkits for object-oriented languages (C++, Python, Pike, ...), in applications 
like LSH or GNUPG, or even in kernel space. 

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
Provides:	%name-devel = %epoch:%version-%release
Requires:	%{libnettlename} = %epoch:%version-%release
Requires:	%{libhogweedname} = %epoch:%version-%release
Obsoletes:	%mklibname -d nettle 0

%description -n %develname
This is the development package of nettle. Install it if you want to 
compile programs using this library.

%prep
%setup -q

%build
%configure2_5x --enable-shared
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_infodir}/*

%files -n %{libnettlename}
%defattr(-,root,root)
%{_libdir}/libnettle.so.%{nettlemajor}*

%files -n %{libhogweedname}
%{_libdir}/libhogweed.so.%{hogweedmajor}*

%files -n %develname
%defattr(-,root,root)
%doc AUTHORS TODO ChangeLog
%{_libdir}/libnettle.a
%{_libdir}/libhogweed.a
%{_libdir}/libnettle.so
%{_libdir}/libhogweed.so
%{_includedir}/nettle/

