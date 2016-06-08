#define MyAppName "DatabaseSwapper"
#define MyAppVersion "0.1b"
#define MyAppPublisher "Grant Mercer"
#define MyAppURL "grantmercer.com"
#define MyAppExeName "swapper.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{54422CFF-C510-4ED2-B7DE-B3F1AE946EE9}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DisableProgramGroupPage=yes
; NOTE: CHANGE PATHS TO OUTPUT LOCATION OF YOUR CHOICE
OutputDir=C:\Users\Grant\Documents\GitHub\db_swapper\build\swapper
OutputBaseFilename=swapper_setupv01b
Compression=lzma
SolidCompression=yes
SetupLogging=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[code]
// Called just before Setup terminates. Note that this function is called even if the user exits Setup before anything is installed.
procedure DeinitializeSetup();
var
  logfilepathname, logfilename, newfilepathname: string;

begin
  logfilepathname := expandconstant('{log}');
  logfilename := ExtractFileName(logfilepathname);
  // Set the new target path as the directory where the installer is being run from
  newfilepathname := expandconstant('{src}\') +logfilename;

  filecopy(logfilepathname, newfilepathname, false);
end; 

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\Grant\Documents\GitHub\db_swapper\build\swapper\swapper.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Grant\Documents\GitHub\db_swapper\build\swapper\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon