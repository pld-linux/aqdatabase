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
#Source0Download: https://www.aquamaniac.de/rdm/projects/aqdatabase/files
Source0:	https://www.aquamaniac.de/rdm/attachments/download/346/%{name}-%{version}.tar.gz
# Source0-md5:	63d6af04a3fc994dd79e17fa8620d30f
Patch0:		%{name}-pc.patch
URL:		https://www.aquamaniac.de/rdm/projects/aqdatabase
#BuildRequires:	autoconf >= 2.60
#BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	gmp-devel
BuildRequires:	gwenhywfar-devel >= 5.2.0.0
BuildRequires:	pkgconfig
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
%patch -P0 -p1

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
%{_libdir}/libaqdatabase.so.*.*.*
%ghost %{_libdir}/libaqdatabase.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/libaqdatabase.so
%{_includedir}/aqdatabase
%dir %{_datadir}/aqdatabase
%{_datadir}/aqdatabase/typemaker2
%{_pkgconfigdir}/aqdatabase.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libaqdatabase.a
%endif
