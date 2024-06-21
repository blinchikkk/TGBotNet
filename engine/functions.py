import os
import platform

def clear_console():
    os_type = platform.system()
    if os_type == "Windows":
        os.system('cls')
    else:
        os.system('clear')
