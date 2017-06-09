# The name of your package
Name: my-new-rpm

# A short summary of your package
Summary: None

# The version of your package
Version: 1.0

# The release number of your package
Release: 1

# Any license you wish to list
License: GNU GPL

# What group this RPM would typically reside in
Group: Applications/System

# Who packaged this RPM
Packager: gld <yangsir@tests.com>

# The build architecture of this RPM (noarch/x86_64/i386/etc)
Buildarch: noarch

# You generally should not need to mess with this setting
Buildroot: %{_tmppath}/%{name}

# Change this extension to change the compression level in your RPM
#  tar / tar.gz / tar.bz2
Source0: %{name}.tar

# If you are having trouble building a package and need to disable
#  automatic dependency/provides checking, uncomment this:
# AutoReqProv: no

# If this package has prerequisites, uncomment this line and
#  list them here - examples are already listed
#Requires: bash, python >= 2.7

# A more verbose description of your package
%description
None

# You probably do not need to change this
%define debug_package %{nil}


%prep
%setup -q -c

%build

%install
rsync -a . %{buildroot}/

%clean
rm -rf %{buildroot}

%pre

%post

%preun

%postun

#%trigger

#%triggerin

#%triggerun

%changelog
* Fri Jun 09 2017 gld <yangsir@tests.com>
- Initial version.

%files
%attr(0755, root, root) %dir "/usr/local/bin/ivpmonitor-first-release"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/colors.py"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/colors.pyc"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/colors.pyo"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/decoder.py"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/decoder.pyc"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/decoder.pyo"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/decoderlog"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/encoder.py"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/encoder.pyc"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/encoder.pyo"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/encoderlog"
%attr(0755, root, root) "/usr/local/bin/ivpmonitor-first-release/install"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/ivp.py"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/ivp.pyc"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/ivp.pyo"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/ivpdb.py"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/ivpdb.pyc"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/ivpdb.pyo"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/ivplog"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/monitor.py"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/monitor.pyc"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/monitor.pyo"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/smip.py"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/smip.pyc"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/smip.pyo"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/smiplog"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/start.py"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/start.pyc"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/start.pyo"
%attr(0755, root, root) %dir "/usr/local/bin/ivpmonitor-first-release/static"
%attr(0755, root, root) %dir "/usr/local/bin/ivpmonitor-first-release/templates"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/yangtest.py"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/yangtest.pyc"
%attr(0644, root, root) "/usr/local/bin/ivpmonitor-first-release/yangtest.pyo"

