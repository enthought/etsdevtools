// ======================================================================
// SWIG code for guitest under Win32.
//
// Copyright (c) 2005  Prabhu Ramachandran, All rights reserved.
// Email: prabhu_r@users.sf.net
// ======================================================================

%module guitest

%{
#include <windows.h>
#include <commctrl.h>
#include "GUITest.cpp"
#include "dibsect.h"
#include "dibsect.cpp"
%}

%include "typemaps.i"
%include "std_vector.i"
%include "std_string.i"

%feature("autodoc", "1");

// ----------------------------------------
// Various typedefs and defines.

typedef int BOOL;
typedef unsigned long DWORD;
typedef unsigned int UINT;

#if defined(_WIN64)
 typedef unsigned __int64 UINT_PTR;
#else
 typedef unsigned int UINT_PTR;
#endif
#if defined(_WIN64)
 typedef __int64 LONG_PTR; 
#else
 typedef long LONG_PTR;
#endif
typedef LONG_PTR LPARAM;
typedef UINT_PTR WPARAM;

// ----------------------------------------
// CONSTANTS
#define SW_HIDE 0
#define SW_NORMAL 1
#define SW_SHOWNORMAL 1
#define SW_SHOWMINIMIZED 2
#define SW_MAXIMIZE 3
#define SW_SHOWMAXIMIZED 3
#define SW_SHOWNOACTIVATE 4
#define SW_SHOW 5
#define SW_MINIMIZE 6
#define SW_SHOWMINNOACTIVE 7
#define SW_SHOWNA 8
#define SW_RESTORE 9
#define SW_SHOWDEFAULT 10
#define SW_FORCEMINIMIZE 11
#define SW_MAX 11

#define LVS_ICON       0
#define LVS_REPORT     1
#define LVS_SMALLICON  2
#define LVS_LIST       3
#define LVS_TYPEMASK   3
#define LVS_SINGLESEL  4
#define LVS_SHOWSELALWAYS      8
#define LVS_SORTASCENDING      16
#define LVS_SORTDESCENDING     32
#define LVS_SHAREIMAGELISTS    64
#define LVS_NOLABELWRAP        128
#define LVS_AUTOARRANGE        256
#define LVS_EDITLABELS 512
#define LVS_NOSCROLL   0x2000
#define LVS_TYPESTYLEMASK      0xfc00
#define LVS_ALIGNTOP   0
#define LVS_ALIGNLEFT  0x800
#define LVS_ALIGNMASK  0xc00
#define LVS_OWNERDRAWFIXED     0x400
#define LVS_NOCOLUMNHEADER     0x4000
#define LVS_NOSORTHEADER       0x8000

