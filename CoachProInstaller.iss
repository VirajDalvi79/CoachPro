#define MyAppName "CoachPro Management System"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Viraj Dalvi"
#define MyAppExeName "CoachPro.exe"

[Setup]
AppId={{A8B03B23-8B5A-4E23-9A9B-COACHPRO1000}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\CoachPro
DefaultGroupName=CoachPro
DisableProgramGroupPage=yes
OutputDir=D:\Coaching\installer
OutputBaseFilename=CoachProSetup
SetupIconFile=D:\Coaching\coachpro.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "D:\Coaching\dist\CoachPro\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\CoachPro"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\CoachPro"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch CoachPro"; Flags: nowait postinstall skipifsilent