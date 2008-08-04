# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _guitest

def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "this"):
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name) or (name == "thisown"):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


SW_HIDE = _guitest.SW_HIDE
SW_NORMAL = _guitest.SW_NORMAL
SW_SHOWNORMAL = _guitest.SW_SHOWNORMAL
SW_SHOWMINIMIZED = _guitest.SW_SHOWMINIMIZED
SW_MAXIMIZE = _guitest.SW_MAXIMIZE
SW_SHOWMAXIMIZED = _guitest.SW_SHOWMAXIMIZED
SW_SHOWNOACTIVATE = _guitest.SW_SHOWNOACTIVATE
SW_SHOW = _guitest.SW_SHOW
SW_MINIMIZE = _guitest.SW_MINIMIZE
SW_SHOWMINNOACTIVE = _guitest.SW_SHOWMINNOACTIVE
SW_SHOWNA = _guitest.SW_SHOWNA
SW_RESTORE = _guitest.SW_RESTORE
SW_SHOWDEFAULT = _guitest.SW_SHOWDEFAULT
SW_FORCEMINIMIZE = _guitest.SW_FORCEMINIMIZE
SW_MAX = _guitest.SW_MAX
LVS_ICON = _guitest.LVS_ICON
LVS_REPORT = _guitest.LVS_REPORT
LVS_SMALLICON = _guitest.LVS_SMALLICON
LVS_LIST = _guitest.LVS_LIST
LVS_TYPEMASK = _guitest.LVS_TYPEMASK
LVS_SINGLESEL = _guitest.LVS_SINGLESEL
LVS_SHOWSELALWAYS = _guitest.LVS_SHOWSELALWAYS
LVS_SORTASCENDING = _guitest.LVS_SORTASCENDING
LVS_SORTDESCENDING = _guitest.LVS_SORTDESCENDING
LVS_SHAREIMAGELISTS = _guitest.LVS_SHAREIMAGELISTS
LVS_NOLABELWRAP = _guitest.LVS_NOLABELWRAP
LVS_AUTOARRANGE = _guitest.LVS_AUTOARRANGE
LVS_EDITLABELS = _guitest.LVS_EDITLABELS
LVS_NOSCROLL = _guitest.LVS_NOSCROLL
LVS_TYPESTYLEMASK = _guitest.LVS_TYPESTYLEMASK
LVS_ALIGNTOP = _guitest.LVS_ALIGNTOP
LVS_ALIGNLEFT = _guitest.LVS_ALIGNLEFT
LVS_ALIGNMASK = _guitest.LVS_ALIGNMASK
LVS_OWNERDRAWFIXED = _guitest.LVS_OWNERDRAWFIXED
LVS_NOCOLUMNHEADER = _guitest.LVS_NOCOLUMNHEADER
LVS_NOSORTHEADER = _guitest.LVS_NOSORTHEADER
VK_LBUTTON = _guitest.VK_LBUTTON
VK_RBUTTON = _guitest.VK_RBUTTON
VK_CANCEL = _guitest.VK_CANCEL
VK_MBUTTON = _guitest.VK_MBUTTON
VK_BACK = _guitest.VK_BACK
VK_TAB = _guitest.VK_TAB
VK_CLEAR = _guitest.VK_CLEAR
VK_RETURN = _guitest.VK_RETURN
VK_SHIFT = _guitest.VK_SHIFT
VK_CONTROL = _guitest.VK_CONTROL
VK_MENU = _guitest.VK_MENU
VK_PAUSE = _guitest.VK_PAUSE
VK_CAPITAL = _guitest.VK_CAPITAL
VK_KANA = _guitest.VK_KANA
VK_HANGEUL = _guitest.VK_HANGEUL
VK_HANGUL = _guitest.VK_HANGUL
VK_JUNJA = _guitest.VK_JUNJA
VK_FINAL = _guitest.VK_FINAL
VK_HANJA = _guitest.VK_HANJA
VK_KANJI = _guitest.VK_KANJI
VK_ESCAPE = _guitest.VK_ESCAPE
VK_CONVERT = _guitest.VK_CONVERT
VK_NONCONVERT = _guitest.VK_NONCONVERT
VK_ACCEPT = _guitest.VK_ACCEPT
VK_MODECHANGE = _guitest.VK_MODECHANGE
VK_SPACE = _guitest.VK_SPACE
VK_PRIOR = _guitest.VK_PRIOR
VK_NEXT = _guitest.VK_NEXT
VK_END = _guitest.VK_END
VK_HOME = _guitest.VK_HOME
VK_LEFT = _guitest.VK_LEFT
VK_UP = _guitest.VK_UP
VK_RIGHT = _guitest.VK_RIGHT
VK_DOWN = _guitest.VK_DOWN
VK_SELECT = _guitest.VK_SELECT
VK_PRINT = _guitest.VK_PRINT
VK_EXECUTE = _guitest.VK_EXECUTE
VK_SNAPSHOT = _guitest.VK_SNAPSHOT
VK_INSERT = _guitest.VK_INSERT
VK_DELETE = _guitest.VK_DELETE
VK_HELP = _guitest.VK_HELP
VK_LWIN = _guitest.VK_LWIN
VK_RWIN = _guitest.VK_RWIN
VK_APPS = _guitest.VK_APPS
VK_SLEEP = _guitest.VK_SLEEP
VK_NUMPAD0 = _guitest.VK_NUMPAD0
VK_NUMPAD1 = _guitest.VK_NUMPAD1
VK_NUMPAD2 = _guitest.VK_NUMPAD2
VK_NUMPAD3 = _guitest.VK_NUMPAD3
VK_NUMPAD4 = _guitest.VK_NUMPAD4
VK_NUMPAD5 = _guitest.VK_NUMPAD5
VK_NUMPAD6 = _guitest.VK_NUMPAD6
VK_NUMPAD7 = _guitest.VK_NUMPAD7
VK_NUMPAD8 = _guitest.VK_NUMPAD8
VK_NUMPAD9 = _guitest.VK_NUMPAD9
VK_MULTIPLY = _guitest.VK_MULTIPLY
VK_ADD = _guitest.VK_ADD
VK_SEPARATOR = _guitest.VK_SEPARATOR
VK_SUBTRACT = _guitest.VK_SUBTRACT
VK_DECIMAL = _guitest.VK_DECIMAL
VK_DIVIDE = _guitest.VK_DIVIDE
VK_F1 = _guitest.VK_F1
VK_F2 = _guitest.VK_F2
VK_F3 = _guitest.VK_F3
VK_F4 = _guitest.VK_F4
VK_F5 = _guitest.VK_F5
VK_F6 = _guitest.VK_F6
VK_F7 = _guitest.VK_F7
VK_F8 = _guitest.VK_F8
VK_F9 = _guitest.VK_F9
VK_F10 = _guitest.VK_F10
VK_F11 = _guitest.VK_F11
VK_F12 = _guitest.VK_F12
VK_F13 = _guitest.VK_F13
VK_F14 = _guitest.VK_F14
VK_F15 = _guitest.VK_F15
VK_F16 = _guitest.VK_F16
VK_F17 = _guitest.VK_F17
VK_F18 = _guitest.VK_F18
VK_F19 = _guitest.VK_F19
VK_F20 = _guitest.VK_F20
VK_F21 = _guitest.VK_F21
VK_F22 = _guitest.VK_F22
VK_F23 = _guitest.VK_F23
VK_F24 = _guitest.VK_F24
VK_NUMLOCK = _guitest.VK_NUMLOCK
VK_SCROLL = _guitest.VK_SCROLL
VK_LSHIFT = _guitest.VK_LSHIFT
VK_RSHIFT = _guitest.VK_RSHIFT
VK_LCONTROL = _guitest.VK_LCONTROL
VK_RCONTROL = _guitest.VK_RCONTROL
VK_LMENU = _guitest.VK_LMENU
VK_RMENU = _guitest.VK_RMENU
VK_PROCESSKEY = _guitest.VK_PROCESSKEY
VK_ATTN = _guitest.VK_ATTN
VK_CRSEL = _guitest.VK_CRSEL
VK_EXSEL = _guitest.VK_EXSEL
VK_EREOF = _guitest.VK_EREOF
VK_PLAY = _guitest.VK_PLAY
VK_ZOOM = _guitest.VK_ZOOM
VK_NONAME = _guitest.VK_NONAME
VK_PA1 = _guitest.VK_PA1
VK_OEM_CLEAR = _guitest.VK_OEM_CLEAR
KEYEVENTF_EXTENDEDKEY = _guitest.KEYEVENTF_EXTENDEDKEY
KEYEVENTF_KEYUP = _guitest.KEYEVENTF_KEYUP
GWL_ID = _guitest.GWL_ID
GWL_STYLE = _guitest.GWL_STYLE
GWL_EXSTYLE = _guitest.GWL_EXSTYLE
WM_MOUSEACTIVATE = _guitest.WM_MOUSEACTIVATE
WM_MOUSEMOVE = _guitest.WM_MOUSEMOVE
WM_LBUTTONDOWN = _guitest.WM_LBUTTONDOWN
WM_LBUTTONUP = _guitest.WM_LBUTTONUP
WM_LBUTTONDBLCLK = _guitest.WM_LBUTTONDBLCLK
WM_RBUTTONDOWN = _guitest.WM_RBUTTONDOWN
WM_RBUTTONUP = _guitest.WM_RBUTTONUP
WM_RBUTTONDBLCLK = _guitest.WM_RBUTTONDBLCLK
WM_MBUTTONDOWN = _guitest.WM_MBUTTONDOWN
WM_MBUTTONUP = _guitest.WM_MBUTTONUP
WM_MBUTTONDBLCLK = _guitest.WM_MBUTTONDBLCLK
WM_MOUSEWHEEL = _guitest.WM_MOUSEWHEEL
WM_MOUSEFIRST = _guitest.WM_MOUSEFIRST
WM_COMMAND = _guitest.WM_COMMAND
WM_SYSCOMMAND = _guitest.WM_SYSCOMMAND
TCM_FIRST = _guitest.TCM_FIRST
TCM_SETCURFOCUS = _guitest.TCM_SETCURFOCUS
class VectorString(_object):
    """Proxy of C++ VectorString class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, VectorString, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, VectorString, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ std::vector<std::string > instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def empty(*args):
        """empty(self) -> bool"""
        return _guitest.VectorString_empty(*args)

    def size(*args):
        """size(self) -> size_type"""
        return _guitest.VectorString_size(*args)

    def clear(*args):
        """clear(self)"""
        return _guitest.VectorString_clear(*args)

    def swap(*args):
        """swap(self, VectorString v)"""
        return _guitest.VectorString_swap(*args)

    def get_allocator(*args):
        """get_allocator(self) -> allocator_type"""
        return _guitest.VectorString_get_allocator(*args)

    def pop_back(*args):
        """pop_back(self)"""
        return _guitest.VectorString_pop_back(*args)

    def __init__(self, *args):
        """
        __init__(self) -> VectorString
        __init__(self, VectorString ??) -> VectorString
        __init__(self, size_type size) -> VectorString
        __init__(self, size_type size, value_type value) -> VectorString
        """
        _swig_setattr(self, VectorString, 'this', _guitest.new_VectorString(*args))
        _swig_setattr(self, VectorString, 'thisown', 1)
    def push_back(*args):
        """push_back(self, value_type x)"""
        return _guitest.VectorString_push_back(*args)

    def front(*args):
        """front(self) -> value_type"""
        return _guitest.VectorString_front(*args)

    def back(*args):
        """back(self) -> value_type"""
        return _guitest.VectorString_back(*args)

    def assign(*args):
        """assign(self, size_type n, value_type x)"""
        return _guitest.VectorString_assign(*args)

    def resize(*args):
        """
        resize(self, size_type new_size)
        resize(self, size_type new_size, value_type x)
        """
        return _guitest.VectorString_resize(*args)

    def reserve(*args):
        """reserve(self, size_type n)"""
        return _guitest.VectorString_reserve(*args)

    def capacity(*args):
        """capacity(self) -> size_type"""
        return _guitest.VectorString_capacity(*args)

    def __nonzero__(*args):
        """__nonzero__(self) -> bool"""
        return _guitest.VectorString___nonzero__(*args)

    def __len__(*args):
        """__len__(self) -> size_type"""
        return _guitest.VectorString___len__(*args)

    def pop(*args):
        """pop(self) -> value_type"""
        return _guitest.VectorString_pop(*args)

    def __getslice__(*args):
        """__getslice__(self, difference_type i, difference_type j) -> VectorString"""
        return _guitest.VectorString___getslice__(*args)

    def __setslice__(*args):
        """__setslice__(self, difference_type i, difference_type j, VectorString v)"""
        return _guitest.VectorString___setslice__(*args)

    def __delslice__(*args):
        """__delslice__(self, difference_type i, difference_type j)"""
        return _guitest.VectorString___delslice__(*args)

    def __delitem__(*args):
        """__delitem__(self, difference_type i)"""
        return _guitest.VectorString___delitem__(*args)

    def __getitem__(*args):
        """__getitem__(self, difference_type i) -> value_type"""
        return _guitest.VectorString___getitem__(*args)

    def __setitem__(*args):
        """__setitem__(self, difference_type i, value_type x)"""
        return _guitest.VectorString___setitem__(*args)

    def append(*args):
        """append(self, value_type x)"""
        return _guitest.VectorString_append(*args)

    def __del__(self, destroy=_guitest.delete_VectorString):
        """__del__(self)"""
        try:
            if self.thisown: destroy(self)
        except: pass


class VectorStringPtr(VectorString):
    def __init__(self, this):
        _swig_setattr(self, VectorString, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, VectorString, 'thisown', 0)
        _swig_setattr(self, VectorString,self.__class__,VectorString)
_guitest.VectorString_swigregister(VectorStringPtr)


def GetListViewContents(*args):
    """
    GetListViewContents(HWND hWnd) -> VectorString

    Returns a list of the contents of the specified list view.
    """
    return _guitest.GetListViewContents(*args)

def IsListViewItemSel(*args):
    """
    IsListViewItemSel(HWND hWnd, char lpItem) -> BOOL

    Determines if the specified list view item is selected.

    """
    return _guitest.IsListViewItemSel(*args)

def GetTabItems(*args):
    """
    GetTabItems(HWND hWnd) -> VectorString

    Returns a list of a tab control's labels.
    """
    return _guitest.GetTabItems(*args)

def SelTabItem(*args):
    """
    SelTabItem(HWND hWnd, int iItem) -> BOOL

    Selects a tab based off an index (zero-based).
    """
    return _guitest.SelTabItem(*args)

def SelTabItemText(*args):
    """
    SelTabItemText(HWND hWnd, char lpItem) -> BOOL

    Selects a tab based off text label (case insensitive).
    """
    return _guitest.SelTabItemText(*args)

def IsTabItemSel(*args):
    """
    IsTabItemSel(HWND hWnd, char lpItem) -> BOOL

    Determines if the specified tab item is selected.
    """
    return _guitest.IsTabItemSel(*args)

def SelTreeViewItemPath(*args):
    """
    SelTreeViewItemPath(HWND hWnd, char lpPath) -> BOOL

    Selects a tree view item based off a 'path' (case insensitive).

        # Select Machine item and Processors sub-item.
        SelTreeViewItemPath(window, 'Machine|Processors')

        SelTreeViewItemPath(window, 'Item')

    """
    return _guitest.SelTreeViewItemPath(*args)

def GetTreeViewSelPath(*args):
    """
    GetTreeViewSelPath(HWND hWnd) -> char

    Returns a string containing the path (i.e., 'parent|child') of the
    currently selected tree view item.

       oldpath = GetTreeViewSelPath(window)
       SelTreeViewItemPath(window, 'Parent|Child')
       SelTreeViewItemPath(window, oldpath);

    """
    return _guitest.GetTreeViewSelPath(*args)

def GetCursorPos(*args):
    """
    GetCursorPos(int out_x, int out_y)

    Retrieves the cursor's position,in screen coordinates as (x,y) array.
    """
    return _guitest.GetCursorPos(*args)

def SendLButtonUp(*args):
    """SendLButtonUp()"""
    return _guitest.SendLButtonUp(*args)

def SendLButtonDown(*args):
    """SendLButtonDown()"""
    return _guitest.SendLButtonDown(*args)

def SendMButtonUp(*args):
    """SendMButtonUp()"""
    return _guitest.SendMButtonUp(*args)

def SendMButtonDown(*args):
    """SendMButtonDown()"""
    return _guitest.SendMButtonDown(*args)

def SendRButtonUp(*args):
    """SendRButtonUp()"""
    return _guitest.SendRButtonUp(*args)

def SendRButtonDown(*args):
    """SendRButtonDown()"""
    return _guitest.SendRButtonDown(*args)

def SendMouseMoveRel(*args):
    """SendMouseMoveRel(int x, int y)"""
    return _guitest.SendMouseMoveRel(*args)

def SendMouseMoveAbs(*args):
    """SendMouseMoveAbs(int x, int y)"""
    return _guitest.SendMouseMoveAbs(*args)

def MouseMoveAbsPix(*args):
    """
    MouseMoveAbsPix(int x, int y)

    Move the mouse cursor to the screen pixel indicated as parameter.
      # Moves to x=200, y=100 in pixel coordinates.
      MouseMoveAbsPix(200, 100);
    """
    return _guitest.MouseMoveAbsPix(*args)

def MouseMoveWheel(*args):
    """
    MouseMoveWheel(DWORD dwChange)

    Positive or negative value to direct mouse wheel movement.
    """
    return _guitest.MouseMoveWheel(*args)

def SendKeysImp(*args):
    """SendKeysImp(char s, DWORD wait)"""
    return _guitest.SendKeysImp(*args)

def GetDesktopWindow(*args):
    """
    GetDesktopWindow() -> HWND

    Returns a handle to the desktop window
    """
    return _guitest.GetDesktopWindow(*args)

def GetWindow(*args):
    """GetWindow(HWND hwnd, UINT uCmd) -> HWND"""
    return _guitest.GetWindow(*args)

def GetWindowText(*args):
    """
    GetWindowText(HWND hwnd) -> char

    Get the text name of the window as shown on the top of it.  Beware,
    this is text depends on localization.

    """
    return _guitest.GetWindowText(*args)

def GetClassName(*args):
    """
    GetClassName(HWND hwnd) -> char

    Using the same Windows library function returns the name of the class
    wo which the specified window belongs.

    See MSDN for more details.

    You can also check out MSDN to see an overview of the Window Classes.
    """
    return _guitest.GetClassName(*args)

def GetParent(*args):
    """
    GetParent(HWND hwnd) -> HWND

    A library function (see MSDN) to return the WindowID of the parent window.
    See MSDN for the special cases.
    """
    return _guitest.GetParent(*args)

def GetWindowLong(*args):
    """GetWindowLong(HWND hwnd, int index) -> long"""
    return _guitest.GetWindowLong(*args)

def SetForegroundWindow(*args):
    """
    SetForegroundWindow(HWND hWnd) -> BOOL

    See corresponding Windows functions.
    """
    return _guitest.SetForegroundWindow(*args)

def SetFocus(*args):
    """
    SetFocus(HWND hWnd) -> HWND

    Sets the keyboard focus to the specified window
    """
    return _guitest.SetFocus(*args)

def GetChildWindows(*args):
    """
    GetChildWindows(HWND hWnd, int nelem) -> HWND

    Using EnumChildWindows library function (see MSDN) it returns the
    WindowID of each child window. If the children have their own children
    the function returns them too until the tree ends.

    """
    return _guitest.GetChildWindows(*args)

def GetTopLevelWindows(*args):
    """
    GetTopLevelWindows(int nelem) -> HWND

    Using EnumWindows library function (see MSDN) it returns the WindowID
    of all the top-level window.
    """
    return _guitest.GetTopLevelWindows(*args)

def WMGetText(*args):
    """
    WMGetText(HWND hwnd) -> char

    Sends a WM_GETTEXT to a window and returns its contents
    """
    return _guitest.WMGetText(*args)

def WMSetText(*args):
    """
    WMSetText(HWND hwnd, char text) -> int

    Sends a WM_SETTEXT to a window setting its contents
    """
    return _guitest.WMSetText(*args)

def IsChild(*args):
    """
    IsChild(HWND hWndParent, HWND hWnd) -> BOOL

    Using the corresponding library function (see MSDN) it returns true if
    the second window is an immediate child or a descendant window of the
    first window.

    """
    return _guitest.IsChild(*args)

def GetChildDepth(*args):
    """
    GetChildDepth(HWND hAncestor, HWND hChild) -> DWORD

    Using the GetParent library function in a loop, returns the distance
    between an ancestor window and a child (descendant) window.

    Features/bugs:

    If the given 'ancsetor' is not really an ancestor, the return value is
    the distance of child from the root window (0). If you supply the same
    id for both the ancestor and the child you get 1.  If the ancestor you
    are checking is not 0 then the distance given is 1 larger than it
    should be.

    """
    return _guitest.GetChildDepth(*args)

def SendMessage(*args):
    """
    SendMessage(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) -> int

    This is a library function (see MSDN) used by a number of the
    functions provided by Win32::GuiTest. It sends the specified message
    to a window or windows.  HWnd is the WindowID or HWND_BROADCAST to
    send message to all top level windows.  Message is not sent to child
    windows. (If I understand this correctly this means it is sent to all
    the immediate children of the root window (0).  Msg the message wParam
    additional parameter lParam additioanl parameter

    It is most likely you won't use this directly but through one of the
    other functions .

    """
    return _guitest.SendMessage(*args)

def PostMessage(*args):
    """
    PostMessage(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) -> int

    See corresponding Windows library function in MSDN.
    """
    return _guitest.PostMessage(*args)

def CheckButton(*args):
    """
    CheckButton(HWND hwnd)

    The names say it.  Works on radio buttons and checkboxes.  For regular
    buttons, use IsWindowEnabled.
    """
    return _guitest.CheckButton(*args)

def UnCheckButton(*args):
    """
    UnCheckButton(HWND hwnd)

    The names say it.  Works on radio buttons and checkboxes.  For regular
    buttons, use IsWindowEnabled.
    """
    return _guitest.UnCheckButton(*args)

def GrayOutButton(*args):
    """
    GrayOutButton(HWND hwnd)

    The names say it.  Works on radio buttons and checkboxes.  For regular
    buttons, use IsWindowEnabled.
    """
    return _guitest.GrayOutButton(*args)

def IsCheckedButton(*args):
    """
    IsCheckedButton(HWND hwnd) -> BOOL

    The names say it.  Works on radio buttons and checkboxes.  For regular
    buttons, use IsWindowEnabled.
    """
    return _guitest.IsCheckedButton(*args)

def IsGrayedButton(*args):
    """
    IsGrayedButton(HWND hwnd) -> BOOL

    The names say it.  Works on radio buttons and checkboxes.  For regular
    buttons, use IsWindowEnabled.
    """
    return _guitest.IsGrayedButton(*args)

def IsWindow(*args):
    """IsWindow(HWND hwnd) -> BOOL"""
    return _guitest.IsWindow(*args)

def ScreenToClient(*args):
    """ScreenToClient(HWND hwnd, int x, int y, int out_x, int out_y)"""
    return _guitest.ScreenToClient(*args)

def ClientToScreen(*args):
    """ClientToScreen(HWND hwnd, int x, int y, int out_x, int out_y)"""
    return _guitest.ClientToScreen(*args)

def GetCaretPos(*args):
    """
    GetCaretPos(HWND hwnd, int out_x, int out_y)

    Retrieves the caret's position, in client coordinates as (x,y)
    array. (Like Windows function)
    """
    return _guitest.GetCaretPos(*args)

def GetFocus(*args):
    """GetFocus(HWND hwnd) -> HWND"""
    return _guitest.GetFocus(*args)

def GetActiveWindow(*args):
    """GetActiveWindow(HWND hwnd) -> HWND"""
    return _guitest.GetActiveWindow(*args)

def GetForegroundWindow(*args):
    """GetForegroundWindow() -> HWND"""
    return _guitest.GetForegroundWindow(*args)

def SetActiveWindow(*args):
    """SetActiveWindow(HWND hwnd) -> HWND"""
    return _guitest.SetActiveWindow(*args)

def EnableWindow(*args):
    """EnableWindow(HWND hwnd, BOOL fEnable) -> BOOL"""
    return _guitest.EnableWindow(*args)

def IsWindowEnabled(*args):
    """IsWindowEnabled(HWND hwnd) -> BOOL"""
    return _guitest.IsWindowEnabled(*args)

def IsWindowVisible(*args):
    """IsWindowVisible(HWND hwnd) -> BOOL"""
    return _guitest.IsWindowVisible(*args)

def ShowWindow(*args):
    """ShowWindow(HWND hwnd, int nCmdShow) -> BOOL"""
    return _guitest.ShowWindow(*args)

def ScreenToNorm(*args):
    """
    ScreenToNorm(int x, int y, int out_x, int out_y)

    Returns normalised coordinates of given point (0-FFFF as a fraction of
    screen resolution)

    """
    return _guitest.ScreenToNorm(*args)

def NormToScreen(*args):
    """
    NormToScreen(int x, int y, int out_x, int out_y)

    The opposite transformation to ScreenToNorm
    """
    return _guitest.NormToScreen(*args)

def GetScreenRes(*args):
    """
    GetScreenRes(int out_x, int out_y)

    Returns screen resolution.
    """
    return _guitest.GetScreenRes(*args)

def GetWindowRect(*args):
    """GetWindowRect(HWND hWnd, int left, int top, int right, int bottom)"""
    return _guitest.GetWindowRect(*args)

def GetComboText(*args):
    """GetComboText(HWND hwnd, int index) -> char"""
    return _guitest.GetComboText(*args)

def GetListText(*args):
    """GetListText(HWND hwnd, int index) -> char"""
    return _guitest.GetListText(*args)

def GetComboContents(*args):
    """GetComboContents(HWND hWnd) -> VectorString"""
    return _guitest.GetComboContents(*args)

def SelComboItem(*args):
    """
    SelComboItem(HWND hWnd, int iItem) -> BOOL

    Selects an item in the combo box based off an index (zero-based).
    """
    return _guitest.SelComboItem(*args)

def SelComboItemText(*args):
    """
    SelComboItemText(HWND hWnd, char lpItem) -> BOOL

    Selects an item in the combo box based off text (case insensitive).
    """
    return _guitest.SelComboItemText(*args)

def GetListContents(*args):
    """
    GetListContents(HWND hWnd) -> VectorString

    Fetch the contents of the list and combo boxes.
    """
    return _guitest.GetListContents(*args)

def IsKeyPressed(*args):
    """
    IsKeyPressed(char name) -> BOOL

    Wrapper around the GetAsyncKeyState API function. Returns TRUE if the
    user presses the specified key.

        IsKeyPressed('ESC')
        IsKeyPressed('A')
        IsKeyPressed('DOWN')

    """
    return _guitest.IsKeyPressed(*args)

def GetSubMenu(*args):
    """GetSubMenu(HMENU hMenu, int nPos) -> HMENU"""
    return _guitest.GetSubMenu(*args)

def GetMenuItemInfo(*args):
    """
    GetMenuItemInfo(HMENU hMenu, UINT uItem) -> VectorString

    Receives a menu handler (one we got from GetMenu or GetSubMenu) and a
    number (which is the location of the item within the given menu).

    Returns a hash of which there are currently 2 keys: type can be either
    'string' or 'separator' - this is the type of the menu item text is
    the visible text of the menu item (provided only for 'string' type)

    WARNING: This is an experimental function. Its behavior might change.

    """
    return _guitest.GetMenuItemInfo(*args)

def GetMenuItemCount(*args):
    """
    GetMenuItemCount(HMENU hMenu) -> int

    Returns the number of elements in the given menu.
    """
    return _guitest.GetMenuItemCount(*args)

def GetMenuItemIndex(*args):
    """
    GetMenuItemIndex(HMENU hm, char sitem) -> int

    First argument is a MenuId and the second is the (localized !) name of
    the menu including the hot key:'Rep&eat'.  

    Returns the index of the menu item (-1 if not found)
    """
    return _guitest.GetMenuItemIndex(*args)

def GetSystemMenu(*args):
    """GetSystemMenu(HWND hWnd, BOOL bRevert) -> HMENU"""
    return _guitest.GetSystemMenu(*args)

def GetMenuItemID(*args):
    """GetMenuItemID(HMENU hMenu, int nPos) -> UINT"""
    return _guitest.GetMenuItemID(*args)

def GetMenu(*args):
    """
    GetMenu(HWND hWnd) -> HMENU

    Using the corresponding library function (see MSDN) it returns a
    MenuID number
    """
    return _guitest.GetMenu(*args)

def SetWindowPos(*args):
    """
    SetWindowPos(HWND hWnd, HWND hWndInsertAfter, int X, int Y, int cx, 
        int cy, UINT uFlags) -> BOOL
    """
    return _guitest.SetWindowPos(*args)

def TabCtrl_SetCurFocus(*args):
    """TabCtrl_SetCurFocus(HWND hWnd, int item)"""
    return _guitest.TabCtrl_SetCurFocus(*args)

def TabCtrl_GetCurFocus(*args):
    """TabCtrl_GetCurFocus(HWND hWnd) -> int"""
    return _guitest.TabCtrl_GetCurFocus(*args)

def TabCtrl_SetCurSel(*args):
    """TabCtrl_SetCurSel(HWND hWnd, int item) -> int"""
    return _guitest.TabCtrl_SetCurSel(*args)

def TabCtrl_GetItemCount(*args):
    """TabCtrl_GetItemCount(HWND hWnd) -> int"""
    return _guitest.TabCtrl_GetItemCount(*args)

def SendRawKey(*args):
    """
    SendRawKey(UINT vk, DWORD flags)

    Wrapper around keybd_event. Allows sending low-level keys. The first
    argument is any of the VK_* constants. The second argument can be 0,
    KEYEVENTF_EXTENDEDKEY, KEYEVENTF_KEYUP or a combination of them.

        KEYEVENTF_EXTENDEDKEY - Means it is an extended key (i.e. to
        distinguish between arrow keys on the numeric keypad and
        elsewhere).

        KEYEVENTF_KEYUP - Means keyup. Unspecified means keydown.

       #Example use Win32::GuiTest qw/:FUNC :VK/;

       while 1:
           SendRawKey(VK_DOWN, KEYEVENTF_EXTENDEDKEY)
           SendKeys('{PAUSE 200}');

    """
    return _guitest.SendRawKey(*args)

def WindowFromPoint(*args):
    """WindowFromPoint(int x, int y) -> HWND"""
    return _guitest.WindowFromPoint(*args)

def AttachWin(*args):
    """AttachWin(HWND hwnd, BOOL fAttach) -> BOOL"""
    return _guitest.AttachWin(*args)
DIBSECT_H = _guitest.DIBSECT_H
class DibSect(_object):
    """Proxy of C++ DibSect class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DibSect, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DibSect, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ DibSect instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        """__init__(self) -> DibSect"""
        _swig_setattr(self, DibSect, 'this', _guitest.new_DibSect(*args))
        _swig_setattr(self, DibSect, 'thisown', 1)
    def __del__(self, destroy=_guitest.delete_DibSect):
        """__del__(self)"""
        try:
            if self.thisown: destroy(self)
        except: pass

    def Destroy(*args):
        """
        Destroy(self) -> bool

        Destroys the contents of the DIB section.
        """
        return _guitest.DibSect_Destroy(*args)

    def Load(*args):
        """Load(self, char szFile) -> bool"""
        return _guitest.DibSect_Load(*args)

    def SaveAs(*args):
        """
        SaveAs(self, char szFile) -> bool

        Save the current contents of the DIB section in a given file. With
        24-bit resolution it can grow quite big, so I immediately convert them
        to PNG (direct writing of PNG seemed to complicated to implement).

        """
        return _guitest.DibSect_SaveAs(*args)

    def Invert(*args):
        """
        Invert(self) -> bool

        Invert the colors in a current DIB section.
        """
        return _guitest.DibSect_Invert(*args)

    def ToGrayScale(*args):
        """
        ToGrayScale(self) -> bool

        Convert the DibSection to the gray scale. Note that it is still
        encoded as 24-bit BMP for simplicity.
        """
        return _guitest.DibSect_ToGrayScale(*args)

    def ToClipboard(*args):
        """
        ToClipboard(self) -> bool

        Copies the DibSect to clipboard (as an old-fashioned metafile), so
        that it can be further processed with your favourite image processing
        software, for example automatically using SendKeys.
        """
        return _guitest.DibSect_ToClipboard(*args)

    def CopyClient(*args):
        """
        CopyClient(self, HWND hwnd, int left, int top, int right, int bottom) -> bool

        Copy a client area of given window (or possibly its subset) into a
        given DibSect.  The rectangle may be optionally passed as a reference
        to 4-element array.  To get the right result make sure the window you
        want to copy is not obscured by others.

        """
        return _guitest.DibSect_CopyClient(*args)

    def CopyWindow(*args):
        """
        CopyWindow(self, HWND hwnd) -> bool

        Copy the window rectangle.
        """
        return _guitest.DibSect_CopyWindow(*args)


class DibSectPtr(DibSect):
    def __init__(self, this):
        _swig_setattr(self, DibSect, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, DibSect, 'thisown', 0)
        _swig_setattr(self, DibSect,self.__class__,DibSect)
_guitest.DibSect_swigregister(DibSectPtr)

def SelListViewItem(*args):
    """
    SelListViewItem(HWND hWnd, int iItem, BOOL bMulti=False) -> BOOL
    SelListViewItem(HWND hWnd, int iItem) -> BOOL

    Selects an item in the list view based off an index (zero-based).

    # Select first item, clears out any previous selections.
    SelListViewItem(win, 0)
    # Select an *additional* item.
    SelListViewItem(win, 1, 1)

    """
    return _guitest.SelListViewItem(*args)

def SelListViewItemText(*args):
    """
    SelListViewItemText(HWND hWnd, char lpItem, BOOL bMulti=False) -> BOOL
    SelListViewItemText(HWND hWnd, char lpItem) -> BOOL

    Selects an item in the list view based off text (case insensitive).

    # Select first item, clears out any previous selections.
    SelListViewItemText($win, 'Temp')
    # Select an *additional* item.
    SelListViewItemText($win, 'cabs', 1)

    """
    return _guitest.SelListViewItemText(*args)

import time
import re

def SendKeys(keys, delay=50):
    """Sends keystrokes to the active window as if typed at the
    keyboard using the optional delay between keystrokes (default is
    50 ms and should be OK for most uses).

    The keystrokes to send are specified in KEYS. There are several
    characters that have special meaning. This allows sending control
    codes and modifiers:

	- ~ means ENTER
	- + means SHIFT 
	- ^ means CTRL 
	- % means ALT

    The parens allow character grouping. You may group several
    characters, so that a specific keyboard modifier applies to all of
    them.  E.g. SendKeys('ABC') is equivalent to SendKeys('+(abc)').

    The curly braces are used to quote special characters (SendKeys('{+}{{}')
    sends a '+' and a '{'). You can also use them to specify certain
    named actions:

    ===========   ======================
	Name          Action
    ===========   ======================
	{BACKSPACE}   Backspace
	{BS}          Backspace
	{BKSP}        Backspace
	{BREAK}       Break
	{CAPS}        Caps Lock
	{DELETE}      Delete
	{DOWN}        Down arrow
	{END}         End
	{ENTER}       Enter (same as ~)
	{ESCAPE}      Escape
	{HELP}        Help key
	{HOME}        Home
	{INSERT}      Insert
	{LEFT}        Left arrow
	{NUMLOCK}     Num lock
	{PGDN}        Page down
	{PGUP}        Page up
	{PRTSCR}      Print screen
	{RIGHT}       Right arrow
	{SCROLL}      Scroll lock
	{TAB}         Tab
	{UP}          Up arrow
	{PAUSE}       Pause
    {F1}          Function Key 1
    ...           ...
    {F24}         Function Key 24
    {SPC}         Spacebar
    {SPACE}       Spacebar
    {SPACEBAR}    Spacebar
    {LWI}         Left Windows Key
    {RWI}         Right Windows Key 
    {APP}         Open Context Menu Key
    ===========   ======================

    All these named actions take an optional integer argument, like in
    {RIGHT 5}.  For all of them, except PAUSE, the argument means a
    repeat count. For PAUSE it means the number of milliseconds SendKeys
    should pause before proceding.

    In this implementation, SendKeys always returns after sending the
    keystrokes.  There is no way to tell if an application has processed
    those keys when the function returns. 
    """
    SendKeysImp(keys, delay)

def SendMouse(command):
    """This function emulates mouse input.  The `command` parameter is
    a string containing one or more of the following substrings:

    - {LEFTDOWN}    left button down
    - {LEFTUP}      left button up
    - {MIDDLEDOWN}  middle button down
	- {MIDDLEUP}    middle button up
	- {RIGHTDOWN}   right button down
	- {RIGHTUP}     right button up
	- {LEFTCLICK}   left button single click
	- {MIDDLECLICK} middle button single click
	- {RIGHTCLICK}  right button single click
	- {ABSx,y}      move to absolute coordinate ( x, y )
    - {RELx,y}      move to relative coordinate ( x, y )

    Note: Absolute mouse coordinates range from 0 to 65535.  Relative
    coordinates can be positive or negative.  If you need pixel
    coordinates you can use MouseMoveAbsPix.

    Also equivalent low-level functions are available:

    - SendLButtonUp()
    - SendLButtonDown()
    - SendMButtonUp()
    - SendMButtonDown()
    - SendRButtonUp()
    - SendRButtonDown()
    - SendMouseMoveRel(x,y)
    - SendMouseMoveAbs(x,y)
    """
    p = re.compile(r'\{(.+?)\}')
    mouse_abs = re.compile(r'abs(-?\d+),\s*(-?\d+)')
    mouse_rel = re.compile(r'rel(-?\d+),\s*(-?\d+)')
    cmds = p.findall(command)
    cmd_map = {'leftdown': SendLButtonDown,
               'leftup': SendLButtonUp,
               'middledown': SendMButtonDown,
               'middleup': SendMButtonUp,
               'rightdown': SendRButtonDown,
               'rightup': SendRButtonUp,
               }               
    for cmd in cmds:
        c = cmd.lower()
        if c in cmd_map:
            cmd_map[c]()
        elif c == 'leftclick':
            SendLButtonDown()
            SendLButtonUp()
        elif c == 'rightclick':
            SendRButtonDown()
            SendRButtonUp()
        elif c == 'middleclick':
            SendMButtonDown()
            SendMButtonUp()
        elif c.startswith('abs'):
            s = mouse_abs.search(c)
            if s:
                SendMouseMoveAbs(int(s.group(1)), int(s.group(2)))
            else:
                print "Unmatched mouse command!"
        elif c.startswith('rel'):            
            s = mouse_rel.search(c)
            if s:
                SendMouseMoveRel(int(s.group(1)), int(s.group(2)))
            else:
                print "Unmatched mouse command!"
        else:
            print "Unmatched mouse command!"
            
def FindWindowLike(titlere, classre='', childid=None, maxlevel=None,
                   window=None):
    """Finds the window handles of the windows matching the specified
    parameters and returns them as a list.  The search strings may all
    be passed as regular expressions.

    You may specify the handle of the window to search under. The
    routine searches through all of this windows children and their
    children recursively.  If 'undef' then the routine searches
    through all windows. There is also a regexp used to match against
    the text in the window caption and another regexp used to match
    against the text in the window class. If you pass a child ID
    number, the functions will only match windows with this id.

    """
    if not window:
        window = GetDesktopWindow()
    
    if titlere:
        tre = re.compile(titlere)
    if classre:
        cre = re.compile(classre)
    ret = []
    
    for w in GetChildWindows(window):
        if maxlevel is not None and GetChildDepth(window, w) > maxlevel:
            continue
        wtxt = GetWindowText(w)
        cname = GetClassName(w)
        cid = None
        if GetParent(w) != 0:
            cid = GetWindowLong(w, GWL_ID)

        if titlere and (not wtxt or not tre.search(wtxt)):
            continue
        if classre and not cre.search(cname):
            continue
        if childid is not None and childid != cid:
            continue
        ret.append(w)
    return ret

def GetWindowID(window):
    """Returns the control Id of the specified window.
    """
    return GetWindowLong(window, GWL_ID)

def PushButton(button, delay):
    """Equivalent to
       PushChildButton(GetForegroundWindow(), button, delay)
    """
    return PushChildButton(GetForegroundWindow(), button, delay)

def MatchTitleOrId(window, regex):
    title = GetWindowText(window)
    id = GetWindowID(window)
    if title:
        tr = re.compile(regex, re.I)
        return tr.search(title) is not None
    else:
        return regex == id

def PushChildButton(parent, button, delay=0):
    """Allows generating a mouse click on a particular button.

    parent - the parent window of the button

    button - either the text in a button (e.g.'Yes') or the control ID
    of a button.

    delay - the time (0.25 means 250 ms) to wait between the mouse
    down and the mouse up event. This is useful for debugging.
    """
    for child in GetChildWindows(parent):
        # Is correct text or correct window ID?
        if MatchTitleOrId(child, button) and IsWindowEnabled(child):
	    # Need to use PostMessage.  SendMessage won't return when
	    # certain dialogs come up.
	    PostMessage(child, WM_LBUTTONDOWN, 0, 0);
	    # Allow for user to see that button is being pressed by
	    # waiting some ms.
            if delay:
                time.sleep(delay)
            PostMessage(child, WM_LBUTTONUP, 0, 0)
	    return 1
    return 0

def WaitWindowLike(parent, titlere, classre, wid, depth, wait=10):
    """Function which allows one to wait for a window to appear
    vs. using hard waits (e.g. sleep 2).

    parent   - Where to start (parent window)

    titlere - Regexp for the window title

    classre - Regexp for the window class name

    wid    - Numeric Window or Control ID
    
    depth    - How deep should we search before we stop
    
    wait     - How many seconds should we wait before giving up

    """
    wins = []
    t = 0
    while t < wait:
        wins = FindWindowLike(titlere, classre, wid, depth, window=parent)
        if wins and IsWindow(wins[0]):
            return wins
        time.sleep(0.5)
        t += 0.5
    return wins

def WaitWindow(titlere, wait=10):
    """Minimal version of WaitWindowLike. Only requires the window
    title regexp. You can also specify the wait timeout in seconds.

    titlere - Regexp for the window title

    wait     - How many seconds should we wait before giving up
    """
    return WaitWindowLike(0, titlere, "", None, None, wait)

def IsWindowStyle(window, style):
    """Determines if a window has the specified style.  See sample
    script for more details.
    """
    return GetWindowLong(window, GWL_STYLE)&style

def IsWindowStyleEx(window, exstyle):
    """Determines if a window has the specified extended style.
    """
    return GetWindowLong(window, GWL_EXSTYLE)&exstyle

def SelectTabItem(window, item, parent=None):
    """Select tab item of window given item number and parent.
    """
    if not parent:
        parent = GetForegroundWindow()
    for child in GetChildWindows(parent):
        if MatchTitleOrId(child, window):
            PostMessage(child, TCM_SETCURFOCUS, item, 0)
            # Success.
            return 1
    return 0

def FindAndCheck(window, parent=None):
    """Find the check button item specified as either a window id
    (HWND) or window title and then check it.
    """
    if not parent:
        parent = GetForegroundWindow()
    for child in GetChildWindows(parent):
        ctxt = GetWindowText(child)
        cid = GetWindowID(child)
        if MatchTitleOrId(child, window):
            CheckButton(child)
            break

def MenuSelect(item, window=None, menu=None):
    """Allows selecting a menu programmatically.

    Simple Examples:
    # Exit foreground application through application menu.
    MenuSelect('&File|E&xit')

    # Exit foreground application through system menu
    MenuSelect('&Close', 0, GetSystemMenu(GetForegroundWindow(), False))
    """
    if not window:
        window = GetForegroundWindow()
    if not menu:
        menu = GetMenu(window)
    return MenuSelectItem(window, menu, item)

def MenuSelectItem(window, menu, items):
    """Parameters: window (Window Handle), menu (Parent/Root Menu),
    items (Menu Item Path).
    
    Returns: False on failure, True on success
    """
    mi = -1
    curr = menu
    menus = items.split('|')
    for m in menus:
        # Look for menu item in current menu level.
        mi = GetMenuItemIndex(curr, m)
        if mi == -1:
            return 0
        next = GetSubMenu(curr, mi)
        if not next:
            break
        curr = next
    if curr != GetSystemMenu(window, 0):
        PostMessage(window, WM_COMMAND, GetMenuItemID(curr, mi), 0)
    else:
        PostMessage(window, WM_SYSCOMMAND, GetMenuItemID(curr, mi), 0)
    return 1


def MouseClick(window, parent=None, x_off=0, y_off=0, button='{LEFT}',
               delay=0):
    """Allows one to easily interact with an application through mouse
    emulation.

    window - Regexp for a Window caption / Child caption, or just a
    Child ID.

    parent - Handle to parent window.  Default is foreground window.
    Use GetDesktopWindow() return value for this if clicking on an
    application title bar.

    x_off - Offset for X axis.  Default is 0.

    y_off - Offset for Y axis.  Default is 0.

    button - {LEFT}, {MIDDLE}, {RIGHT}.  Default is {LEFT}

    delay - Default is 0.  0.50 = 500 ms.  Delay between button down
    and button up.

    Simple Examples:

    # Click on CE button if its parent window is in foreground.
    MouseClick('^CE$')

    # Right click on CE button if its parent window is in foreground
    MouseClick('^CE$', button='{RIGHT}')

    # Click on 8 button window under the specified parent window; where
    # [PARENTHWND] will be replaced by a parent handle variable.
    MouseClick('8', [PARENTHWND]);

    # Click on Calculator parent window itself
    MouseClick('Calculator', GetDesktopWindow());

    """    
    p = re.compile(r'^\{\D+\}$')
    assert p.match(button) is not None
    # Remove the trailing brace.
    button = button[:-1]
    if not parent:
        parent = GetForegroundWindow()
        
    for child in GetChildWindows(parent):
        if MatchTitleOrId(child, window):
            x, y, w, h = GetWindowRect(child)
            MouseMoveAbsPix(x+1 + x_off, y+1 + y_off)
            SendMouse(button + 'DOWN}')
            time.sleep(delay)
            SendMouse(button + 'UP}')
            return 1
    return 0            
    
        


