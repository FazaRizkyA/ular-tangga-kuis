[app]
# Konfigurasi APK Android (Buildozer / python-for-android).
# Dibangun otomatis oleh GitHub Actions: .github/workflows/android.yml

title = Ular Tangga Kuis
package.name = ulartanggakuis
package.domain = id.sch.smkkrian1

source.dir = .
source.include_exts = py,png,jpg,ttf,wav,ogg,json,txt,ico
source.exclude_dirs = venv,build,dist,alat,aset_sumber,docs,.impeccable,.github,__pycache__,bin,.buildozer
source.exclude_patterns = *.spec,*.iss,*.bat,*.md,LICENSE

# Nomor versi diambil dari config.py (VERSI), sama dengan versi Windows
version.regex = VERSI = "(.*)"
version.filename = %(source.dir)s/config.py

# Versi dikunci: resep pygame (2.1) di python-for-android cocok dengan Python 3.10.
# Python 3.11+ memindahkan header longintrepr.h sehingga pygame gagal dikompilasi.
requirements = python3==3.10.10,hostpython3==3.10.10,pygame

icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/icon.png
android.presplash_color = #1C4A98

orientation = landscape
fullscreen = 1

# Tidak meminta izin apa pun (100% offline, tanpa internet)
android.permissions =

android.api = 33
android.minapi = 24
android.ndk = 25b
# arm untuk HP; x86_64 agar APK bisa diuji otomatis di emulator (dan jalan di tablet/Chromebook x86)
android.archs = arm64-v8a, armeabi-v7a, x86_64
android.release_artifact = apk
android.debug_artifact = apk
android.accept_sdk_license = True
android.allow_backup = True

p4a.bootstrap = sdl2
# Rilis python-for-android yang teruji dengan Python 3.10 + NDK r25b
p4a.branch = v2023.09.16

[buildozer]
log_level = 2
warn_on_root = 0