#define VK_LBUTTON     1
#define VK_RBUTTON     2
#define VK_CANCEL      3
#define VK_MBUTTON     4
#define VK_BACK        8
#define VK_TAB 9
#define VK_CLEAR       12
#define VK_RETURN      13
#define VK_SHIFT       16
#define VK_CONTROL     17
#define VK_MENU        18
#define VK_PAUSE       19
#define VK_CAPITAL     20
#define VK_KANA        0x15
#define VK_HANGEUL     0x15
#define VK_HANGUL      0x15
#define VK_JUNJA       0x17
#define VK_FINAL       0x18
#define VK_HANJA       0x19
#define VK_KANJI       0x19
#define VK_ESCAPE      0x1B
#define VK_CONVERT     0x1C
#define VK_NONCONVERT  0x1D
#define VK_ACCEPT      0x1E
#define VK_MODECHANGE  0x1F
#define VK_SPACE       32
#define VK_PRIOR       33
#define VK_NEXT        34
#define VK_END 35
#define VK_HOME        36
#define VK_LEFT        37
#define VK_UP  38
#define VK_RIGHT       39
#define VK_DOWN        40
#define VK_SELECT      41
#define VK_PRINT       42
#define VK_EXECUTE     43
#define VK_SNAPSHOT    44
#define VK_INSERT      45
#define VK_DELETE      46
#define VK_HELP        47
#define VK_LWIN        0x5B
#define VK_RWIN        0x5C
#define VK_APPS        0x5D
#define VK_SLEEP       0x5F
#define VK_NUMPAD0     0x60
#define VK_NUMPAD1     0x61
#define VK_NUMPAD2     0x62
#define VK_NUMPAD3     0x63
#define VK_NUMPAD4     0x64
#define VK_NUMPAD5     0x65
#define VK_NUMPAD6     0x66
#define VK_NUMPAD7     0x67
#define VK_NUMPAD8     0x68
#define VK_NUMPAD9     0x69
#define VK_MULTIPLY    0x6A
#define VK_ADD 0x6B
#define VK_SEPARATOR   0x6C
#define VK_SUBTRACT    0x6D
#define VK_DECIMAL     0x6E
#define VK_DIVIDE      0x6F
#define VK_F1  0x70
#define VK_F2  0x71
#define VK_F3  0x72
#define VK_F4  0x73
#define VK_F5  0x74
#define VK_F6  0x75
#define VK_F7  0x76
#define VK_F8  0x77
#define VK_F9  0x78
#define VK_F10 0x79
#define VK_F11 0x7A
#define VK_F12 0x7B
#define VK_F13 0x7C
#define VK_F14 0x7D
#define VK_F15 0x7E
#define VK_F16 0x7F
#define VK_F17 0x80
#define VK_F18 0x81
#define VK_F19 0x82
#define VK_F20 0x83
#define VK_F21 0x84
#define VK_F22 0x85
#define VK_F23 0x86
#define VK_F24 0x87
#define VK_NUMLOCK     0x90
#define VK_SCROLL      0x91
#define VK_LSHIFT      0xA0
#define VK_RSHIFT      0xA1
#define VK_LCONTROL    0xA2
#define VK_RCONTROL    0xA3
#define VK_LMENU       0xA4
#define VK_RMENU       0xA5
#define VK_PROCESSKEY  0xE5
#define VK_ATTN        0xF6
#define VK_CRSEL       0xF7
#define VK_EXSEL       0xF8
#define VK_EREOF       0xF9
#define VK_PLAY        0xFA
#define VK_ZOOM        0xFB
#define VK_NONAME      0xFC
#define VK_PA1 0xFD
#define VK_OEM_CLEAR   0xFE
#define KEYEVENTF_EXTENDEDKEY 0x00000001
#define KEYEVENTF_KEYUP 00000002

#define GWL_ID (-12)
#define GWL_STYLE (-16)
#define GWL_EXSTYLE (-20)

#define WM_MOUSEACTIVATE 33
#define WM_MOUSEMOVE 512
#define WM_LBUTTONDOWN 513
#define WM_LBUTTONUP 514
#define WM_LBUTTONDBLCLK 515
#define WM_RBUTTONDOWN 516
#define WM_RBUTTONUP 517
#define WM_RBUTTONDBLCLK 518
#define WM_MBUTTONDOWN 519
#define WM_MBUTTONUP 520
#define WM_MBUTTONDBLCLK 521
#define WM_MOUSEWHEEL 522
#define WM_MOUSEFIRST 512

#define WM_COMMAND 273
#define WM_SYSCOMMAND 274


#define TCM_FIRST      0x1300
#define TCM_SETCURFOCUS        (TCM_FIRST+48)

// ----------------------------------------
// TYPEMAPS and other SWIG code.

// The next two typemaps handle HWND in and out of functions.
%typemap(in) HWND
{
    $1 = ($1_ltype) PyLong_AsLong($input);
    if (PyErr_Occurred()) SWIG_fail;
}

%typemap(out) HWND
{
    $result = PyLong_FromLong((long)$1);
    if (PyErr_Occurred()) SWIG_fail;
}

// Apply this typemap for HMENU also.
%apply HWND { HMENU };

// Type map to handle HWND* return values with an int *nelem as an
// argument.  This happens for:
//     HWND* GetChildWindows(HWND hWnd, int *nelem);

%typemap(in,numinputs=0) (int *nelem) (int temp) {
        $1 = &temp;
}

