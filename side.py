import os
if os.name == 'posix':    
    from subprocess import check_output
elif os.name == 'nt':
    import win32api, win32con, win32process
    from ctypes import windll
    user32 = windll.user32

def get_locale():
    if os.name == 'nt':
        w = user32.GetForegroundWindow() 
        tid = user32.GetWindowThreadProcessId(w, 0) 
        return hex(user32.GetKeyboardLayout(tid))
    elif os.name == 'posix':
        return check_output(["xkblayout-state", "print", "%s"])

print(get_locale())