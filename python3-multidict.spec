#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	multidict implementation
Summary(pl.UTF-8):	Implementacja multidict
Name:		python3-multidict
Version:	6.0.4
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/multidict/
Source0:	https://files.pythonhosted.org/packages/source/m/multidict/multidict-%{version}.tar.gz
# Source0-md5:	ec06a613d871dadfb66f2be3a1f2f3fa
URL:		https://pypi.org/project/multidict/
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-setuptools >= 1:40
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.752
%if %{with doc}
BuildRequires:	python3-alabaster
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Multidict is dict-like collection of key-value pairs where key might
be occurred more than once in the container.

%description -l pl.UTF-8
Multidict to podobna do dict kolekcja par klucz-wartość, gdzie klucz
może wystąpić więcej niż raz w danym kontenerze.

%package apidocs
Summary:	API documentation for Python multidict module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona multidict
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python multidict module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona multidict.

%prep
%setup -q -n multidict-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin" \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%dir %{py3_sitedir}/multidict
%attr(755,root,root) %{py3_sitedir}/multidict/_multidict.cpython-*.so
%{py3_sitedir}/multidict/*.py
%{py3_sitedir}/multidict/__init__.pyi
%{py3_sitedir}/multidict/py.typed
%{py3_sitedir}/multidict/__pycache__
%{py3_sitedir}/multidict-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