%typemap(out) HWND* {
        $result = PyList_New(*arg2);
        for (int i=0; i< *arg2; ++i)
                PyList_SetItem($result, i, PyLong_FromLong(long($1[i])));
        free($1);
}


// Wrap a vector of strings.
%template(VectorString) std::vector<std::string>;

// Renaming some wrapper functions.
%rename(SetFocus) MySetFocus;
%rename(SetActiveWindow) MySetActiveWindow;
%rename(ShowWindow) MyShowWindow;

// ----------------------------------------
// DOCUMENTATION.
%feature("docstring") GetListViewContents
"Returns a list of the contents of the specified list view.";

%feature("docstring") MouseMoveAbsPix
"Move the mouse cursor to the screen pixel indicated as parameter.
  # Moves to x=200, y=100 in pixel coordinates.
  MouseMoveAbsPix(200, 100);";

%feature("docstring") MouseMoveWheel
"Positive or negative value to direct mouse wheel movement.";

%feature("docstring") GetMenu
"Using the corresponding library function (see MSDN) it returns a
MenuID number";

%feature("docstring") GetMenuItemIndex

"First argument is a MenuId and the second is the (localized !) name of
the menu including the hot key:'Rep&eat'.  

Returns the index of the menu item (-1 if not found)";

%feature("docstring") GetMenuItemCount
"Returns the number of elements in the given menu.";

%feature("docstring") MenuSelect
"Allows selecting a menu programmatically.

Simple Examples:
    # Exit foreground application through application menu.
    MenuSelect('&File|E&xit')

    # Exit foreground application through system menu
    MenuSelect('&Close', 0, GetSystemMenu(GetForegroundWindow(), FALSE));
";

%feature("docstring") GetMenuItemInfo
"Receives a menu handler (one we got from GetMenu or GetSubMenu) and a
number (which is the location of the item within the given menu).

Returns a hash of which there are currently 2 keys: type can be either
'string' or 'separator' - this is the type of the menu item text is
the visible text of the menu item (provided only for 'string' type)

WARNING: This is an experimental function. Its behavior might change.
";

%feature("docstring") WMGetText
"Sends a WM_GETTEXT to a window and returns its contents";

%feature("docstring") WMSetText
"Sends a WM_SETTEXT to a window setting its contents";

%feature("docstring") GetCursorPos
"Retrieves the cursor's position,in screen coordinates as (x,y) array.";

%feature("docstring") GetCaretPos
"Retrieves the caret's position, in client coordinates as (x,y)
array. (Like Windows function)";

%feature("docstring") MySetFocus
"Sets the keyboard focus to the specified window";

%feature("docstring") GetDesktopWindow
"Returns a handle to the desktop window";

%feature("docstring") GetWindowText
"Get the text name of the window as shown on the top of it.  Beware,
this is text depends on localization.
";

%feature("docstring") GetClassName
"Using the same Windows library function returns the name of the class
wo which the specified window belongs.

See MSDN for more details.

You can also check out MSDN to see an overview of the Window Classes.";

%feature("docstring") GetParent
"A library function (see MSDN) to return the WindowID of the parent window.
See MSDN for the special cases.";

%feature("docstring") SetForegroundWindow
"See corresponding Windows functions.";

%feature("docstring") GetChildWindows
"Using EnumChildWindows library function (see MSDN) it returns the
WindowID of each child window. If the children have their own children
the function returns them too until the tree ends.
";

%feature("docstring") GetTopLevelWindows
"Using EnumWindows library function (see MSDN) it returns the WindowID
of all the top-level window.";

%feature("docstring") IsChild
"Using the corresponding library function (see MSDN) it returns true if
the second window is an immediate child or a descendant window of the
first window.
";

%feature("docstring") GetChildDepth
"Using the GetParent library function in a loop, returns the distance
between an ancestor window and a child (descendant) window.

Features/bugs:

If the given 'ancsetor' is not really an ancestor, the return value is
the distance of child from the root window (0). If you supply the same
id for both the ancestor and the child you get 1.  If the ancestor you
are checking is not 0 then the distance given is 1 larger than it
should be.
";

