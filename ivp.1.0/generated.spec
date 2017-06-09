# The name of your package
Name: ivp.1.0

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
%attr(0644, root, root) "/usr/local/bin/example_file"

