# NOTE: tests use predictable paths in /tmp:
#    rm -rf /tmp/hdtest_perm
#    rm -rf /tmp/hdtest_out

# Conditional build:
%bcond_without	tests	# do not perform "make test"

%include	/usr/lib/rpm/macros.perl
Summary:	Documentation generator
Name:		headerdoc
Version:	8.9.5
Release:	1
License:	Apple Public Source License
Group:		Development/Tools
URL:		http://developer.apple.com/opensource/tools/headerdoc.html
Source0:	http://www.opensource.apple.com/tarballs/headerdoc/%{name}-%{version}.tar.gz
# Source0-md5:	ebc481aa8344d1fc7c9e8117e1ac2203
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-FreezeThaw
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HeaderDoc is a tool for generating HTML reference documentation from
comments in C or C++ header files.

%prep
%setup -q

%build
%{__make} -C xmlman -j1 \
	CC="%{__cc}" \
	LOCALCFLAGS="%{rpmcflags}" \
	ARCH=$(uname) \
	%{nil}

%if %{with tests}
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} installsub \
	DSTROOT=$RPM_BUILD_ROOT

# introduction to man pages
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man5/manpages.5*
# link to xml2man
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/mpgl.1

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/testsuite

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gatherheaderdoc
%attr(755,root,root) %{_bindir}/headerdoc2html
%attr(755,root,root) %{_bindir}/hdxml2manxml
%attr(755,root,root) %{_bindir}/resolveLinks
%attr(755,root,root) %{_bindir}/xml2man
%{_datadir}/%{name}/Availability.list
%{_datadir}/%{name}/Modules
%{_datadir}/%{name}/conf
%{_mandir}/man1/gatherheaderdoc.1*
%{_mandir}/man1/hdxml2manxml.1*
%{_mandir}/man1/headerdoc.1
%{_mandir}/man1/headerdoc2html.1*
%{_mandir}/man1/resolveLinks.1*
%{_mandir}/man1/xml2man.1*