%feature("docstring") SendMessage
"This is a library function (see MSDN) used by a number of the
functions provided by Win32::GuiTest. It sends the specified message
to a window or windows.  HWnd is the WindowID or HWND_BROADCAST to
send message to all top level windows.  Message is not sent to child
windows. (If I understand this correctly this means it is sent to all
the immediate children of the root window (0).  Msg the message wParam
additional parameter lParam additioanl parameter

It is most likely you won't use this directly but through one of the
other functions .
";

%feature("docstring") PostMessage
"See corresponding Windows library function in MSDN.";

%feature("docstring") CheckButton
"The names say it.  Works on radio buttons and checkboxes.  For regular
buttons, use IsWindowEnabled.";

%feature("docstring") UnCheckButton
"The names say it.  Works on radio buttons and checkboxes.  For regular
buttons, use IsWindowEnabled.";

%feature("docstring") GrayOutButton
"The names say it.  Works on radio buttons and checkboxes.  For regular
buttons, use IsWindowEnabled.";

%feature("docstring") IsCheckedButton
"The names say it.  Works on radio buttons and checkboxes.  For regular
buttons, use IsWindowEnabled.";

%feature("docstring") IsGrayedButton
"The names say it.  Works on radio buttons and checkboxes.  For regular
buttons, use IsWindowEnabled.";

%feature("docstring") ScreenToNorm
"Returns normalised coordinates of given point (0-FFFF as a fraction of
screen resolution)
";

%feature("docstring") NormToScreen
"The opposite transformation to ScreenToNorm";

%feature("docstring") GetScreenRes
"Returns screen resolution.";

%feature("docstring") SelComboItem
"Selects an item in the combo box based off an index (zero-based).";

%feature("docstring") SelComboItemText
"Selects an item in the combo box based off text (case insensitive).";

%feature("docstring") GetListContents
"Fetch the contents of the list and combo boxes.";

%feature("docstring") IsKeyPressed
"Wrapper around the GetAsyncKeyState API function. Returns TRUE if the
user presses the specified key.

    IsKeyPressed('ESC')
    IsKeyPressed('A')
    IsKeyPressed('DOWN')
";

%feature("docstring") SendRawKey
"Wrapper around keybd_event. Allows sending low-level keys. The first
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
";

%feature("docstring") GetListViewContents
"Returns a list of the contents of the specified list view.";

%feature("docstring") SelListViewItem
"Selects an item in the list view based off an index (zero-based).

# Select first item, clears out any previous selections.
SelListViewItem(win, 0)
# Select an *additional* item.
SelListViewItem(win, 1, 1)
";

%feature("docstring") SelListViewItemText
"Selects an item in the list view based off text (case insensitive).

# Select first item, clears out any previous selections.
SelListViewItemText($win, 'Temp')
# Select an *additional* item.
SelListViewItemText($win, 'cabs', 1)
";

%feature("docstring") IsListViewItemSel
"Determines if the specified list view item is selected.
";

%feature("docstring") GetTabItems
"Returns a list of a tab control's labels.";

%feature("docstring") SelTabItem
"Selects a tab based off an index (zero-based).";

%feature("docstring") SelTabItemText
"Selects a tab based off text label (case insensitive).";

%feature("docstring") IsTabItemSel
"Determines if the specified tab item is selected.";

%feature("docstring") SelTreeViewItemPath
"Selects a tree view item based off a 'path' (case insensitive).

    # Select Machine item and Processors sub-item.
    SelTreeViewItemPath(window, 'Machine|Processors')

    SelTreeViewItemPath(window, 'Item')
";

%feature("docstring") GetTreeViewSelPath
"Returns a string containing the path (i.e., 'parent|child') of the
currently selected tree view item.

   oldpath = GetTreeViewSelPath(window)
   SelTreeViewItemPath(window, 'Parent|Child')
   SelTreeViewItemPath(window, oldpath);
";

%feature("docstring") DibSect::CopyClient
"Copy a client area of given window (or possibly its subset) into a
given DibSect.  The rectangle may be optionally passed as a reference
to 4-element array.  To get the right result make sure the window you
want to copy is not obscured by others.
";

