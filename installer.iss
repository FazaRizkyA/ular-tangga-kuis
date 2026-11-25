; Skrip Inno Setup untuk Ular Tangga Kuis
; Kompilasi: ISCC.exe installer.iss  (setelah PyInstaller membuat dist\UlarTanggaKuis)

#define NamaApp "Ular Tangga Kuis"
; Versi dikirim oleh build.bat dari config.py (VERSI); nilai di bawah hanya cadangan.
#ifndef VersiApp
  #define VersiApp "1.1"
#endif
#define ExeApp "UlarTanggaKuis.exe"

[Setup]
AppId={{6C3D0F5E-8B1A-4F2C-9C1E-2B7A5D4E9F10}
AppName={#NamaApp}
AppVersion={#VersiApp}
AppPublisher=SMK Krian 1 Sidoarjo
DefaultDirName={autopf}\UlarTanggaKuis
DefaultGroupName={#NamaApp}
PrivilegesRequired=lowest
OutputDir=..\installer
OutputBaseFilename=Setup_UlarTanggaKuis_v{#VersiApp}
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\{#ExeApp}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=yes

[Tasks]
Name: "desktopicon"; Description: "Buat shortcut di Desktop"; GroupDescription: "Shortcut:"

[Files]
Source: "dist\UlarTanggaKuis\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\{#NamaApp}"; Filename: "{app}\{#ExeApp}"
Name: "{group}\Hapus {#NamaApp}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#NamaApp}"; Filename: "{app}\{#ExeApp}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#ExeApp}"; Description: "Jalankan {#NamaApp}"; Flags: nowait postinstall skipifsilent
