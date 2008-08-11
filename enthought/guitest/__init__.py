#------------------------------------------------------------------------------
# Copyright (c) 2006 by Enthought, Inc.
# All rights reserved.
#------------------------------------------------------------------------------
""" A collection of utilities for unit testing user interfaces.  
    Part of the ETSDevTools project of the Enthought Tool Suite.
    
    These utilities are a translation of the Perl X11::GUITest and 
    Win32::GuiTest modules.
"""
from sys import platform

if platform == 'win32':
    from win32.guitest import *
elif platform == 'darwin':
    raise ImportError, "Only Win32 and X11 are currently supported."
else:
    from x11.guitest import *

# Cleanup.
del platform
