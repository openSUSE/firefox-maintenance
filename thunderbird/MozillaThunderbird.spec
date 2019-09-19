#
# spec file for package MozillaThunderbird
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#               2006-2019 Wolfgang Rosenauer <wr@rosenauer.org>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


# changed with every update
# orig_version vs. mainver: To have beta-builds
# FF70beta3 would be released as FF69.99
# orig_version would be the upstream tar ball
# orig_version 70.0
# orig_suffix b3
# major 69
# mainver %major.99
%define major          68
%define mainver        %major.1.0
%define orig_version   68.1.0
%define orig_suffix    %{nil}
%define update_channel release
%define branding       1
%define releasedate    20190522150740
%define source_prefix  thunderbird-%{orig_version}

# https://bugzilla.suse.com/show_bug.cgi?id=1138688
# always build with GCC as SUSE Security Team requires that
%define clang_build 0

# PIE, full relro
%define build_hardened 1

%bcond_with only_print_mozconfig

%bcond_without mozilla_tb_kde4
%bcond_with    mozilla_tb_valgrind
%bcond_without mozilla_tb_optimize_for_size

# general build definitions
%define progname thunderbird
%define pkgname  MozillaThunderbird
%define appname  Thunderbird
%define progdir %{_prefix}/%_lib/%{progname}
%define gnome_dir     %{_prefix}
%define desktop_file_name %{progname}
%define __provides_exclude ^lib.*\\.so.*$
%define __requires_exclude ^(libmoz.*|liblgpllibs.*|libxul.*|libldap.*|libldif.*|libprldap.*)$

%define localize 1
%ifarch %ix86 x86_64
%define crashreporter 1
%else
%define crashreporter 0
%endif

