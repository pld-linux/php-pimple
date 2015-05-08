#
# Conditional build:
%bcond_without	tests		# build without tests

%define		pkgname	pimple
%define		php_min_version 5.3.0
Summary:	A simple dependency injection container for PHP
Name:		php-%{pkgname}
Version:	3.0.0
Release:	1
License:	MIT
Group:		Development/Languages/PHP
Source0:	https://github.com/silexphp/Pimple/archive/v%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	09c5470d679cf31187289aa89d039926
URL:		http://pimple.sensiolabs.org/
%if %{with tests}
BuildRequires:	phpab
BuildRequires:	phpunit
%endif
Requires:	php(core) >= %{php_min_version}
Requires:	php(spl)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		namespace	Pimple

%description
Pimple is a small dependency injection container for PHP that consists
of just one file and one class.

%prep
%setup -qn Pimple-%{version}

%build
%if %{with tests}
# roll our own loader to run tests
# (can't seem to get it to load the fixtures with --include-path any more)
phpab --output bootstrap.php --exclude '*Test.php' --basedir . src
phpunit --bootstrap bootstrap.php
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_data_dir}
cp -a src/%{namespace} $RPM_BUILD_ROOT%{php_data_dir}
# clean out tests
rm -r $RPM_BUILD_ROOT%{php_data_dir}/%{namespace}/Tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst LICENSE
%{php_data_dir}/%{namespace}
