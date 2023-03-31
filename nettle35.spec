# Just a hack because rpmlint rejects build with unstripped libs
#% define _enable_debug_packages %{nil}
#% define debug_package %{nil}
%define _disable_lto 1

%global optflags %{optflags} -O3

%bcond_with bootstrap

# (tpg) enable PGO build
%bcond_without pgo

%define major 7
%define hogweedmajor 5
%define libname %mklibname nettle %{major}
%define libhogweed %mklibname hogweed %{hogweedmajor}

Summary:	Nettle cryptographic library
Name:		nettle35
Epoch:		1
Version:	3.5.1
Release:	3
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.lysator.liu.se/~nisse/nettle/
Source0:	https://ftp.gnu.org/gnu/nettle/nettle-%{version}.tar.gz
BuildRequires:	recode
BuildRequires:	gmp-devel
BuildRequires:	texinfo
%ifnarch riscv64
BuildRequires:	pkgconfig(valgrind)
%endif
%if %{with bootstrap}
BuildRequires:	pkgconfig(openssl)
%endif

%description
Nettle is a cryptographic library that is designed to fit easily in more or
less any context:
In crypto toolkits for object-oriented languages (C++, Python, Pike, ...),
in applications like LSH or GNUPG, or even in kernel space.

#files
#{_bindir}/*

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Nettle shared library
Group:		System/Libraries

%description -n %{libname}
This is the shared library part of the Nettle library.

%files -n %{libname}
%{_libdir}/libnettle.so.%{major}*

#----------------------------------------------------------------------------

%if !%{with bootstrap}
%package -n %{libhogweed}
Summary:	Hogweed shared library
Group:		System/Libraries

%description -n %{libhogweed}
This is the shared library part of the Hogweed library.

%files -n %{libhogweed}
%{_libdir}/libhogweed.so.%{hogweedmajor}*
%endif

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n nettle-%{version}
%config_update
# Disable -ggdb3 which makes debugedit unhappy
sed s/ggdb3/g/ -i configure
#sed 's/ecc-192.c//g' -i Makefile.in
#sed 's/ecc-224.c//g' -i Makefile.in

%build
mkdir -p bfd
ln -s %{_bindir}/ld.bfd bfd/ld
export PATH=$PWD/bfd:$PATH
# enable-x86-aesni without enable-fat likely causes bug 2408
# Inline asm isn't compatible with clang style asm
CFLAGS="%{optflags} -fno-integrated-as"

%if %{with pgo}
export LLVM_PROFILE_FILE=%{name}-%p.profile.d
export LD_LIBRARY_PATH="$(pwd)"
CFLAGS="%{optflags} -fprofile-instr-generate" \
CXXFLAGS="%{optflags} -fprofile-instr-generate" \
FFLAGS="$CFLAGS_PGO" \
FCFLAGS="$CFLAGS_PGO" \
LDFLAGS="%{ldflags} -fprofile-instr-generate" \
%configure \
	--enable-static \
	--disable-openssl \
%ifarch %{arm} %{aarch64}
	--enable-arm-neon \
%endif
%ifarch %{x86_64}
	--enable-x86-aesni \
%ifnarch znver1
	--enable-fat \
%endif
%endif
	--enable-shared

%make_build
make check

unset LD_LIBRARY_PATH
unset LLVM_PROFILE_FILE
llvm-profdata merge --output=%{name}.profile *.profile.d

make clean

CFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
CXXFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
LDFLAGS="%{ldflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
%endif
%configure \
	--enable-static \
	--disable-openssl \
	--disable-x86-sha-ni \
%ifarch %{arm} %{aarch64}
	--enable-arm-neon \
%endif
%ifarch %{x86_64}
	--enable-x86-aesni \
%ifnarch znver1
	--enable-fat \
%endif
%endif
	--enable-shared

%make_build

%check
%make check

%install
%make_install
recode ISO-8859-1..UTF-8 ChangeLog

rm -rf \
	%{buildroot}%{_bindir} \
	%{buildroot}%{_libdir}/*.so \
	%{buildroot}%{_libdir}/*.a \
	%{buildroot}%{_libdir}/pkgconfig \
	%{buildroot}%{_includedir} \
	%{buildroot}%{_infodir}