%feature("docstring") DibSect::CopyWindow
"Copy the window rectangle.";

%feature("docstring") DibSect::SaveAs
"Save the current contents of the DIB section in a given file. With
24-bit resolution it can grow quite big, so I immediately convert them
to PNG (direct writing of PNG seemed to complicated to implement).
";

%feature("docstring") DibSect::Invert
"Invert the colors in a current DIB section.";

%feature("docstring") DibSect::ToGrayScale
"Convert the DibSection to the gray scale. Note that it is still
encoded as 24-bit BMP for simplicity.";

%feature("docstring") DibSect::ToClipboard
"Copies the DibSect to clipboard (as an old-fashioned metafile), so
that it can be further processed with your favourite image processing
software, for example automatically using SendKeys.";

%feature("docstring") DibSect::Destroy
"Destroys the contents of the DIB section.";



// ----------------------------------------
// Functions to wrap.

std::vector<std::string> GetListViewContents(HWND hWnd);

BOOL SelListViewItem(HWND hWnd, int iItem, BOOL bMulti=FALSE);

BOOL SelListViewItemText(HWND hWnd, char* lpItem, BOOL bMulti=FALSE);

BOOL IsListViewItemSel(HWND hWnd, char* lpItem);

std::vector<std::string> GetTabItems(HWND hWnd);

BOOL SelTabItem(HWND hWnd, int iItem);

BOOL SelTabItemText(HWND hWnd, char* lpItem);

BOOL IsTabItemSel(HWND hWnd, char* lpItem);

BOOL SelTreeViewItemPath(HWND hWnd, char* lpPath);

char* GetTreeViewSelPath(HWND hWnd);

%apply int *OUTPUT { int *out_x, int *out_y };

void GetCursorPos(int *out_x, int *out_y);

void SendLButtonUp();

void SendLButtonDown();

void SendMButtonUp();

void SendMButtonDown();

void SendRButtonUp();

void SendRButtonDown();

void SendMouseMoveRel(int x, int y);

void SendMouseMoveAbs(int x, int y);

void MouseMoveAbsPix(int x, int y);


void MouseMoveWheel(DWORD dwChange);

void SendKeysImp(char* s, DWORD wait);

HWND GetDesktopWindow();

HWND GetWindow(HWND hwnd, UINT uCmd);

char* GetWindowText(HWND hwnd);

char* GetClassName(HWND hwnd);

HWND GetParent(HWND hwnd);

long GetWindowLong(HWND hwnd, int index);
    
BOOL SetForegroundWindow(HWND hWnd);

HWND MySetFocus(HWND hWnd);

HWND* GetChildWindows(HWND hWnd, int *nelem);

%typemap(out) HWND* {
        $result = PyList_New(*arg1);
        for (int i=0; i< *arg1; ++i)
                PyList_SetItem($result, i, PyLong_FromLong(long($1[i])));
        free($1);
}

HWND* GetTopLevelWindows(int *nelem);

char* WMGetText(HWND hwnd);

int WMSetText(HWND hwnd, char* text);

BOOL IsChild(HWND hWndParent, HWND hWnd);

DWORD GetChildDepth(HWND hAncestor, HWND hChild);

int SendMessage(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam);
  
int PostMessage(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam);

void CheckButton(HWND hwnd);

void UnCheckButton(HWND hwnd);

void GrayOutButton(HWND hwnd);

BOOL IsCheckedButton(HWND hwnd);

BOOL IsGrayedButton(HWND hwnd);

BOOL IsWindow(HWND hwnd);

void ScreenToClient(HWND hwnd, int x, int y, int *out_x, int *out_y);

void ClientToScreen(HWND hwnd, int x, int y, int* out_x, int* out_y);

void GetCaretPos(HWND hwnd, int* out_x, int* out_y);

HWND GetFocus(HWND hwnd);

HWND GetActiveWindow(HWND hwnd);


HWND GetForegroundWindow();

HWND MySetActiveWindow(HWND hwnd);