%define has_system_cairo 0

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
BuildRequires:  cargo >= 1.34
BuildRequires:  libXcomposite-devel
BuildRequires:  libcurl-devel
BuildRequires:  libidl-devel
BuildRequires:  libnotify-devel
BuildRequires:  libproxy-devel
BuildRequires:  mozilla-nspr-devel >= 4.21
BuildRequires:  mozilla-nss-devel >= 3.44.1
BuildRequires:  nasm >= 2.13
BuildRequires:  nodejs8 >= 8.11
BuildRequires:  python-devel
BuildRequires:  python2-xml
BuildRequires:  python3 >= 3.5
BuildRequires:  rust >= 1.34
BuildRequires:  rust-cbindgen >= 0.8.7
BuildRequires:  startup-notification-devel
BuildRequires:  unzip
BuildRequires:  update-desktop-files
BuildRequires:  xorg-x11-libXt-devel
BuildRequires:  xvfb-run
BuildRequires:  yasm
BuildRequires:  zip
%if 0%{?suse_version} < 1550
BuildRequires:  pkgconfig(gconf-2.0) >= 1.2.1
%endif
BuildRequires:  pkgconfig(gdk-x11-2.0)
BuildRequires:  pkgconfig(glib-2.0) >= 2.22
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gtk+-2.0) >= 2.18.0
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.4.0
BuildRequires:  pkgconfig(gtk+-unix-print-2.0)
BuildRequires:  pkgconfig(gtk+-unix-print-3.0)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  xz
%if %{with mozilla_tb_valgrind}
BuildRequires:  pkgconfig(valgrind)
%endif
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
Provides:       thunderbird = %{version}
Provides:       MozillaThunderbird-devel = %{version}
Obsoletes:      MozillaThunderbird-devel < %{version}
Provides:       appdata()
Provides:       appdata(thunderbird.appdata.xml)
%if %{with mozilla_tb_kde4}
# this is needed to match this package with the kde4 helper package without the main package
# having a hard requirement on the kde4 package
%define kde_helper_version 6
Provides:       mozilla-kde4-version = %{kde_helper_version}
%endif
Summary:        The Stand-Alone Mozilla Mail Component
License:        MPL-2.0
Group:          Productivity/Networking/Email/Clients
Url:            https://www.thunderbird.net/
%if !%{with only_print_mozconfig}
Source:         http://ftp.mozilla.org/pub/%{progname}/releases/%{version}%{orig_suffix}/source/%{progname}-%{orig_version}%{orig_suffix}.source.tar.xz
Source1:        thunderbird.desktop
Source2:        thunderbird-rpmlintrc
Source3:        mozilla.sh.in
Source4:        tar_stamps
Source6:        kde.js
Source7:        l10n-%{orig_version}%{orig_suffix}.tar.xz
Source9:        suse-default-prefs.js
Source10:       compare-locales.tar.xz
Source13:       spellcheck.js
Source14:       https://github.com/openSUSE/firefox-scripts/raw/master/create-tar.sh
Source15:       thunderbird.appdata.xml
Source16:       MozillaThunderbird.changes
Source20:       https://ftp.mozilla.org/pub/%{progname}/releases/%{version}%{orig_suffix}/source/%{progname}-%{orig_version}%{orig_suffix}.source.tar.xz.asc
Source21:       https://ftp.mozilla.org/pub/%{progname}/releases/%{version}%{orig_suffix}/KEY#/mozilla.keyring
# Gecko/Toolkit
Patch1:         mozilla-nongnome-proxies.patch
Patch2:         mozilla-kde.patch
Patch3:         mozilla-ntlm-full-path.patch
Patch4:         mozilla-openaes-decl.patch
Patch5:         mozilla-aarch64-startup-crash.patch
Patch6:         mozilla-bmo1463035.patch
Patch7:         mozilla-cubeb-noreturn.patch
Patch8:         mozilla-fix-aarch64-libopus.patch
Patch9:         mozilla-disable-wasm-emulate-arm-unaligned-fp-access.patch
Patch10:        mozilla-s390-context.patch
Patch11:        mozilla-s390-bigendian.patch
Patch12:        mozilla-reduce-rust-debuginfo.patch
Patch13:        mozilla-ppc-altivec_static_inline.patch
Patch14:        mozilla-bmo1005535.patch
Patch15:        mozilla-bmo1568145.patch
Patch16:        mozilla-bmo1573381.patch
Patch17:        mozilla-bmo1504834-part1.patch
Patch18:        mozilla-bmo1504834-part2.patch
Patch19:        mozilla-bmo1504834-part3.patch
Patch20:        mozilla-bmo1511604.patch
Patch21:        mozilla-bmo1554971.patch
Patch22:        mozilla-nestegg-big-endian.patch
Patch23:        mozilla-bmo1512162.patch
# Thunderbird
Patch101:       thunderbird-broken-locales-build.patch
%endif # only_print_mozconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires(post):   coreutils shared-mime-info desktop-file-utils
Requires(postun): shared-mime-info desktop-file-utils
Requires:       mozilla-nspr >= %(rpm -q --queryformat '%%{VERSION}' mozilla-nspr)
Requires:       mozilla-nss >= %(rpm -q --queryformat '%%{VERSION}' mozilla-nss)
Recommends:     libcanberra0
Recommends:     libpulse0
Conflicts:      thunderbird-esr
%define libgssapi libgssapi_krb5.so.2

%description
Mozilla Thunderbird is a redesign of the Mozilla Mail component. It is
written using the XUL user interface language and designed to be
cross-platform. It is a stand-alone application instead of part of the
Mozilla application suite.

%if %localize
%package translations-common
Summary:        Common translations for %{appname}
Group:          System/Localization
Provides:       locale(%{name}:ar;ca;cs;da;de;el;en_GB;es_AR;es_CL;es_ES;fi;fr;hu;it;ja;ko;nb_NO;nl;pl;pt_BR;pt_PT;ru;sv_SE;zh_CN;zh_TW)
Requires:       %{name} = %{version}
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

%if %crashreporter
%package buildsymbols
Summary:        Breakpad buildsymbols for %{appname}
Group:          Development/Debug

%description buildsymbols
This subpackage contains the Breakpad created and compatible debugging
symbols meant for upload to Mozilla's crash collector database.
%endif

