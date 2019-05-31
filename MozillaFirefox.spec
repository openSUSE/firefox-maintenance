#
# spec file for package MozillaFirefox
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
#               2006-2018 Wolfgang Rosenauer
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


# changed with every update
%define major 68
%define mainver %major.0
%define version_postfix b5
%define update_channel esr
%define branding 1
%define releasedate 20190507001600
%define source_prefix firefox-%{mainver}

# PIE, full relro (x86_64 for now)
%define build_hardened 1

# Firefox only supports i686
%ifarch %ix86
ExclusiveArch:  i586 i686
BuildArch:      i686
%{expand:%%global optflags %(echo "%optflags"|sed -e s/i586/i686/) -march=i686 -mtune=generic}
%endif

# general build definitions
%define progname firefox
%define pkgname  MozillaFirefox
%define appname  Firefox
%define progdir %{_prefix}/%_lib/%{progname}
%define gnome_dir     %{_prefix}
%define desktop_file_name %{progname}
%define firefox_appid \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
%define __provides_exclude ^lib.*\\.so.*$
%define __requires_exclude ^(libmoz.*|liblgpllibs.*|libxul.*)$
%define localize 1
%ifarch %ix86 x86_64
%define crashreporter 1
%else
%define crashreporter 0
%endif

Name:           %{pkgname}
BuildRequires:  Mesa-devel
BuildRequires:  alsa-devel
BuildRequires:  autoconf213
BuildRequires:  dbus-1-glib-devel
BuildRequires:  fdupes
BuildRequires:  memory-constraints
%if 0%{?suse_version} <= 1320
BuildRequires:  gcc7-c++
%else
BuildRequires:  gcc-c++
%endif
BuildRequires:  cargo
BuildRequires:  libXcomposite-devel
BuildRequires:  libcurl-devel
BuildRequires:  libidl-devel
BuildRequires:  libiw-devel
BuildRequires:  libnotify-devel
BuildRequires:  libproxy-devel
BuildRequires:  makeinfo
BuildRequires:  mozilla-nspr-devel >= 4.19
BuildRequires:  mozilla-nss-devel >= 3.36.6
BuildRequires:  python-devel
BuildRequires:  python2-xml
# Rust version bump for packaging changes only, Firefox can build with older rust
# Upstream Firefox ESR 60.x presumes rust-1.24
# openSUSE and SLE use improved packaging in rust >= 1.30
# Use RUSTFLAGS="--cap-lints allow" to allow building, see below
BuildRequires:  rust >= 1.34
BuildRequires:  startup-notification-devel
BuildRequires:  unzip
BuildRequires:  update-desktop-files
BuildRequires:  xorg-x11-libXt-devel
BuildRequires:  yasm
BuildRequires:  zip
BuildRequires:  rust-cbindgen
BuildRequires:  nodejs10 >= 8.11
BuildRequires:  nasm
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  pkgconfig(gdk-x11-2.0)
BuildRequires:  pkgconfig(glib-2.0) >= 2.22
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gtk+-2.0) >= 2.18.0
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.4.0
BuildRequires:  pkgconfig(gtk+-unix-print-2.0)
BuildRequires:  pkgconfig(gtk+-unix-print-3.0)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(libpulse)
%if 0%{?suse_version} > 1320
BuildRequires:  llvm-clang-devel >= 3.9.0
%else
# this covers the workaround to compile on Leap 42 in OBS
BuildRequires:  clang4-devel
%endif
# libavcodec is required for H.264 support but the
# openSUSE version is currently not able to play H.264
# therefore the Packman version is required
# minimum version of libavcodec is 53
Recommends:     libavcodec-full >= 0.10.16
Version:        %{mainver}
Release:        0
%if "%{name}" == "MozillaFirefox"
Provides:       firefox = %{mainver}
Provides:       firefox = %{version}-%{release}
%endif
Provides:       web_browser
Provides:       appdata()
Provides:       appdata(firefox.appdata.xml)
# this is needed to match this package with the kde4 helper package without the main package
# having a hard requirement on the kde4 package
%define kde_helper_version 6
Provides:       mozilla-kde4-version = %{kde_helper_version}
Summary:        Mozilla %{appname} Web Browser
License:        MPL-2.0
Group:          Productivity/Networking/Web/Browsers
Url:            http://www.mozilla.org/
Source:         http://ftp.mozilla.org/pub/firefox/releases/%{version}%{version_postfix}/source/firefox-%{version}%{version_postfix}.source.tar.xz
Source1:        MozillaFirefox.desktop
Source2:        MozillaFirefox-rpmlintrc
Source3:        mozilla.sh.in
Source5:        source-stamp.txt
Source6:        kde.js
Source7:        l10n-%{version}%{version_postfix}.tar.xz
Source8:        firefox-mimeinfo.xml
Source9:        firefox.js
Source10:       compare-locales.tar.xz
Source11:       firefox.1
Source12:       mozilla-get-app-id
Source13:       spellcheck.js
Source14:       create-tar.sh
Source15:       firefox-appdata.xml
Source16:       MozillaFirefox.changes
# Set up API keys, see http://www.chromium.org/developers/how-tos/api-keys
# Note: these are for the openSUSE Firefox builds ONLY. For your own distribution,
# please get your own set of keys.
Source18:       mozilla-api-key
Source19:       google-api-key
Source20:       http://ftp.mozilla.org/pub/firefox/releases/%{version}%{version_postfix}/source/firefox-%{version}%{version_postfix}.source.tar.xz.asc
Source21:       mozilla.keyring
# Gecko/Toolkit
Patch1:         mozilla-nongnome-proxies.patch
Patch2:         mozilla-kde.patch
Patch3:         mozilla-ntlm-full-path.patch
Patch4:         mozilla-openaes-decl.patch
Patch6:         mozilla-reduce-files-per-UnifiedBindings.patch
Patch7:         mozilla-aarch64-startup-crash.patch
Patch11:        mozilla-bmo1464766.patch
Patch15:        mozilla-bmo1005535.patch
Patch18:        mozilla-s390-bigendian.patch
Patch19:        mozilla-s390-context.patch
Patch20:        mozilla-ppc-altivec_static_inline.patch
# Firefox/browser
Patch101:       firefox-kde.patch
Patch102:       firefox-branded-icons.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires(post):   coreutils shared-mime-info desktop-file-utils
Requires(postun): shared-mime-info desktop-file-utils
%if %branding
Requires:       %{name}-branding >= 60
%endif
Requires:       mozilla-nspr >= %(rpm -q --queryformat '%%{VERSION}' mozilla-nspr)
Requires:       mozilla-nss >= %(rpm -q --queryformat '%%{VERSION}' mozilla-nss)
Recommends:     libcanberra0
Recommends:     libpulse0
# addon leads to startup crash (bnc#908892)
Obsoletes:      tracker-miner-firefox < 0.15
# libproxy's mozjs pacrunner crashes FF (bnc#759123)
%if 0%{?suse_version} < 1220
Obsoletes:      libproxy1-pacrunner-mozjs <= 0.4.7
%endif
##BuildArch:      i686 x86_64 aarch64 ppc64le

