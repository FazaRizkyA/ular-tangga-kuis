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

requirements = python3,pygame

icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/icon.png
android.presplash_color = #1C4A98

orientation = landscape
fullscreen = 1

# Tidak meminta izin apa pun (100% offline, tanpa internet)
android.permissions =

android.api = 34
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = True

p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 0
