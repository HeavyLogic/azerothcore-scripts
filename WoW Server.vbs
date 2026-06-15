Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Папка, где лежит VBS
basePath = fso.GetParentFolderName(WScript.ScriptFullName)

cmd = "wt " & _
      "new-tab cmd /k ""cd /d """ & basePath & """ && title MYSQL && call MySQL.bat"" ; " & _
      "new-tab cmd /k ""cd /d """ & basePath & """ && timeout /t 8 >nul && title AUTH && authserver"" ; " & _
      "new-tab cmd /k ""cd /d """ & basePath & """ && timeout /t 11 >nul && title WORLD && worldserver"""

WshShell.Run cmd, 1, False

' Ждём загрузку серверов
WScript.Sleep 31000

' Имя процесса для проверки
Dim processName
processName = "wow.exe"

' Проверяем, запущен ли процесс
Dim objWMIService, colProcesses, isRunning
Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
Set colProcesses = objWMIService.ExecQuery("Select * from Win32_Process Where Name = '" & processName & "'")

isRunning = (colProcesses.Count > 0)

' Запуск клиента, если процесс не найден
If Not isRunning Then
    If fso.FileExists(basePath & "\Wow.lnk") Then
        WshShell.Run """" & basePath & "\Wow.lnk"""
    End If
End If