%description
Mozilla Firefox is a standalone web browser, designed for standards
compliance and performance.  Its functionality can be enhanced via a
plethora of extensions.

%package devel
Summary:        Devel package for %{appname}
Group:          Development/Tools/Other
Provides:       firefox-devel = %{version}-%{release}
Requires:       %{name} = %{version}
Requires:       perl(Archive::Zip)
Requires:       perl(XML::Simple)

%description devel
Development files for %{appname} to make packaging of addons easier.

%if %localize
%package translations-common
Summary:        Common translations for %{appname}
Group:          System/Localization
Provides:       locale(%{name}:ar;ca;cs;da;de;en_GB;el;es_AR;es_CL;es_ES;fi;fr;hu;it;ja;ko;nb_NO;nl;pl;pt_BR;pt_PT;ru;sv_SE;zh_CN;zh_TW)
Requires:       %{name} = %{version}
Provides:       %{name}-translations
Obsoletes:      %{name}-translations < %{version}-%{release}

%description translations-common
This package contains several common languages for the user interface
of %{appname}.

%package translations-other
Summary:        Extra translations for %{appname}
Group:          System/Localization
Provides:       locale(%{name}:ach;af;an;as;ast;az;bg;bn_BD;bn_IN;br;bs;cak;cy;dsb;en_ZA;eo;es_MX;et;eu;fa;ff;fy_NL;ga_IE;gd;gl;gn;gu_IN;he;hi_IN;hr;hsb;hy_AM;id;is;ka;kab;kk;km;kn;lij;lt;lv;mai;mk;ml;mr;ms;ne-NP;nn_NO;oc;or;pa_IN;rm;ro;si;sk;sl;son;sq;sr;ta;te;th;tr;uk;uz;vi;xh)
Requires:       %{name} = %{version}
Obsoletes:      %{name}-translations < %{version}-%{release}