%if !%{with only_print_mozconfig}
%prep
%if %localize

# If generated incorrectly, the tarball will be ~270B in
# size, so 1MB seems like good enough limit to check.
MINSIZE=1048576
if (( $(stat -c%s "%{SOURCE7}") < MINSIZE)); then
    echo "Translations tarball %{SOURCE7} not generated properly."
    exit 1
fi

%setup -q -n %{source_prefix} -b 7 -b 10
%else
%setup -q -n %{source_prefix}
%endif
#cd $RPM_BUILD_DIR/%{source_prefix}
%patch1 -p1
%if %{with mozilla_tb_kde4}
%patch2 -p1
%endif
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%ifarch s390x ppc64
%patch11 -p1
%endif
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch101 -p1
%endif # only_print_mozconfig

%build
%if !%{with only_print_mozconfig}
# no need to add build time to binaries
modified="$(sed -n '/^----/n;s/ - .*$//;p;q' "%{_sourcedir}/%{name}.changes")"
DATE="\"$(date -d "${modified}" "+%%b %%e %%Y")\""
TIME="\"$(date -d "${modified}" "+%%R")\""
find . -regex ".*\.c\|.*\.cpp\|.*\.h" -exec sed -i "s/__DATE__/${DATE}/g;s/__TIME__/${TIME}/g" {} +
#
%if %{with mozilla_tb_kde4}
kdehelperversion=$(cat toolkit/xre/nsKDEUtils.cpp | grep '#define KMOZILLAHELPER_VERSION' | cut -d ' ' -f 3)
if test "$kdehelperversion" != %{kde_helper_version}; then
  echo fix kde helper version in the .spec file
  exit 1
fi
%endif
%endif # only_print_mozconfig

export SUSE_ASNEEDED=0
export MOZ_BUILD_DATE=%{releasedate}
export MOZILLA_OFFICIAL=1
export BUILD_OFFICIAL=1
export MOZ_TELEMETRY_REPORTING=1
%if %{update_channel} == "esr"
export MOZ_ESR=1
%endif
%if 0%{?suse_version} <= 1320
export CC=gcc-7
%else
%if 0%{?clang_build} == 0
export CC=gcc
export CXX=g++
%endif
%endif
%ifarch %arm %ix86
# Limit RAM usage during link
export LDFLAGS="${LDFLAGS} -Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif
%if 0%{?build_hardened}
export LDFLAGS="${LDFLAGS} -fPIC -Wl,-z,relro,-z,now"
%endif
%ifarch ppc64 ppc64le
%if 0%{?clang_build} == 0
export CFLAGS="$CFLAGS -mminimal-toc"
%endif
%endif
export CXXFLAGS="$CFLAGS"
export MOZCONFIG=$RPM_BUILD_DIR/mozconfig
%if %{with only_print_mozconfig}
echo "export CC=$CC"
echo "export CXX=$CXX"
echo "export CFLAGS=\"$CFLAGS\""
echo "export LDFLAGS=\"$LDFLAGS\""
echo "export RUSTFLAGS=\"$RUSTFLAGS\""
echo ""
cat << EOF
%else
%limit_build -m 2000
cat << EOF > $MOZCONFIG
%endif
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZ_MAKE_FLAGS=%{?jobs:-j%jobs}
mk_add_options MOZ_OBJDIR=$RPM_BUILD_DIR/obj
ac_add_options --prefix=%{_prefix}
ac_add_options --libdir=%{_libdir}
ac_add_options --includedir=%{_includedir}
ac_add_options --enable-application=comm/mail
ac_add_options --enable-calendar
ac_add_options --enable-release
ac_add_options --enable-default-toolkit=cairo-gtk3
%if 0%{?suse_version} >= 1550
ac_add_options --disable-gconf
%endif
# bmo#1441155 - Disable the generation of Rust debug symbols on Linux32
%ifarch %ix86 %arm
ac_add_options --disable-debug-symbols
%else
ac_add_options --enable-debug-symbols
%endif
%if 0%{?suse_version} > 1549
%ifnarch aarch64 ppc64 ppc64le s390x
ac_add_options --disable-elf-hack
%endif
%endif
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
%if %{localize}
ac_add_options --with-l10n-base=$RPM_BUILD_DIR/l10n
%endif
#ac_add_options --with-system-jpeg    # libjpeg-turbo is used internally
#ac_add_options --with-system-png     # doesn't work because of missing APNG support
ac_add_options --with-system-zlib
ac_add_options --disable-updater
ac_add_options --disable-tests
ac_add_options --enable-alsa
ac_add_options --disable-debug
ac_add_options --enable-startup-notification
ac_add_options --disable-necko-wifi
ac_add_options --enable-update-channel=%{update_channel}
%if %has_system_cairo
ac_add_options --enable-system-cairo
%endif
ac_add_options --with-unsigned-addon-scopes=app
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
%ifarch aarch64 %arm s390x
ac_add_options --disable-webrtc
%endif
# mitigation/workaround for bmo#1512162
%ifarch ppc64le s390x
ac_add_options --enable-optimize="-O1"
%endif
%ifarch x86_64
# LTO needs newer toolchain stack only (at least GCC 8.2.1 (r268506)
%if 0%{?suse_version} > 1500
ac_add_options --enable-lto
ac_add_options MOZ_PGO=1
%endif
%endif

