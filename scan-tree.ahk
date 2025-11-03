; Example: Press Ctrl+Alt+W to open/activate Notepad

#Requires AutoHotkey v2.0

;Camera
;ahk_class ApplicationFrameWindow
;ahk_exe ApplicationFrameHost.exe
;ahk_pid 18816
;ahk_id 133368

^!w:: {
    Loop 550 {
        WinActivate("ahk_exe ApplicationFrameHost.exe ahk_class ApplicationFrameWindow")
        SendInput("{Enter}")
        Sleep(100)

        WinActivate("Raspberry_Pi_3B remote shell – Raspberry Pi Connect - Thorium")
        SendInput("{Enter}")
        Sleep(100)
    }
}

Esc::ExitApp  ; Exits the entire script