%description translations-other
This package contains rarely used languages for the user interface
of %{appname}.
%endif

%if %branding
%package branding-upstream
Summary:        Upstream branding for %{appname}
Group:          Productivity/Networking/Web/Browsers
Provides:       %{name}-branding = %{version}
Conflicts:      otherproviders(%{name}-branding)
Supplements:    packageand(%{name}:branding-upstream)
#BRAND: Provide three files -
#BRAND: /usr/lib/firefox/browserconfig.properties that contains the
#BRAND: default homepage and some other default configuration options
#BRAND: /usr/lib/firefox/defaults/profile/bookmarks.html that contains
#BRAND: the list of default bookmarks
#BRAND: It's also possible to create a file
#BRAND: /usr/lib/firefox/defaults/preferences/firefox-$vendor.js to set
#BRAND: custom preference overrides.
#BRAND: It's also possible to drop files in /usr/lib/firefox/distribution/searchplugins/common/

%description branding-upstream
This package provides upstream look and feel for %{appname}.
%endif

%if %crashreporter
%package buildsymbols
Summary:        Breakpad buildsymbols for %{appname}
Group:          Development/Debug

%description buildsymbols
This subpackage contains the Breakpad created and compatible debugging
symbols meant for upload to Mozilla's crash collector database.
%endif

%prep
%if %localize
%setup -q -n %{source_prefix} -b 7 -b 10
%else
%setup -q -n %{source_prefix}
%endif
cd $RPM_BUILD_DIR/%{source_prefix}
%patch1 -p1
#%patch2 -p1
%patch3 -p1
%patch4 -p1
%ifarch %ix86
%patch6 -p1
%endif
%patch7 -p1
#%patch8 -p1
%ifarch %ix86
#%patch9 -p1
#%patch10 -p1
%endif
%patch11 -p1
#%patch13 -p1
#%patch14 -p1
%ifarch s390x
%patch15 -p1
#%patch16 -p1
%patch18 -p1
%patch19 -p1
%endif
%patch20 -p1
# Firefox
#%patch101 -p1
%patch102 -p1

%build
%ifarch x86_64
# x86_64 has often problems of too many concurrent jobs
# it seems 1.epsilon GB per build job is enough
%limit_build -m 1100
%endif