%if %{with mozilla_tb_valgrind}
ac_add_options --disable-jemalloc
ac_add_options --enable-valgrind
%endif
EOF
%if !%{with only_print_mozconfig}
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
xvfb-run --server-args="-screen 0 1920x1080x24" ./mach build
%endif # only_print_mozconfig

%install
cd $RPM_BUILD_DIR/obj
make -C comm/mail/installer STRIP=/bin/true MOZ_PKG_FATAL_WARNINGS=0
# copy tree into RPM_BUILD_ROOT
mkdir -p %{buildroot}%{progdir}
cp -rf $RPM_BUILD_DIR/obj/dist/%{progname}/* %{buildroot}%{progdir}
install -m 644 %{SOURCE13} %{buildroot}%{progdir}/defaults/pref/
%if %{with mozilla_tb_kde4}
# install kde.js
install -m 644 %{SOURCE6} %{buildroot}%{progdir}/defaults/pref/kde.js
install -m 644 %{SOURCE9} %{buildroot}%{progdir}/defaults/pref/all-thunderbird.js
%endif
# build additional locales
%if %localize
mkdir -p %{buildroot}%{progdir}/extensions/
truncate -s 0 %{_tmppath}/translations.{common,other}
sed -r '/^(ja-JP-mac|en-US|)$/d;s/ .*$//' $RPM_BUILD_DIR/%{source_prefix}/comm/mail/locales/shipped-locales \
    | xargs -P 8 -n 1 -I {} /bin/sh -c '
        locale=$1
        pushd $RPM_BUILD_DIR/compare-locales
        PYTHONPATH=lib \
            scripts/compare-locales -m ../l10n-merged/$locale \
          ../%{source_prefix}/comm/mail/locales/l10n.ini ../l10n $locale
        popd
        LOCALE_MERGEDIR=$RPM_BUILD_DIR/l10n-merged/$locale \
            make -C comm/mail/locales langpack-$locale
        cp -rL dist/xpi-stage/locale-$locale \
           %{buildroot}%{progdir}/extensions/langpack-$locale@thunderbird.mozilla.org
        # remove prefs and profile defaults from langpack
        rm -rf %{buildroot}%{progdir}/extensions/langpack-$locale@thunderbird.mozilla.org/defaults
        # check against the fixed common list and sort into the right filelist
        _matched=0
        for _match in ar ca cs da de el en-GB es-AR es-CL es-ES fi fr hu it ja ko nb-NO nl pl pt-BR pt-PT ru sv-SE zh-CN zh-TW; do
            [ "$_match" = "$locale" ] && _matched=1
        done
        [ $_matched -eq 1 ] && _l10ntarget=common || _l10ntarget=other
        echo %{progdir}/extensions/langpack-$locale@thunderbird.mozilla.org \
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
mkdir --parents %{buildroot}%{_bindir}/
sed "s:%%PREFIX:%{_prefix}:g
s:%%PROGDIR:%{progdir}:g
s:%%APPNAME:thunderbird:g
s:%%PROFILE:.thunderbird:g" \
  %{SOURCE3} > %{buildroot}%{progdir}/%{progname}.sh
chmod 755 %{buildroot}%{progdir}/%{progname}.sh
ln -sf ../..%{progdir}/%{progname}.sh %{buildroot}%{_bindir}/%{progname}
# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
sed "s:%%NAME:%{appname}:g
s:%%EXEC:%{progname}:g
s:%%ICON:%{progname}:g" \
  %{SOURCE1} > %{buildroot}%{_datadir}/applications/%{desktop_file_name}.desktop
%suse_update_desktop_file %{desktop_file_name} Network Email GTK
# appdata
mkdir -p %{buildroot}%{_datadir}/appdata
cp %{SOURCE15} %{buildroot}%{_datadir}/appdata/%{desktop_file_name}.appdata.xml
# apply SUSE defaults
sed -e 's,RPM_VERSION,%{mainversion},g
s,GSSAPI,%{libgssapi},g' \
   %{SOURCE9} > suse-default-prefs
cp suse-default-prefs %{buildroot}%{progdir}/defaults/pref/all-opensuse.js
rm suse-default-prefs
# use correct locale for useragent
cat > %{buildroot}%{progdir}/defaults/pref/all-l10n.js << EOF
pref("general.useragent.locale", "chrome://global/locale/intl.properties");
EOF
#
for size in 16 22 24 32 48 64 128; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/
  cp %{buildroot}%{progdir}/chrome/icons/default/default$size.png \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{progname}.png
done

# excluded files
rm -f %{buildroot}%{progdir}/thunderbird
rm -f %{buildroot}%{progdir}/removed-files
rm -f %{buildroot}%{progdir}/precomplete
rm -f %{buildroot}%{progdir}/updater
rm -f %{buildroot}%{progdir}/updater.ini
rm -f %{buildroot}%{progdir}/update.locale
rm -f %{buildroot}%{progdir}/dictionaries/en-US*
rm -f %{buildroot}%{progdir}/nspr-config
# Some sites use different partitions for /usr/(lib|lib64) and /usr/share.  Since you
# can't create hardlinks across partitions, we'll do this more than once.
%fdupes %{buildroot}%{progdir}
%fdupes %{buildroot}%{_libdir}/mozilla
%fdupes %{buildroot}%{_datadir}
# create breakpad debugsymbols
%if %crashreporter
SYMBOLS_NAME="thunderbird-%{version}-%{release}.%{_arch}-%{suse_version}-symbols"
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
%dir %{progdir}/chrome/
%{progdir}/defaults/
%{progdir}/features/
%{progdir}/chrome/icons/
%{progdir}/blocklist.xml
%{progdir}/distribution/
%{progdir}/isp/
%attr(755,root,root) %{progdir}/%{progname}.sh
%{progdir}/thunderbird-bin
%{progdir}/application.ini
%{progdir}/chrome.manifest
%{progdir}/dependentlibs.list
%dir %{progdir}/gtk2
%{progdir}/gtk2/libmozgtk.so
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
%endif
%{_datadir}/applications/%{desktop_file_name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{progname}.png
%{_bindir}/%{progname}
%{_datadir}/appdata/

%if %localize
%files translations-common -f %{_tmppath}/translations.common
%defattr(-,root,root)
%dir %{progdir}/extensions/

%files translations-other -f %{_tmppath}/translations.other
%defattr(-,root,root)
%dir %{progdir}/extensions/
%endif

%if %crashreporter
%files buildsymbols
%defattr(-,root,root)
%{_datadir}/mozilla/
%endif

%changelog
