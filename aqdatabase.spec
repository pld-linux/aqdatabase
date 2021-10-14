#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	AqDatabase - database used by AqFinance
Summary(pl.UTF-8):	AqDatabase - baza danych wykorzystywana przez AqFinance
Name:		aqdatabase
Version:	1.0.15
Release:	1
License:	LGPL v2.1+
Group:		Libraries
# https://www.aquamaniac.de/sites/download/packages.php
#Source0:	https://www.aquamaniac.de/sites/download/download.php?package=14&release=200&file=01&dummy=/%{name}-%{version}.tar.gz
Source0:	https://www.aquamaniac.de/rdm/attachments/download/346/%{name}-%{version}.tar.gz
# Source0-md5:	63d6af04a3fc994dd79e17fa8620d30f
Patch0:		%{name}-pc.patch
URL:		https://www.aquamaniac.de/sites/aqfinance/
#BuildRequires:	autoconf >= 2.60
#BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	gmp-devel
BuildRequires:	gwenhywfar-devel >= 5.2.0.0
#BuildRequires:	libtool
Requires:	gwenhywfar >= 4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AqDatabase - database used by AqFinance.

%description -l pl.UTF-8
AqDatabase - baza danych wykorzystywana przez AqFinance.

%package devel
Summary:	Header files for AqDatabase library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki AqDatabase
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gwenhywfar-devel >= 4

%description devel
Header files for AqDatabase library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki AqDatabase.

%package static
Summary:	Static AqDatabase library
Summary(pl.UTF-8):	Statyczna biblioteka AqDatabase
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static AqDatabase library.

%description static -l pl.UTF-8
Statyczna biblioteka AqDatabase.

%prep
%setup -q
%patch0 -p1

# workaround to build without headers installed
install -d aqdatabase
cd aqdatabase
ln -sf ../src/lib/*.h .
ln -sf ../src/*.h .

%build
%configure \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libaqdatabase.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/aqdbtool
%attr(755,root,root) %{_bindir}/aqfscheck
%attr(755,root,root) %{_libdir}/libaqdatabase.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaqdatabase.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaqdatabase.so
%{_includedir}/aqdatabase
%{_datadir}/aqdatabase
%{_pkgconfigdir}/aqdatabase.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libaqdatabase.a
%endif