# no need to add build time to binaries
modified="$(sed -n '/^----/n;s/ - .*$//;p;q' "%{_sourcedir}/MozillaFirefox.changes")"
DATE="\"$(date -d "${modified}" "+%%b %%e %%Y")\""
TIME="\"$(date -d "${modified}" "+%%R")\""
find . -regex ".*\.c\|.*\.cpp\|.*\.h" -exec sed -i "s/__DATE__/${DATE}/g;s/__TIME__/${TIME}/g" {} +
#
#kdehelperversion=$(cat toolkit/xre/nsKDEUtils.cpp | grep '#define KMOZILLAHELPER_VERSION' | cut -d ' ' -f 3)
#if test "$kdehelperversion" != %{kde_helper_version}; then
#  echo fix kde helper version in the .spec file
#  exit 1
#fi
source %{SOURCE5}
export MOZ_SOURCE_CHANGESET=$REV
export SOURCE_REPO=$REPO
export source_repo=$REPO
export MOZ_SOURCE_REPO=$REPO
export MOZ_BUILD_DATE=%{releasedate}
export MOZILLA_OFFICIAL=1
export BUILD_OFFICIAL=1
export MOZ_TELEMETRY_REPORTING=1
%if 0%{?suse_version} <= 1320
export CC=gcc-7
%endif
export CFLAGS="%{optflags} -fno-strict-aliasing"
## bmo#1461041: aarch64: GraphicsCriticalError: seg fault crash
#%ifnarch %arm aarch64
#  #boo#986541: add -fno-delete-null-pointer-checks for gcc6
#  %if 0%{?suse_version} > 1320
#  export CFLAGS="$CFLAGS -fno-delete-null-pointer-checks"
#  %endif
#%endif
# boo#986541: add -fno-delete-null-pointer-checks for gcc6
%if 0%{?suse_version} > 1320
export CFLAGS="$CFLAGS -fno-delete-null-pointer-checks"
%endif
%ifarch %arm aarch64
# no debug symbols on ARM to speed up build
export CFLAGS="${CFLAGS/-g / }"
%endif
%ifarch %arm aarch64 %ix86
# Limit RAM usage during link
export LDFLAGS="${LDFLAGS} -Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif
%if 0%{?build_hardened}
%ifarch x86_64
export LDFLAGS="${LDFLAGS} -Wl,-z,relro,-z,now"
%endif
%endif
%ifarch ppc64 ppc64le
# TODO: This is currently an unknown switch. Why do we need it?
#export CFLAGS="$CFLAGS -mminimal-toc"
%endif
export CXXFLAGS="$CFLAGS"
# Set RUSTFLAGS to fix building with rust >= 1.33
# boo#1130694 rust 1.33.0 breaks Firefox and Thunderbird
# bmo#1539901 ESR 60 build fails with Rust 1.33 due to missing documentation on macros in stylo
# bmo#1519629 Stylo fails with --enable-warnings-as-errors using Rust 1.33
# Preferred alternative to patching and revendoring stylo rust crates
# Revisit with intent to remove in next Firefox ESR 68.0 2019-07-09
export RUSTFLAGS="--cap-lints allow"
%ifarch %{arm} aarch64
export RUSTFLAGS="-Cdebuginfo=0 --cap-lints allow"
%endif
export MOZCONFIG=$RPM_BUILD_DIR/mozconfig
cat << EOF > $MOZCONFIG
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZ_MAKE_FLAGS=%{?jobs:-j%jobs}
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/../obj
. \$topsrcdir/browser/config/mozconfig
ac_add_options --prefix=%{_prefix}
ac_add_options --libdir=%{_libdir}
ac_add_options --includedir=%{_includedir}
ac_add_options --enable-release
ac_add_options --enable-default-toolkit=cairo-gtk3
%if 0%{?build_hardened}
# TODO: Unknown option. Is there an alternative?
#ac_add_options --enable-pie
%endif
# gcc7 (boo#104105)
%if 0%{?suse_version} > 1320
ac_add_options --enable-optimize="-g -O2"
%endif
%ifarch %ix86 %arm aarch64
%if 0%{?suse_version} > 1230
ac_add_options --disable-optimize
%endif
%endif
%ifarch %arm
ac_add_options --disable-elf-hack
%endif
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
%if %{localize}
ac_add_options --with-l10n-base=$RPM_BUILD_DIR/l10n
%endif
#ac_add_options --with-system-jpeg    # libjpeg-turbo is used internally
#ac_add_options --with-system-png     # doesn't work because of missing APNG support
ac_add_options --with-system-zlib
%ifarch %power64 s390x s390
# jemalloc is broken on (some) secondary architectures, definitely on ppc64le
ac_add_options --disable-jemalloc
# NOTE: Currently, system-icu is too old, so we can't build with that,
#       but have to generate the .dat-file freshly. This seems to be a
#       less fragile approach anyways. See below (next line with echo)
# ac_add_options --with-system-icu
%endif
ac_add_options --disable-updater
ac_add_options --disable-tests
ac_add_options --enable-alsa
ac_add_options --disable-debug
ac_add_options --enable-startup-notification
#ac_add_options --enable-chrome-format=jar
ac_add_options --enable-update-channel=%{update_channel}
ac_add_options --with-mozilla-api-keyfile=%{SOURCE18}
ac_add_options --with-google-location-service-api-keyfile=%{SOURCE19}
ac_add_options --with-google-safebrowsing-api-keyfile=%{SOURCE19}
%if %branding
ac_add_options --enable-official-branding
%endif
ac_add_options --enable-libproxy
%if ! %crashreporter
ac_add_options --disable-crashreporter
%endif
%ifarch %arm
ac_add_options --with-fpu=vfpv3-d16
ac_add_options --with-float-abi=hard
%ifarch armv6l armv6hl
ac_add_options --with-arch=armv6
%else
ac_add_options --with-arch=armv7-a
%endif
%endif
%ifarch %arm aarch64 s390x %power64
ac_add_options --disable-webrtc
%endif
EOF

