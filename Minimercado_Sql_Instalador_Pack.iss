[Setup]
AppName=Sistema de Minimercado
AppVersion=1.0
DefaultDirName=C:\Program Files\MinimercadoSql\Sistema de Minimercado Sql
DefaultGroupName=MinimercadoSql
LicenseFile=licenca.txt
WizardImageFile=splash.bmp
WizardSmallImageFile=splash.bmp
SetupIconFile=icone.ico
WizardStyle=modern
UsePreviousAppDir=no
Compression=lzma
SolidCompression=yes
OutputBaseFilename=MinimercadoSqlSetup
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
;WizardImageBackColor=$00C0C0FF
;Password=mercado2025  
; << Senha para instalação mercado2025

[Files]
Source: "dist\\minimercado_tkinter_sql.exe"; DestDir: "{app}"; Flags: ignoreversion
;minimercado_tkinter_sql

[Icons]
Name: "{group}\Sistema de Minimercado Sql"; Filename: "{app}\minimercado_tkinter_sql.exe"
Name: "{userdesktop}\Sistema de Minimercado Sql"; Filename: "{app}\minimercado_tkinter_sql.exe"; Flags: createonlyiffileexists
Name: "{group}\Desinstalar Sistema de Minimercado Sql"; Filename: "{uninstallexe}"

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar ícone na Área de Trabalho"; GroupDescription: "Opções adicionais:"

[Run]
;Filename: "https://seusite.com.br"; Description: "Visitar nosso site"; Flags: shellexec postinstall skipifsilent
Filename: "{app}\\minimercado_tkinter_sql.exe"; Description: "Executar Sistema agora"; Flags: nowait postinstall skipifsilent
Filename: "{sys}\\cmd.exe"; Parameters: "/c echo ^G"; StatusMsg: "Finalizando instalação..."; Flags: runhidden

[Messages]
WelcomeLabel1=Bem-vindo ao Instalador do Sistema de Minimercado Sql!
WelcomeLabel2=Este assistente irá instalar o Sistema de Minimercado Sql no seu computador.
;WelcomeLabel3=Clique em Avançar para continuar.
FinishedLabel=Sistema de Minimercado Sql instalado com sucesso! Obrigado!
