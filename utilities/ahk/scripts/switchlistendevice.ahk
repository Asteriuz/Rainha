#KeyHistory, 0
ListLines, Off
SetBatchLines, -1

isExist:=WinExist("ahk_exe rundll32.exe ahk_class #32770")
Run, % "rundll32.exe shell32.dll,Control_RunDLL mmsys.cpl,,recording",,, uPID
WinWait, Som
If Not ErrorLevel
{ 
    ControlSend,SysListView321,{Down 2}
    ControlClick, % "Button3", % "ahk_pid"uPID,,, 3
    WinWait, % "A"
    PostMessage, 0x1330, 1,, % "SysTabControl321", % "ahk_pid"uPID
    WinWait, % "A"
    ControlGet, isEnabled, Checked,, % "Button1", % "ahk_pid"uPID
    Control, % isEnabled ? "UnCheck":"Check",, % "Button1", % "ahk_pid"uPID
    Send, {TAB}
    Send, {TAB}
    Send, {TAB}
    Send, {TAB}
    Send, {TAB}
    Send, {Enter}
    Process, Close, % uPID
}
IfEqual, ErrorLevel, % True, MsgBox, % 2621 (isExist ? 92:60)
, % isExist ? "Info:":"Oops:"
, % isExist ? "Close other window":"Something went wrong!"
    , % isExist ? 1.5:3
    KeyWait, % A_ThisHotkey
    Exit, uPID:=isEnabled:=isExist:=""