from sys import platform

if platform == 'win32':
    from win32.guitest import *
elif platform == 'darwin':
    raise ImportError, "Only Win32 and X11 are currently supported."
else:
    from x11.guitest import *

# Cleanup.
del platform
