# This file was automatically generated by SWIG (http://www.swig.org).
# Version 1.3.32
#
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _guitest
import new
new_instancemethod = new.instancemethod
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


NUL = _guitest.NUL
DEF_EVENT_SEND_DELAY = _guitest.DEF_EVENT_SEND_DELAY
DEF_KEY_SEND_DELAY = _guitest.DEF_KEY_SEND_DELAY
KEYMAP_VECTOR_SIZE = _guitest.KEYMAP_VECTOR_SIZE
KEYMAP_BIT_COUNT = _guitest.KEYMAP_BIT_COUNT
class WindowTable(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, WindowTable, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, WindowTable, name)
    __repr__ = _swig_repr
    __swig_setmethods__["Ids"] = _guitest.WindowTable_Ids_set
    __swig_getmethods__["Ids"] = _guitest.WindowTable_Ids_get
    if _newclass:Ids = _swig_property(_guitest.WindowTable_Ids_get, _guitest.WindowTable_Ids_set)
    __swig_setmethods__["NVals"] = _guitest.WindowTable_NVals_set
    __swig_getmethods__["NVals"] = _guitest.WindowTable_NVals_get
    if _newclass:NVals = _swig_property(_guitest.WindowTable_NVals_get, _guitest.WindowTable_NVals_set)
    __swig_setmethods__["Max"] = _guitest.WindowTable_Max_set
    __swig_getmethods__["Max"] = _guitest.WindowTable_Max_get
    if _newclass:Max = _swig_property(_guitest.WindowTable_Max_get, _guitest.WindowTable_Max_set)
    def __init__(self, *args): 
        """__init__(self) -> WindowTable"""
        this = _guitest.new_WindowTable(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _guitest.delete_WindowTable
    __del__ = lambda self : None;
WindowTable_swigregister = _guitest.WindowTable_swigregister
WindowTable_swigregister(WindowTable)

class KeyNameSymTable(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, KeyNameSymTable, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, KeyNameSymTable, name)
    __repr__ = _swig_repr
    __swig_setmethods__["Name"] = _guitest.KeyNameSymTable_Name_set
    __swig_getmethods__["Name"] = _guitest.KeyNameSymTable_Name_get
    if _newclass:Name = _swig_property(_guitest.KeyNameSymTable_Name_get, _guitest.KeyNameSymTable_Name_set)
    __swig_setmethods__["Sym"] = _guitest.KeyNameSymTable_Sym_set
    __swig_getmethods__["Sym"] = _guitest.KeyNameSymTable_Sym_get
    if _newclass:Sym = _swig_property(_guitest.KeyNameSymTable_Sym_get, _guitest.KeyNameSymTable_Sym_set)
    def __init__(self, *args): 
        """__init__(self) -> KeyNameSymTable"""
        this = _guitest.new_KeyNameSymTable(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _guitest.delete_KeyNameSymTable
    __del__ = lambda self : None;
KeyNameSymTable_swigregister = _guitest.KeyNameSymTable_swigregister
KeyNameSymTable_swigregister(KeyNameSymTable)

DEF_WAIT = _guitest.DEF_WAIT
M_BTN1 = _guitest.M_BTN1
M_BTN2 = _guitest.M_BTN2
M_BTN3 = _guitest.M_BTN3
M_BTN4 = _guitest.M_BTN4
M_BTN5 = _guitest.M_BTN5
M_LEFT = _guitest.M_LEFT
M_MIDDLE = _guitest.M_MIDDLE
M_RIGHT = _guitest.M_RIGHT

def InitGUITest(*args):
  """
    InitGUITest()

    Initializes XTest.  This is automatically called on module import.
    """
  return _guitest.InitGUITest(*args)

def DeInitGUITest(*args):
  """
    DeInitGUITest()

    This should be called when the module is no longer used.  It is
    automatically called when Python exits via `atexit`.
    """
  return _guitest.DeInitGUITest(*args)

def SetEventSendDelay(*args):
  """
    SetEventSendDelay(unsigned long delay) -> unsigned long

    Sets the milliseconds of delay between events being sent to the X
    display.  It is usually not a good idea to set this to 0.

    Please note that this delay will also affect SendKeys.

    Returns the old delay amount in milliseconds.

    """
  return _guitest.SetEventSendDelay(*args)

def GetEventSendDelay(*args):
  """
    GetEventSendDelay() -> unsigned long

    Returns the current event sending delay amount in milliseconds.
    """
  return _guitest.GetEventSendDelay(*args)

def SetKeySendDelay(*args):
  """
    SetKeySendDelay(unsigned long delay) -> unsigned long

    Sets the milliseconds of delay between keystrokes.  Returns the old
    delay amount in milliseconds.

    """
  return _guitest.SetKeySendDelay(*args)

def GetKeySendDelay(*args):
  """
    GetKeySendDelay() -> unsigned long

    Returns the current keystroke sending delay amount in milliseconds.
    """
  return _guitest.GetKeySendDelay(*args)

def GetWindowName(*args):
  """
    GetWindowName(unsigned long win) -> char

    Returns the window name for the specified window Id.  undef is
    returned if name could not be obtained.

      # Return the name of the window that has the input focus.
      my $WinName = GetWindowName(GetInputFocus());

    """
  return _guitest.GetWindowName(*args)

def SetWindowName(*args):
  """
    SetWindowName(unsigned long win, char name) -> int

    Sets the window name for the specified window Id.  zero is returned
    on failure, non-zero for success.

    """
  return _guitest.SetWindowName(*args)

def GetRootWindow(*args):
  """
    GetRootWindow() -> unsigned long

    Returns the root window Id.  This is the top/root level window that
    all other windows are under.
    """
  return _guitest.GetRootWindow(*args)

def GetChildWindows(*args):
  """
    GetChildWindows(unsigned long win, unsigned int nchild) -> unsigned long

    Returns an array of the child windows for the specified window Id.
    """
  return _guitest.GetChildWindows(*args)

def MoveMouseAbs(*args):
  """
    MoveMouseAbs(int x, int y) -> int

    Moves the mouse cursor to the specified absolute position. zero is
    returned on failure, non-zero for success.
    """
  return _guitest.MoveMouseAbs(*args)

def GetMousePos(*args):
  """
    GetMousePos(int root_x, int root_y)

    Returns an array containing the position of the mouse cursor.

      my ($x, $y) = GetMousePos(); 

    """
  return _guitest.GetMousePos(*args)

def PressMouseButton(*args):
  """
    PressMouseButton(int button) -> int

    Presses the specified mouse button.  Available mouse buttons are:
    M_LEFT, M_MIDDLE, M_RIGHT.  Also, you could use the logical Id for the
    button: M_BTN1, M_BTN2, M_BTN3, M_BTN4, M_BTN5.  These are all
    available through the :CONST export tag.

    zero is returned on failure, non-zero for success.

    """
  return _guitest.PressMouseButton(*args)

def ReleaseMouseButton(*args):
  """
    ReleaseMouseButton(int button) -> int

    Releases the specified mouse button.  Available mouse buttons are:
    M_LEFT, M_MIDDLE, M_RIGHT.  Also, you could use the logical Id for the
    button: M_BTN1, M_BTN2, M_BTN3, M_BTN4, M_BTN5.  These are all
    available through the :CONST export tag.

    zero is returned on failure, non-zero for success.

    """
  return _guitest.ReleaseMouseButton(*args)

def SendKeys(*args):
  """
    SendKeys(char keys) -> int

    Sends keystrokes to the window that has the input focus.

    The keystrokes to send are those specified in KEYS.  Some characters
    have special meaning, they are:

    Modifier Keys
    -------------
    
    - ^    CTRL
    - %    ALT
    - +    SHIFT

    Other Keys
    ----------
    
    - ~    ENTER
    - ()   modifier delimiters
    - {}   quote delimiters

    Simply, one can send a text string like so::

            SendKeys('Hello, how are you today?');

    Parentheses allow a modifier to work on one or more characters.  For
    example::

            SendKeys('%(f)q'); # Alt-f, then press q
            SendKeys('%(fa)^(m)'); # Alt-f, Alt-a, Ctrl-m
            SendKeys('+(abc)'); # Uppercase ABC using shift modifier
            SendKeys('^(+(l))'); # Ctrl-Shift-l
            SendKeys('+'); # Press shift

    Braces are used to quote special characters, for utilizing aliased key
    names, or for special functionality. Multiple characters can be
    specified in a brace by space delimiting the entries.  Characters can
    be repeated using a number that is space delimited after the
    preceeding key.

    Quote Special Characters::

        SendKeys('{{}'); # {
        SendKeys('{+}'); # +

    You can also use QuoteStringForSendKeys to perform quoting.

    Aliased Key Names::
        
            SendKeys('{BAC}'); # Backspace
            SendKeys('{F1 F2 F3}'); # F1, F2, F3
            SendKeys('{TAB 3}'); # Press TAB 3 times
            SendKeys('{SPC 3 a b c}'); # Space 3 times, a, b, c

    Special Functionality::
        
            # Pause execution for 500 milliseconds
            SendKeys('{PAUSE 500}');

    Combinations::
        
            SendKeys('abc+(abc){TAB PAUSE 500}'); # a, b, c, A, B, C, Tab, Pause 500
            SendKeys('+({a b c})'); # A, B, C

    The following abbreviated key names are currently recognized within a
    brace set.  If you don't see the desired key, you can still use the
    unabbreviated name for the key.  If you are unsure of this name,
    utilize the xev (X event view) tool, press the key you want and look
    at the tools output for the name of that key.  Names that are in the
    list below can be utilized regardless of case.  Ones that aren't in
    this list are going to be case sensitive and also not abbreviated.
    For example, using 'xev' you will find that the name of the backspace
    key is BackSpace, so you could use {BackSpace} in place of {bac} if
    you really wanted to.

            ====    ===========
            Name    Action
            ====    ===========
            BAC     BackSpace
            BS      BackSpace
            BKS     BackSpace
            BRE     Break
            CAN     Cancel
            CAP     Caps_Lock
            DEL     Delete
            DOW     Down
            END     End
            ENT     Return
            ESC     Escape
            F1      F1
            ...     ...
            F12     F12
            HEL     Help
            HOM     Home
            INS     Insert
            LAL     Alt_L
            LCT     Control_L
            LEF     Left
            LSH     Shift_L
            LSK     Super_L
            MNU     Menu
            NUM     Num_Lock
            PGD     Page_Down
            PGU     Page_Up
            PRT     Print
            RAL     Alt_R
            RCT     Control_R
            RIG     Right
            RSH     Shift_R
            RSK     Super_R
            SCR     Scroll_Lock
            SPA     Space
            SPC     Space
            TAB     Tab
            UP      Up
            ====    ===========

    Zero is returned on failure, non-zero for success.

    """
  return _guitest.SendKeys(*args)

def PressKey(*args):
  """
    PressKey(char key) -> int

    Presses the specified key.

    One can utilize the abbreviated key names from the table
    listed above as outlined in the following example:

      # Alt-n
      PressKey('LAL'); # Left Alt
      PressKey('n');
      ReleaseKey('n');
      ReleaseKey('LAL');

      # Uppercase a
      PressKey('LSH'); # Left Shift
      PressKey('a'); 
      ReleaseKey('a');
      ReleaseKey('LSH');

    The ReleaseKey calls in the above example are there to set
    both key states back.

    zero is returned on failure, non-zero for success.

    """
  return _guitest.PressKey(*args)

def ReleaseKey(*args):
  """
    ReleaseKey(char key) -> int

    Releases the specified key.  Normally follows a PressKey call.

    One can utilize the abbreviated key names from the table
    listed above.

      ReleaseKey('n');

    zero is returned on failure, non-zero for success.

    """
  return _guitest.ReleaseKey(*args)

def PressReleaseKey(*args):
  """
    PressReleaseKey(char key) -> int

    Presses and releases the specified key.

    One can utilize the abbreviated key names from the table
    listed above.

      PressReleaseKey('n');

    This function is effected by the key send delay.

    zero is returned on failure, non-zero for success.

    """
  return _guitest.PressReleaseKey(*args)

def IsKeyPressed(*args):
  """
    IsKeyPressed(char key) -> int

    Determines if the specified key is currently being pressed.

    You can specify such things as 'bac' or the unabbreviated form
    'BackSpace' as covered in the SendKeys information.  Brace forms such
    as '{bac}' are unsupported.  A '{' is taken literally and letters are
    case sensitive.

      if (IsKeyPressed('esc')) {  # Is Escape pressed?
      if (IsKeyPressed('a')) { # Is a pressed?
      if (IsKeyPressed('A')) { # Is A pressed?

    Returns non-zero for true, zero for false.

    """
  return _guitest.IsKeyPressed(*args)

def IsMouseButtonPressed(*args):
  """
    IsMouseButtonPressed(int button) -> int

    Determines if the specified mouse button is currently being pressed.

    Available mouse buttons are: M_LEFT, M_MIDDLE, M_RIGHT.  Also, you
    could use the logical Id for the button: M_BTN1, M_BTN2, M_BTN3,
    M_BTN4, M_BTN5.  These are all available through the :CONST export
    tag.

      if (IsMouseButtonPressed(M_LEFT)) { # Is left button pressed?

    Returns non-zero for true, zero for false.

    """
  return _guitest.IsMouseButtonPressed(*args)

def IsWindow(*args):
  """
    IsWindow(unsigned long win) -> int

    zero is returned if the specified window Id is not for something that
    can be recognized as a window.  non-zero is returned if it looks like
    a window.
    """
  return _guitest.IsWindow(*args)

def IsWindowViewable(*args):
  """
    IsWindowViewable(unsigned long win) -> int

    zero is returned if the specified window Id is for a window that
    isn't viewable.  non-zero is returned if the window is viewable.
    """
  return _guitest.IsWindowViewable(*args)

def MoveWindow(*args):
  """
    MoveWindow(unsigned long win, int x, int y) -> int

    Moves the window to the specified location.  zero is returned on
    failure, non-zero for success.
    """
  return _guitest.MoveWindow(*args)

def ResizeWindow(*args):
  """
    ResizeWindow(unsigned long win, int w, int h) -> int

    Resizes the window to the specified size.  zero is returned on
    failure, non-zero for success.
    """
  return _guitest.ResizeWindow(*args)

def IconifyWindow(*args):
  """
    IconifyWindow(unsigned long win) -> int

    Minimizes (Iconifies) the specified window.  zero is returned on
    failure, non-zero for success.

    """
  return _guitest.IconifyWindow(*args)

def UnIconifyWindow(*args):
  """
    UnIconifyWindow(unsigned long win) -> int

    Unminimizes (UnIconifies) the specified window.  zero is returned on
    failure, non-zero for success.

    """
  return _guitest.UnIconifyWindow(*args)

def RaiseWindow(*args):
  """
    RaiseWindow(unsigned long win) -> int

    Raises the specified window to the top of the stack, so that no other
    windows cover it.  zero is returned on failure, non-zero for success.
    """
  return _guitest.RaiseWindow(*args)

def LowerWindow(*args):
  """
    LowerWindow(unsigned long win) -> int

    Lowers the specified window to the bottom of the stack, so other
    existing windows will cover it.  zero is returned on failure, non-zero
    for success.
    """
  return _guitest.LowerWindow(*args)

def GetInputFocus(*args):
  """
    GetInputFocus() -> unsigned long

    Returns the window that currently has the input focus.
    """
  return _guitest.GetInputFocus(*args)

def SetInputFocus(*args):
  """
    SetInputFocus(unsigned long win) -> int

    Sets the specified window to be the one that has the input focus.
    zero is returned on failure, non-zero for success.
    """
  return _guitest.SetInputFocus(*args)

def GetWindowPos(*args):
  """
    GetWindowPos(unsigned long win, int x, int y, int width, int height)

    Returns an array containing the position information for the
    specified window.

      my ($x, $y, $width, $height) = GetWindowPos(GetRootWindow());

    """
  return _guitest.GetWindowPos(*args)

def GetParentWindow(*args):
  """
    GetParentWindow(unsigned long win) -> unsigned long

    Returns the parent of the specified window.  zero is returned if
    parent couldn't be determined (i.e., root window).
    """
  return _guitest.GetParentWindow(*args)

def GetScreenRes(*args):
  """
    GetScreenRes(int res_x, int res_y)

    Returns the screen resolution.

      my ($x, $y) = GetScreenRes();

    """
  return _guitest.GetScreenRes(*args)

def GetScreenDepth(*args):
  """
    GetScreenDepth() -> int

    Returns the color depth for the screen.  Value is represented as
    bits, i.e. 16.

      my $depth = GetScreenDepth();

    """
  return _guitest.GetScreenDepth(*args)
import os
import time
import re
import atexit

def FindWindowLike(title, start=None):
    """Finds the window Ids of the windows matching the specified
    title regex.  Optionally one can specify the window to start
    under; which would allow one to constrain the search to child
    windows of that window.

    An array of window Ids is returned for the matches found.  An
    empty array is returned if no matches were found.

       >>> w = FindWindowLike('gedit')
    """
    t_re = re.compile(r'%s'%title)
    if start is None:
        start = GetRootWindow()
    wins = []
    winname = GetWindowName(start) or ''
    if t_re.search(winname):
        wins.append(start)

    for child in GetChildWindows(start):
        winname = GetWindowName(child) or ''
        if t_re.search(winname):
            wins.append(child)
    return wins

def WaitWindowLike(title, start=None, wait=DEF_WAIT):
    """Waits for a window to come up that matches the specified title
    regex.  Optionally one can specify the window to start under;
    which would allow one to constrain the search to child windows of
    that window.

    One can optionally specify an alternative wait amount in seconds.
    A window will keep being looked for that matches the specified
    title regex until this amount of time has been reached.  The
    default amount is defined in the DEF_WAIT constant.

    If a window is going to be manipulated by input,
    WaitWindowViewable is the more robust solution to utilize.

    An array of window Ids is returned for the matches found.  An
    empty array is returned if no matches were found.

    >>> w = WaitWindowLike('gedit');
    """
    if start is None:
        start = GetRootWindow()
    wins = []
    t = 0
    while t < wait:
        wins = FindWindowLike(title, start)
        if wins:
            return wins
        time.sleep(0.5)
        t += 0.5
    return wins

def WaitWindowViewable(title, start=None, wait=DEF_WAIT):
    """Similar to WaitWindow, but only recognizes windows that are
    viewable.  When GUI applications are started, their window isn't
    necessarily viewable yet, let alone available for input, so this
    function is very useful.

    Likewise, this function will only return an array of the matching
    window Ids for those windows that are viewable.  An empty array is
    returned if no matches were found.
    """
    if start is None:
        start = GetRootWindow()
    wins = []
    t = 0
    while t < wait:
        for win in FindWindowLike(title, start):
            if IsWindowViewable(win):
                wins.append(win)
        if wins:
            return wins
        time.sleep(0.5)
        t += 0.5

def WaitWindowClose(win, wait=DEF_WAIT):
    """Waits for the specified window to close.

    One can optionally specify an alternative wait amount in
    seconds. The window will keep being checked to see if it has
    closed until this amount of time has been reached.  The default
    amount is defined in the DEF_WAIT constant.

    zero is returned if window is not gone, non-zero if it is gone.
    """
    t = 0
    while t < wait:
        if not IsWindow(win):
            return 1
        time.sleep(0.5)
        t += 0.5
    return 0    

def ClickMouseButton(button):
    """Clicks the specified mouse button.  Available mouse buttons
    are: M_LEFT, M_MIDDLE, M_RIGHT.  Also, you could use the logical
    Id for the button: M_BTN1, M_BTN2, M_BTN3, M_BTN4, M_BTN5.

    zero is returned on failure, non-zero for success.
    """
    if not PressMouseButton(button) or \
       not ReleaseMouseButton(button):
        return 0
    return 1

def ClickWindow(win, x_offset=0, y_offset=0, button=M_LEFT):
    """Clicks on the specified window with the mouse.

    Optionally one can specify the X offset and Y offset.  By default,
    the top left corner of the window is clicked on, with these two
    parameters one can specify a different position to be clicked on.

    One can also specify an alternative button.  The default button is
    M_LEFT, but M_MIDDLE and M_RIGHT may be specified too.  Also, you
    could use the logical Id for the button: M_BTN1, M_BTN2, M_BTN3,
    M_BTN4, M_BTN5.  These are all available through the :CONST export
    tag.

    zero is returned on failure, non-zero for success
    """
    x, y, w, h = GetWindowPos(win)
    if (x< -1000000000) and (w > 1000000000):
        return 0
    if not MoveMouseAbs(x + x_offset, y + y_offset):
        return 0
    if not ClickMouseButton(button):
        return 0
    return 1
    
def GetWindowFromPoint(x, y):
    """Returns the window that is at the specified point.

    zero is returned if there are no matches (i.e., off screen).
    """
    lastmatch = 0
    for win in GetChildWindows(GetRootWindow()):
        x1, y1, w, h = GetWindowPos(win)
        if (x1 < 0) or (y1 < 0):
            continue
        x2, y2 = x1 + w, y1 + h
        if (x >= x1) and (x <= x2) and (y >= y1) and (y <= y2):
            lastmatch = win
    return lastmatch

def IsChild(parent, win):
    """Determines if the specified window is a child of the specified
    parent.

    zero is returned for false, non-zero for true.
    """
    for child in GetChildWindows(parent):
        if child == win and child != parent:
            return 1
    return 0

def QuoteStringForSendKeys(s=''):
    """Quotes {} characters in the specified string that would be
    interpreted as having special meaning if sent to SendKeys
    directly.  This function would be useful if you had a text file in
    which you wanted to use each line of the file as input to the
    SendKeys function, but didn't want any special interpretation of
    the characters in the file.

    Returns the quoted string, undef is returned on error.

    >>> # Quote ~, \%, etc. as \{~\}, \{\%\}, etc for literal use in SendKeys. 
    >>> SendKeys( QuoteStringForSendKeys('Hello: ~%^(){}+') )
    """
    p = re.compile(r'(\^|\%|\+|\~|\(|\)|\{|\})')
    return p.sub(r'{\1}', s)
    
    
def StartApp(cmdline):
    """Uses the shell to execute a program.  A primitive method is
    used to detach from the shell, so this function returns as soon as
    the program is called.  Useful for starting GUI applications and
    then going on to work with them.

    zero is returned on failure, non-zero for success

    >>> StartApp('gedit')
    """
    if not cmdline.endswith('&'):
        cmdline += ' &'
    return os.system(cmdline)

def RunApp(cmdline):
    """Uses the shell to execute a program until its completion.

    Return value will be application specific, however -1 is returned
    to indicate a failure in starting the program.

    >>> RunApp('/work/myapp')
    """
    return os.system(cmdline)


# Called at startup.
InitGUITest()

# Call this atleast when Python exits.
atexit.register(DeInitGUITest)



