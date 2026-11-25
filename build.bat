@echo off
rem Build Ular Tangga Kuis: .exe (PyInstaller) lalu installer offline (Inno Setup).
rem Jalankan dari folder source_code. Butuh: venv berisi requirements.txt, Inno Setup 6.
setlocal
cd /d "%~dp0"

if not exist venv\Scripts\python.exe (
  echo [1/4] Membuat virtual environment...
  python -m venv venv || goto :gagal
  venv\Scripts\python.exe -m pip install -r requirements.txt || goto :gagal
)

rem Nomor versi diambil dari config.py (VERSI) agar menu dan installer selalu sama.
for /f %%v in ('venv\Scripts\python.exe -c "import config; print(config.VERSI)"') do set VERSI=%%v
echo Versi: %VERSI%

echo [2/4] Uji logika...
venv\Scripts\python.exe alat\uji_logika.py || goto :gagal

echo [3/4] PyInstaller...
venv\Scripts\pyinstaller.exe --noconfirm --clean --noconsole --onedir ^
  --icon=icon.ico --name UlarTanggaKuis ^
  --add-data "assets;assets" --add-data "soal.json;." --add-data "icon.ico;." ^
  main.py || goto :gagal

echo [4/4] Inno Setup...
set ISCC="%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
if not exist %ISCC% set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
%ISCC% /DVersiApp=%VERSI% installer.iss || goto :gagal

echo.
echo Selesai: ..\installer\Setup_UlarTanggaKuis_v%VERSI%.exe
exit /b 0

:gagal
echo.
echo BUILD GAGAL. Periksa pesan di atas.
exit /b 1
