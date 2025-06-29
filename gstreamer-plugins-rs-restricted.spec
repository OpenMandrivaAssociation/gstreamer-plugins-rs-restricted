%define _name gst-plugins-rs
%define gst_branch 1.0
# Disable csound for now, bring issue upstream
#%%global __requires_exclude pkgconfig\\(csound\\)

##########################
# Hardcode PLF build
%define build_plf 1
##########################

%if %{build_plf}
%define distsuffix plf
# make EVR of plf build higher than regular to allow update
%define extrarelsuffix plf
%define build_vvdec 1
%endif

Name:           gstreamer-plugins-rs
Version:        1.26.3
# Make sure that release in restriected is higher than in main
Release:        100
Summary:        GStreamer Streaming-Media Framework Plug-Ins
License:        LGPL-2.1-or-later
Group:          Productivity/Multimedia/Other
URL:            https://gitlab.freedesktop.org/gstreamer/gst-plugins-rs
Source0:        https://gitlab.freedesktop.org/gstreamer/gst-plugins-rs/-/archive/gstreamer-%{version}/gst-plugins-rs-gstreamer-%{version}.tar.bz2
Source2:        vendor.tar.xz
#Source3:        cargo_config
Source4:        gstreamer-plugins-rs.appdata.xml

BuildRequires:	rust
BuildRequires:	cargo
BuildRequires:  cargo-c
BuildRequires:  rust-packaging
BuildRequires:  clang
# Disable csound for now, bring issue upstream
#BuildRequires:  csound-devel
BuildRequires:  llvm
BuildRequires:  git
BuildRequires:  meson >= 0.60
BuildRequires:  nasm
BuildRequires:  pkgconfig
BuildRequires:  python3dist(tomli)
BuildRequires:  zstd
BuildRequires:  pkgconfig(cairo) >= 1.10.0
BuildRequires:  pkgconfig(dav1d)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gstreamer-webrtc-1.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libsodium)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(rav1e)
BuildRequires:  pkgconfig(libvvdec)
# may be needed sson when gst adds encoder. To not lose this, let's add BR right away.
BuildRequires:  pkgconfig(libvvenc)
Requires:       gstreamer1.0-tools
Requires:       gstreamer1.0-plugins-base

%description
GStreamer is a streaming media framework based on graphs of filters
that operate on media data. Applications using this library can do
anything media-related, from real-time sound processing to playing
videos. Its plug-in-based architecture means that new data types or
processing capabilities can be added simply by installing new
plug-ins.

This package provides various plugins written in Rust.

%package devel
Summary:        GStreamer Streaming-Media Framework Plug-Ins development files
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}
#Requires:       csound-devel

%description devel
GStreamer is a streaming media framework based on graphs of filters
that operate on media data. Applications using this library can do
anything media-related, from real-time sound processing to playing
videos. Its plug-in-based architecture means that new data types or
processing capabilities can be added simply by installing new
plug-ins.

This package contains the pkgconfig development files for the rust
plugins.

%prep
%autosetup -n gst-plugins-rs-gstreamer-%{version} -a2 -p1
#cargo_prep -v vendor
mkdir -p .cargo
cat >> .cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source."git+https://github.com/gtk-rs/gtk-rs-core?branch=main"]
git = "https://github.com/gtk-rs/gtk-rs-core"
branch = "main"
replace-with = "vendored-sources"

[source."git+https://github.com/gtk-rs/gtk4-rs?branch=main"]
git = "https://github.com/gtk-rs/gtk4-rs"
branch = "main"
replace-with = "vendored-sources"

[source."git+https://github.com/rust-av/ffv1.git?rev=bd9eabfc14c9ad53c37b32279e276619f4390ab8"]
git = "https://github.com/rust-av/ffv1.git"
rev = "bd9eabfc14c9ad53c37b32279e276619f4390ab8"
replace-with = "vendored-sources"

[source."git+https://github.com/rust-av/flavors"]
git = "https://github.com/rust-av/flavors"
replace-with = "vendored-sources"

[source."git+https://gitlab.freedesktop.org/gstreamer/gstreamer-rs?branch=main"]
git = "https://gitlab.freedesktop.org/gstreamer/gstreamer-rs"
branch = "main"
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
# Disable csound for now, bring issue upstream
#export CSOUND_LIB_DIR=%%{_libdir}
export RUSTFLAGS="%{build_rustflags}"

%meson \
	--default-library=shared \
	-Ddoc=disabled \
  	-Dwebp=enabled \
	-Ddav1d=enabled \
  	-Drav1e=enabled \
	-Dsodium=enabled \
	-Dcsound=disabled \
%if !%{build_vvdec} 
 	-Dvvdec=disabled \
%else
  	-Dvvdec=enabled \
%endif
	-Daws=disabled

%meson_build