BOOL EnableWindow(HWND hwnd, BOOL fEnable);

BOOL IsWindowEnabled(HWND hwnd);

BOOL IsWindowVisible(HWND hwnd);

BOOL MyShowWindow(HWND hwnd, int nCmdShow);
    
void ScreenToNorm(int x, int y, int* out_x, int* out_y);

void NormToScreen(int x, int y, int* out_x, int* out_y);

void GetScreenRes(int* out_x, int* out_y);

%apply int *OUTPUT { int* left, int* top, int* right, int* bottom };
void GetWindowRect(HWND hWnd, int* left, int* top, int* right, int* bottom);

char* GetComboText(HWND hwnd, int index);

char* GetListText(HWND hwnd, int index);

std::vector<std::string> GetComboContents(HWND hWnd);

BOOL SelComboItem(HWND hWnd, int iItem);

BOOL SelComboItemText(HWND hWnd, char* lpItem);
	
std::vector<std::string> GetListContents(HWND hWnd);

BOOL IsKeyPressed(char* name);

HMENU GetSubMenu(HMENU hMenu, int nPos);

std::vector<std::string> GetMenuItemInfo(HMENU hMenu, UINT uItem);

int GetMenuItemCount(HMENU hMenu);
    
int GetMenuItemIndex(HMENU hm, char* sitem);

HMENU GetSystemMenu(HWND hWnd, BOOL bRevert);

UINT GetMenuItemID(HMENU hMenu, int nPos);
 
HMENU GetMenu(HWND hWnd);
 
BOOL SetWindowPos(HWND hWnd, HWND hWndInsertAfter, int X, int Y, int cx, 
                  int cy, UINT uFlags);

void TabCtrl_SetCurFocus(HWND hWnd, int item);

int TabCtrl_GetCurFocus(HWND hWnd);

int TabCtrl_SetCurSel(HWND hWnd, int item);

int TabCtrl_GetItemCount(HWND hWnd);

void SendRawKey(UINT vk, DWORD flags);

HWND WindowFromPoint(int x, int y);

BOOL AttachWin(HWND hwnd, BOOL fAttach);

// --------------------------------------------------
// Dibsect
%ignore BITMAPINFOHEADER;
%include "dibsect.h"


// --------------------------------------------------
// This stuff is injected into the proxy file.
%pythoncode
%{
import time
import re

def SendKeys(keys, delay=50):
    """Sends keystrokes to the active window as if typed at the
    keyboard using the optional delay between keystrokes (default is
    50 ms and should be OK for most uses).

    The keystrokes to send are specified in KEYS. There are several
    characters that have special meaning. This allows sending control
    codes and modifiers:

	~ means ENTER
	+ means SHIFT 
	^ means CTRL 
	% means ALT

    The parens allow character grouping. You may group several
    characters, so that a specific keyboard modifier applies to all of
    them.  E.g. SendKeys('ABC') is equivalent to SendKeys('+(abc)').

    The curly braces are used to quote special characters (SendKeys('{+}{{}')
    sends a '+' and a '{'). You can also use them to specify certain
    named actions:

	Name          Action

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

        {LEFTDOWN}    left button down
        {LEFTUP}      left button up
        {MIDDLEDOWN}  middle button down
	{MIDDLEUP}    middle button up
	{RIGHTDOWN}   right button down
	{RIGHTUP}     right button up
	{LEFTCLICK}   left button single click
	{MIDDLECLICK} middle button single click
	{RIGHTCLICK}  right button single click
	{ABSx,y}      move to absolute coordinate ( x, y )
        {RELx,y}      move to relative coordinate ( x, y )

    Note: Absolute mouse coordinates range from 0 to 65535.  Relative
    coordinates can be positive or negative.  If you need pixel
    coordinates you can use MouseMoveAbsPix.

    Also equivalent low-level functions are available:

        SendLButtonUp()
        SendLButtonDown()
        SendMButtonUp()
        SendMButtonDown()
        SendRButtonUp()
        SendRButtonDown()
        SendMouseMoveRel(x,y)
        SendMouseMoveAbs(x,y)
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
    
        
%}
