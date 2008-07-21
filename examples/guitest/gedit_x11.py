#!/usr/bin/env python
"""Simple example to show how guitest may be used to automate tasks.
"""
# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2006, Enthought, Inc.
# License: BSD Style.

from enthought import guitest
import time, sys

try:
    guitest.StartApp('gedit')
except:
    print 'This example does not work on this platform.'
    sys.exit()

print "Waiting for window ..."
time.sleep(3)
# The title for the window can be a regular expression.
windows = guitest.FindWindowLike(r'(Untitled)|(Unsaved).*gedit')
w = windows[0]
print "Moving window to (0,0)."
guitest.MoveWindow(w, 0, 0)
print 'Resizing window.'
guitest.ResizeWindow(w, 800, 600)
guitest.SetInputFocus(w)
print 'Moving mouse to the middle of the window.'
guitest.MoveMouseAbs(400, 300)
# Try to pick the menu item to turn on Python syntax highlighting by
# pressing: Alt v h UP RIGHT DOWN DOWN DOWN DOWN DOWN ENTER
guitest.SendKeys('%(v)h{UP RIG DOW DOW DOW DOW DOW ENT}')
# Now write some Python code!
guitest.SendKeys('import sys{ENT}print "hello world!"{ENT}')

