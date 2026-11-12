#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit and benchmark tests

Summary:	multidict implementation
Summary(pl.UTF-8):	Implementacja multidict
Name:		python3-multidict
Version:	7.2.1
Release:	2
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/multidict/
Source0:	https://files.pythonhosted.org/packages/source/m/multidict/multidict-%{version}.tar.gz
# Source0-md5:	3f9f08805cdffa6469e13ef33c93d091
Patch0:		%{name}-testcyapi-uaf.patch
URL:		https://pypi.org/project/multidict/
BuildRequires:	python3-devel >= 1:3.11
BuildRequires:	python3-setuptools >= 1:77
%if %{with tests}
BuildRequires:	python3-Cython >= 3.0
BuildRequires:	python3-hypothesis
BuildRequires:	python3-objgraph
BuildRequires:	python3-psutil
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-benchmark
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest_codspeed
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.752
%if %{with doc}
BuildRequires:	python3-alabaster
BuildRequires:	python3-sphinxcontrib-towncrier
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.11
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
%patch -P0 -p1

%build
%py3_build

%if %{with tests}
%{__mv} multidict{,.away}

# pytest_codspeed defines the benchmark fixture only when pytest_benchmark
# is not importable, so load pytest_benchmark too to have it either way;
# test_circular_imports runs python -I, which ignores PYTHONPATH and so
# imports the system multidict instead of the built one
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_codspeed.plugin,pytest_benchmark.plugin \
PYTHONPATH=$(readlink -f build-3/lib.*) \
%{__python3} -m pytest tests \
	--benchmark-disable \
	--ignore tests/test_circular_imports.py

%{__mv} multidict{.away,}
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

# test-only C API exercisers; _testcyapi is built only when Cython happens to be installed
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/multidict/_testcapi.cpython-*.so
%{__rm} -f $RPM_BUILD_ROOT%{py3_sitedir}/multidict/_testcyapi.cpython-*.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%dir %{py3_sitedir}/multidict
%attr(755,root,root) %{py3_sitedir}/multidict/_multidict.cpython-*.so
%{py3_sitedir}/multidict/*.py
%{py3_sitedir}/multidict/__init__.pxd
%{py3_sitedir}/multidict/multidict_capi.h
%{py3_sitedir}/multidict/multidict_capi_struct.h
%{py3_sitedir}/multidict/py.typed
%{py3_sitedir}/multidict/__pycache__
%{py3_sitedir}/multidict-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