%install
export RUSTFLAGS="%{build_rustflags}"
%meson_install
mkdir -p %{buildroot}%{_datadir}/appdata
cp %{SOURCE4} %{buildroot}%{_datadir}/appdata/

%files
%license LICENSE-APACHE LICENSE-LGPLv2 LICENSE-MIT
%doc README.md
%dir %{_libdir}/gstreamer-%{gst_branch}
%{_libdir}/gstreamer-%{gst_branch}/libgstcdg.so
%{_libdir}/gstreamer-%{gst_branch}/libgstclaxon.so
# Disable csound for now, bring issue upstream
#%%{_libdir}/gstreamer-%%{gst_branch}/libgstcsound.so
%{_libdir}/gstreamer-%{gst_branch}/libgstdav1d.so
%{_libdir}/gstreamer-%{gst_branch}/libgstfallbackswitch.so
%{_libdir}/gstreamer-%{gst_branch}/libgstffv1.so
%{_libdir}/gstreamer-%{gst_branch}/libgstfmp4.so
%{_libdir}/gstreamer-%{gst_branch}/libgstgif.so
%{_libdir}/gstreamer-%{gst_branch}/libgstgtk4.so
%{_libdir}/gstreamer-%{gst_branch}/libgsthlssink3.so
%{_libdir}/gstreamer-%{gst_branch}/libgsthsv.so
%{_libdir}/gstreamer-%{gst_branch}/libgstjson.so
%{_libdir}/gstreamer-%{gst_branch}/libgstlewton.so
%{_libdir}/gstreamer-%{gst_branch}/libgstlivesync.so
%{_libdir}/gstreamer-%{gst_branch}/libgstmp4.so
%{_libdir}/gstreamer-%{gst_branch}/libgstndi.so
%{_libdir}/gstreamer-%{gst_branch}/libgstraptorq.so
%{_libdir}/gstreamer-%{gst_branch}/libgstrav1e.so
%{_libdir}/gstreamer-%{gst_branch}/libgstregex.so
%{_libdir}/gstreamer-%{gst_branch}/libgstreqwest.so
%{_libdir}/gstreamer-%{gst_branch}/libgstrsaudiofx.so
%{_libdir}/gstreamer-%{gst_branch}/libgstrsclosedcaption.so
%{_libdir}/gstreamer-%{gst_branch}/libgstrsfile.so
%{_libdir}/gstreamer-%{gst_branch}/libgstrsflv.so
%{_libdir}/gstreamer-%{gst_branch}/libgstrsonvif.so
%{_libdir}/gstreamer-%{gst_branch}/libgstrspng.so
%{_libdir}/gstreamer-%{gst_branch}/libgstrsrtp.so
%{_libdir}/gstreamer-%{gst_branch}/libgstrstracers.so
%{_libdir}/gstreamer-%{gst_branch}/libgstrsvideofx.so
%{_libdir}/gstreamer-%{gst_branch}/libgstrswebp.so
%{_libdir}/gstreamer-%{gst_branch}/libgstrswebrtc.so
%{_libdir}/gstreamer-%{gst_branch}/libgstsodium.so
%{_libdir}/gstreamer-%{gst_branch}/libgstspotify.so
%{_libdir}/gstreamer-%{gst_branch}/libgsttextahead.so
%{_libdir}/gstreamer-%{gst_branch}/libgsttextwrap.so
%{_libdir}/gstreamer-%{gst_branch}/libgstthreadshare.so
%{_libdir}/gstreamer-%{gst_branch}/libgsttogglerecord.so
%{_libdir}/gstreamer-%{gst_branch}/libgsturiplaylistbin.so
%{_libdir}/gstreamer-%{gst_branch}/libgstwebrtchttp.so
%{_libdir}/gstreamer-%{gst_branch}/libgstgopbuffer.so
%{_libdir}/gstreamer-%{gst_branch}/libgsthlsmultivariantsink.so
%{_libdir}/gstreamer-%{gst_branch}/libgstmpegtslive.so
%{_libdir}/gstreamer-%{gst_branch}/libgstoriginalbuffer.so
%{_libdir}/gstreamer-%{gst_branch}/libgstquinn.so
%{_libdir}/gstreamer-%{gst_branch}/libgstrsinter.so
%{_libdir}/gstreamer-%{gst_branch}/libgstelevenlabs.so
%{_libdir}/gstreamer-%{gst_branch}/libgstrsanalytics.so
%{_libdir}/gstreamer-%{gst_branch}/libgstrsrtsp.so
%{_libdir}/gstreamer-%{gst_branch}/libgstspeechmatics.so
%{_libdir}/gstreamer-%{gst_branch}/libgststreamgrouper.so
%{_libdir}/gstreamer-%{gst_branch}/libgstvvdec.so
%dir %{_datadir}/appdata
%{_datadir}/appdata/gstreamer-plugins-rs.appdata.xml
%{_bindir}/gst-webrtc-signalling-server

%files devel
%{_libdir}/pkgconfig/*.pc
