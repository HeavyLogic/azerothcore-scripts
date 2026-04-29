Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Папка, где лежит VBS
basePath = fso.GetParentFolderName(WScript.ScriptFullName)

cmd = "wt " & _
      "new-tab cmd /k ""cd /d """ & basePath & """ && title MYSQL && call MySQL.bat"" ; " & _
      "new-tab cmd /k ""cd /d """ & basePath & """ && timeout /t 8 >nul && title AUTH && authserver"" ; " & _
      "new-tab cmd /k ""cd /d """ & basePath & """ && timeout /t 11 >nul && title WORLD && worldserver"""

WshShell.Run cmd, 1, False

' Ждём загрузку
WScript.Sleep 31000

' Запуск клиента
If fso.FileExists(basePath & "\Wow.lnk") Then
    WshShell.Run """" & basePath & "\Wow.lnk"""
End If