%ifarch ppc64 s390x s390
# NOTE: Currently, system-icu is too old, so we can't build with that,
#       but have to generate the .dat-file freshly. This seems to be a
#       less fragile approach anyways.
# ac_add_options --with-system-icu
echo "Generate big endian version of config/external/icu/data/icud58l.dat"
./mach python intl/icu_sources_data.py .
ls -l config/external/icu/data
rm -f config/external/icu/data/icudt*l.dat
%endif

./mach build

%install
cd $RPM_BUILD_DIR/obj
source %{SOURCE5}
export MOZ_SOURCE_STAMP=$REV
export MOZ_SOURCE_REPO=$REPO
# need to remove default en-US firefox-l10n.js before it gets
# populated into browser's omni.ja; it only contains general.useragent.locale
# which should be loaded from each language pack (set in firefox.js)
rm dist/bin/browser/defaults/preferences/firefox-l10n.js
make -C browser/installer STRIP=/bin/true MOZ_PKG_FATAL_WARNINGS=0
#DEBUG (break the build if searchplugins are missing / temporary)
grep amazondotcom dist/firefox/browser/omni.ja
# copy tree into RPM_BUILD_ROOT
mkdir -p %{buildroot}%{progdir}
cp -rf $RPM_BUILD_DIR/obj/dist/firefox/* %{buildroot}%{progdir}
mkdir -p %{buildroot}%{progdir}/distribution/extensions
mkdir -p %{buildroot}%{progdir}/browser/defaults/preferences/
# install gre prefs
install -m 644 %{SOURCE13} %{buildroot}%{progdir}/defaults/pref/
# install browser prefs
install -m 644 %{SOURCE6} %{buildroot}%{progdir}/browser/defaults/preferences/kde.js
install -m 644 %{SOURCE9} %{buildroot}%{progdir}/browser/defaults/preferences/firefox.js
# install additional locales
%if %localize
mkdir -p %{buildroot}%{progdir}/browser/extensions
truncate -s 0 %{_tmppath}/translations.{common,other}
sed -r '/^(ja-JP-mac|en-US|)$/d;s/ .*$//' $RPM_BUILD_DIR/%{source_prefix}/browser/locales/shipped-locales \
    | xargs -P 8 -n 1 -I {} /bin/sh -c '
        locale=$1
        pushd $RPM_BUILD_DIR/compare-locales
        PYTHONPATH=lib \
            scripts/compare-locales -m ../l10n-merged/$locale \
            ../%{source_prefix}/browser/locales/l10n.ini ../l10n $locale
        popd
        LOCALE_MERGEDIR=$RPM_BUILD_DIR/l10n-merged/$locale \
            make -C browser/locales langpack-$locale
        cp -rL dist/xpi-stage/locale-$locale \
            %{buildroot}%{progdir}/browser/extensions/langpack-$locale@firefox.mozilla.org
        # remove prefs, profile defaults, and hyphenation from langpack
        rm -rf %{buildroot}%{progdir}/browser/extensions/langpack-$locale@firefox.mozilla.org/defaults
        rm -rf %{buildroot}%{progdir}/browser/extensions/langpack-$locale@firefox.mozilla.org/hyphenation
        # check against the fixed common list and sort into the right filelist
        _matched=0
        for _match in ar ca cs da de en-GB el es-AR es-CL es-ES fi fr hu it ja ko nb-NO nl pl pt-BR pt-PT ru sv-SE zh-CN zh-TW; do
            [ "$_match" = "$locale" ] && _matched=1
        done
        [ $_matched -eq 1 ] && _l10ntarget=common || _l10ntarget=other
        echo %{progdir}/browser/extensions/langpack-$locale@firefox.mozilla.org \
            >> %{_tmppath}/translations.$_l10ntarget
' -- {}
%endif
# remove some executable permissions
find %{buildroot}%{progdir} \
     -name "*.js" -o \
     -name "*.jsm" -o \
     -name "*.rdf" -o \
     -name "*.properties" -o \
     -name "*.dtd" -o \
     -name "*.txt" -o \
     -name "*.xml" -o \
     -name "*.css" \
     -exec chmod a-x {} +
# remove mkdir.done files from installed base
find %{buildroot}%{progdir} -type f -name ".mkdir.done" -delete
# overwrite the mozilla start-script and link it to /usr/bin
mkdir --parents %{buildroot}/usr/bin
sed "s:%%PREFIX:%{_prefix}:g
s:%%PROGDIR:%{progdir}:g
s:%%APPNAME:firefox:g
s:%%PROFILE:.mozilla/firefox:g" \
  %{SOURCE3} > %{buildroot}%{progdir}/%{progname}.sh
chmod 755 %{buildroot}%{progdir}/%{progname}.sh
ln -sf ../..%{progdir}/%{progname}.sh %{buildroot}%{_bindir}/%{progname}
# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
sed "s:%%NAME:%{appname}:g
s:%%EXEC:%{progname}:g
s:%%ICON:%{progname}:g" \
  %{SOURCE1} > %{buildroot}%{_datadir}/applications/%{desktop_file_name}.desktop
%suse_update_desktop_file %{desktop_file_name} Network WebBrowser GTK
# additional mime-types
mkdir -p %{buildroot}%{_datadir}/mime/packages
cp %{SOURCE8} %{buildroot}%{_datadir}/mime/packages/%{progname}.xml
# appdata
mkdir -p %{buildroot}%{_datadir}/appdata
cp %{SOURCE15} %{buildroot}%{_datadir}/appdata/%{desktop_file_name}.appdata.xml
# install man-page
mkdir -p %{buildroot}%{_mandir}/man1/
cp %{SOURCE11} %{buildroot}%{_mandir}/man1/%{progname}.1
##########
# ADDONS
#
mkdir -p %{buildroot}%{_datadir}/mozilla/extensions/%{firefox_appid}
mkdir -p %{buildroot}%{_libdir}/mozilla/extensions/%{firefox_appid}
mkdir -p %{buildroot}/usr/share/pixmaps/
ln -sf %{progdir}/browser/chrome/icons/default/default128.png %{buildroot}/usr/share/pixmaps/%{progname}.png
ln -sf %{progdir}/browser/chrome/icons/default/default128.png %{buildroot}/usr/share/pixmaps/%{progname}-gnome.png
%if %branding
for size in 16 22 24 32 48 64 128 256; do
%else
for size in 16 32 48; do
%endif
  mkdir -p %{buildroot}%{gnome_dir}/share/icons/hicolor/${size}x${size}/apps/
  cp %{buildroot}%{progdir}/browser/chrome/icons/default/default$size.png \
         %{buildroot}%{gnome_dir}/share/icons/hicolor/${size}x${size}/apps/%{progname}.png
done
# excludes
rm -f %{buildroot}%{progdir}/updater.ini
rm -f %{buildroot}%{progdir}/removed-files
rm -f %{buildroot}%{progdir}/README.txt
rm -f %{buildroot}%{progdir}/old-homepage-default.properties
rm -f %{buildroot}%{progdir}/run-mozilla.sh
rm -f %{buildroot}%{progdir}/LICENSE
rm -f %{buildroot}%{progdir}/precomplete
rm -f %{buildroot}%{progdir}/dictionaries/en-US*
rm -f %{buildroot}%{progdir}/update-settings.ini
# devel
mkdir -p %{buildroot}%{_bindir}
install -m 755 %SOURCE12 %{buildroot}%{_bindir}
# inspired by mandriva
mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat <<'FIN' >%{buildroot}%{_sysconfdir}/rpm/macros.%{progname}
# Macros from %{name} package
%%firefox_major              %{major}
%%firefox_version            %{version}
%%firefox_mainver            %{mainver}
%%firefox_mozillapath        %%{_libdir}/%{progname}
%%firefox_pluginsdir         %%{_libdir}/browser-plugins
%%firefox_appid              \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
%%firefox_extdir             %%(if [ "%%_target_cpu" = "noarch" ]; then echo %%{_datadir}/mozilla/extensions/%%{firefox_appid}; else echo %%{_libdir}/mozilla/extensions/%%{firefox_appid}; fi)

%%firefox_ext_install() \
   extdir="%%{buildroot}%%{firefox_extdir}/`mozilla-get-app-id '%%1'`" \
   mkdir -p "$extdir" \
   %%{__unzip} -q -d "$extdir" "%%1" \
   %%{nil}
FIN
# just dumping an xpi file there doesn't work...
#%%firefox_ext_install() \
#       extdir="%%{buildroot}%%{firefox_extdir}" \
#       mkdir -p "$extdir" \
#       cp "%%1" "$extdir" \
#       %%{nil}
# fdupes
%fdupes %{buildroot}%{progdir}
%fdupes %{buildroot}%{_datadir}
# create breakpad debugsymbols
%if %crashreporter
SYMBOLS_NAME="firefox-%{version}-` echo '%{release}' | sed 's@\.[^\.]\+$@@' `.%{_arch}-%{suse_version}-symbols"
make buildsymbols \
  SYMBOL_INDEX_NAME="$SYMBOLS_NAME.txt" \
  SYMBOL_FULL_ARCHIVE_BASENAME="$SYMBOLS_NAME-full" \
  SYMBOL_ARCHIVE_BASENAME="$SYMBOLS_NAME"
if [ -e dist/*symbols.zip ]; then
  mkdir -p %{buildroot}%{_datadir}/mozilla/
  cp dist/*symbols.zip %{buildroot}%{_datadir}/mozilla/
fi
%endif

%clean
rm -rf %{buildroot}
%if %localize
rm -rf %{_tmppath}/translations.*
%endif

%post
# update mime and desktop database
%mime_database_post
%desktop_database_post
%icon_theme_cache_post
exit 0

%postun
%icon_theme_cache_postun
%desktop_database_postun
%mime_database_postun
exit 0

%files
%defattr(-,root,root)
%dir %{progdir}
%dir %{progdir}/browser/
%dir %{progdir}/browser/chrome/
%{progdir}/browser/defaults
%{progdir}/browser/features/
%{progdir}/browser/chrome/icons
%{progdir}/browser/blocklist.xml
%{progdir}/browser/chrome.manifest
%{progdir}/browser/omni.ja
%dir %{progdir}/distribution/
%{progdir}/distribution/extensions/
%{progdir}/defaults/
%dir %{progdir}/gtk2
%{progdir}/gtk2/libmozgtk.so
%{progdir}/gmp-clearkey/
%attr(755,root,root) %{progdir}/%{progname}.sh
%{progdir}/firefox
%{progdir}/firefox-bin
%{progdir}/application.ini
%{progdir}/chrome.manifest
%{progdir}/dependentlibs.list
%{progdir}/*.so
%{progdir}/omni.ja
%{progdir}/fonts/
%{progdir}/pingsender
%{progdir}/platform.ini
%{progdir}/plugin-container
%if %crashreporter
%{progdir}/crashreporter
%{progdir}/crashreporter.ini
%{progdir}/Throbber-small.gif
%{progdir}/minidump-analyzer
%{progdir}/browser/crashreporter-override.ini
%endif
%{_datadir}/applications/%{desktop_file_name}.desktop
%{_datadir}/mime/packages/%{progname}.xml
%{_datadir}/pixmaps/firefox*
%dir %{_datadir}/mozilla
%dir %{_datadir}/mozilla/extensions
%dir %{_datadir}/mozilla/extensions/%{firefox_appid}
%dir %{_libdir}/mozilla
%dir %{_libdir}/mozilla/extensions
%dir %{_libdir}/mozilla/extensions/%{firefox_appid}
%{gnome_dir}/share/icons/hicolor/
%{_bindir}/%{progname}
%doc %{_mandir}/man1/%{progname}.1.gz
%{_datadir}/appdata/

%files devel
%defattr(-,root,root)
%{_bindir}/mozilla-get-app-id
%config %{_sysconfdir}/rpm/macros.%{progname}

%if %localize

%files translations-common -f %{_tmppath}/translations.common
%defattr(-,root,root)
%dir %{progdir}
%dir %{progdir}/browser/extensions/

%files translations-other -f %{_tmppath}/translations.other
%defattr(-,root,root)
%dir %{progdir}
%dir %{progdir}/browser/extensions/
%endif

# this package does not need to provide files but is needed to fulfill
# requirements if no other branding package is to be installed
%if %branding
%files branding-upstream
%defattr(-,root,root)
%dir %{progdir}
%endif

%if %crashreporter
%files buildsymbols
%defattr(-,root,root)
%{_datadir}/mozilla/*.zip
%endif

%changelog
