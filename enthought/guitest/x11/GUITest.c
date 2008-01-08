/* X11::GUITest ($Id: GUITest.xs,v 1.40 2004/01/16 23:41:42 ctrondlp Exp $)
 *  
 * Copyright (c) 2003-2004  Dennis K. Paulsen, All Rights Reserved.
 * Email: ctrondlp@users.sourceforge.net
 *
 * Copyright (c) 2005 Prabhu Ramachandran, All Rights Reserved.
 * Email: prabhu_r@users.sf.net
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of
 * the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 *
 */

/* Modified by Prabhu Ramachandran so this works with SWIG and
   therefore may be used from Python and various other languages.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <assert.h>
#include <ctype.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Intrinsic.h>
#include <X11/StringDefs.h>
#include <X11/keysym.h>
#include <X11/extensions/XTest.h>
#include "GUITest.h"

/* File Level Variables */
static Display *TheXDisplay = NULL;
static int TheScreen = 0;
static WindowTable ChildWindows = {0};
static ULONG EventSendDelay = DEF_EVENT_SEND_DELAY;
static ULONG KeySendDelay = DEF_KEY_SEND_DELAY;


/* Non Exported Utility Functions: */

/* Function: IgnoreBadWindow
 * Description: User defined error handler callback for X event errors.
 */
static int IgnoreBadWindow(Display *display, XErrorEvent *error)
{
	/* Ignore bad window errors here, handle elsewhere */
	if (error->request_code != BadWindow) {
		XSetErrorHandler(NULL);
	}
	/* Note: Return is ignored */
	return(0);
}

/* Function: SetupXDisplay
 * Description: Sets up our connection to the X server's display
 */
static void SetupXDisplay(void)
{
	int eventnum = 0, errornum = 0,
		majornum = 0, minornum = 0;

	/* Get Display Pointer */
	TheXDisplay = XOpenDisplay(NULL);
	if (TheXDisplay == NULL) {
		printf("X11::GUITest - This program is designed to run in X Windows!\n");
	}

	/* Ensure the XTest extension is available */
	if (!XTestQueryExtension(TheXDisplay, &eventnum, &errornum, 
							 &majornum, &minornum)) {
		printf("X11::GUITest - XServer %s doesn't support the XTest extensions!\n",
			  DisplayString(TheXDisplay));
	}

	TheScreen = DefaultScreen(TheXDisplay);

	/* Discard current events in queue. */	
	XSync(TheXDisplay, True);
}

/* Function: CloseXDisplay
 * Description: Closes our connection to the X server's display
 */
static void CloseXDisplay(void)
{
	if (TheXDisplay) {
		XFlush(TheXDisplay);
		XCloseDisplay(TheXDisplay);
		TheXDisplay = NULL;
	}
}

/* Function: IsNumber
 * Description: Determines if the specified string represents a
 *              number.
 */
static BOOL IsNumber(const char *str)
{
	unsigned int i = 0;

	assert(str != NULL);

	for (i = 0; i < strlen(str); i++) {
		if (!isdigit(str[i])) {
			return(FALSE);
		}
	}
	return(TRUE);
}

/* Function: GetKeySym
 * Description: Given a regular(i.e., a) or special(i.e., Tab) key name,
 *              this function obtains the appropriate keysym by first
 *              checking the XStringToKeysym (case sensitive) library
 *        		function.  If the key is not recognized by that function,
 *				an internal table to this function is utilized for the
 *				lookup (case insensitive).
 * Note: Returns TRUE (non-zero) on success, FALSE (zero) on failure.  Also,
 *       on success, sym gets set to the appropriate keysym. On failure, sym
 * 		 gets set to NoSymbol.
 */
static BOOL GetKeySym(const char *name, KeySym *sym)
{
	static const KeyNameSymTable kns_table[] = { /* {Name, Sym}, */
		{"BAC", XK_BackSpace},		{"BS", XK_BackSpace},		{"BKS", XK_BackSpace},
 		{"BRE", XK_Break},			{"CAN", XK_Cancel}, 		{"CAP", XK_Caps_Lock},
		{"DEL", XK_Delete},			{"DOW", XK_Down},			{"END", XK_End},
		{"ENT", XK_Return},			{"ESC", XK_Escape},			{"HEL", XK_Help},
		{"HOM", XK_Home},			{"INS", XK_Insert},			{"LEF", XK_Left},
		{"NUM", XK_Num_Lock},		{"PGD", XK_Next},			{"PGU", XK_Prior},
		{"PRT", XK_Print},			{"RIG", XK_Right},			{"SCR", XK_Scroll_Lock},
		{"TAB", XK_Tab},			{"UP", XK_Up},				{"F1", XK_F1},
		{"F2", XK_F2},				{"F3", XK_F3},				{"F4", XK_F4},
		{"F5", XK_F5},				{"F6", XK_F6},				{"F7", XK_F7},
		{"F8", XK_F8},				{"F9", XK_F9},				{"F10", XK_F10},
		{"F11", XK_F11},			{"F12", XK_F12},			{"SPC", XK_space},
		{"SPA", XK_space},			{"LSK", XK_Super_L}, 		{"RSK", XK_Super_R},
		{"MNU", XK_Menu},			{"~", XK_asciitilde},		{"_", XK_underscore},
		{"[", XK_bracketleft},		{"]", XK_bracketright},		{"!", XK_exclam},
		{"\"", XK_quotedbl}, 		{"#", XK_numbersign},		{"$", XK_dollar},
		{"%", XK_percent},			{"&", XK_ampersand}, 		{"'", XK_quoteright},
		{"*", XK_asterisk},			{"+", XK_plus},				{",", XK_comma},
		{"-", XK_minus},			{".", XK_period}, 			{"?", XK_question},
		{"<", XK_less},				{">", XK_greater},			{"=", XK_equal},
		{"@", XK_at},				{":", XK_colon},			{";", XK_semicolon},
		{"\\", XK_backslash}, 		{"`", XK_grave},			{"{", XK_braceleft},
		{"}", XK_braceright},		{"|", XK_bar},				{"^", XK_asciicircum},
		{"(", XK_parenleft},		{")", XK_parenright}, 		{" ", XK_space},
		{"/", XK_slash},			{"\t", XK_Tab},				{"\n", XK_Return},
		{"LSH", XK_Shift_L},		{"RSH", XK_Shift_R},		{"LCT", XK_Control_L},
		{"RCT", XK_Control_R},		{"LAL", XK_Alt_L},			{"RAL", XK_Alt_R}, 
	};
	int i = 0;

	assert(name != NULL);
	assert(sym != NULL);

	/* See if we can obtain the KeySym without looking at table. 
	 * Note: XStringToKeysym("space") would return KeySym
	 * XK_space... Case sensitive. */
	*sym = XStringToKeysym(name);
	if (*sym != NoSymbol) {
		/* Got It */
		return(TRUE);
	}
	/* Do case insensitive search for specified name to obtain the KeySym from table */
	for (i = 0; i < int(sizeof(kns_table) / sizeof(KeyNameSymTable)); i++) {
		if (strcasecmp(kns_table[i].Name, name) == 0) {
			/* Found It */
			*sym = kns_table[i].Sym;
			return(TRUE);
		}
	}
	/* Not Found */	
	*sym = NoSymbol;
	return(FALSE);
}

/* Function: GetRegKeySym
 * Description: Given a regular key name as a single character(i.e., a), this
 *				function obtains the appropriate keysym by calling GetKeySym(). 
 * Note: Returns TRUE (non-zero) on success, FALSE (zero) on failure.  Also,
 *       on success, sym gets set to the appropriate keysym. On failure, sym
 * 		 will get set to NoSymbol.
 */
static BOOL GetRegKeySym(const char name, KeySym *sym)
{
	#define MAX_REG_KEY 2
	static char key[MAX_REG_KEY] = "";
	
	key[0] = name;
	key[1] = NUL;

	return( GetKeySym(key, sym) );
}

/* Function: PressKeyImp
 * Description: Presses the key for the specified keysym.  Lower-level
 * 				implementation.
 * Note: Returns TRUE (non-zero) on success, FALSE (zero) on failure.
 */
static BOOL PressKeyImp(KeySym sym)
{
	KeyCode kc = 0;
	BOOL retval = 0;

	kc = XKeysymToKeycode(TheXDisplay, sym);
	if (kc == 0) {
		return(FALSE);
	}

	retval = (BOOL)XTestFakeKeyEvent(TheXDisplay, kc, True, EventSendDelay);
	
	XFlush(TheXDisplay);
	return(retval);
}

/* Function: ReleaseKeyImp 
 * Description: Releases the key for the specified keysym.  Lower-level
 *			 	implementation.
 * Note: Returns TRUE (non-zero) on success, FALSE (zero) on failure.
 */
static BOOL ReleaseKeyImp(KeySym sym)
{
	KeyCode kc = 0;
	BOOL retval = 0;
	
	kc = XKeysymToKeycode(TheXDisplay, sym);
	if (kc == 0) {
		return(FALSE);
	}

	retval = (BOOL)XTestFakeKeyEvent(TheXDisplay, kc, False, EventSendDelay);

	XFlush(TheXDisplay);
	return(retval);
}

/* Function: PressReleaseKeyImp
 * Description: Presses and releases the key for the specified keysym.
 * 				Also implements key send delay.  Lower-level implementation.
 * Note: Returns TRUE (non-zero) on success, FALSE (zero) on failure.
 */
static BOOL PressReleaseKeyImp(KeySym sym)
{
	if (!PressKeyImp(sym)) {
		return(FALSE);
	}
	if (!ReleaseKeyImp(sym)) {
		return(FALSE);
	}
	/* Possibly wait between(after) keystrokes */ 
	if (KeySendDelay > 0) {
		/* usleep(500 * 1000) = ~500ms */
		usleep(KeySendDelay * 1000);
	}
	return(TRUE);
}

/* Function: IsShiftNeeded
 * Description: Determines if the specified keysym needs the shift
 *				modifier. 
 * Note: Returns TRUE (non-zero) on success, FALSE (zero) on failure.
 */
static BOOL IsShiftNeeded(KeySym sym)
{
	KeySym ksl = 0, ksu = 0, *kss = NULL;
	KeyCode kc = 0;
	int syms = 0;
	BOOL needed = FALSE;
	
	kc = XKeysymToKeycode(TheXDisplay, sym);
	if (!kc) {
		return(FALSE);
	}

	/* kc(grave) = kss(grave, asciitilde, ) */	
	kss = XGetKeyboardMapping(TheXDisplay, kc, 1, &syms);

	XConvertCase(sym, &ksl, &ksu);

	if (sym == kss[0] && (sym == ksl && sym == ksu)) {
		/* Not subject to case conversion */
		needed = FALSE;
	} else if (sym == ksl && sym != ksu) {
		/* Shift not needed */
		needed = FALSE;
	} else {
		/* Shift needed */
		needed = TRUE;
	}

	XFree(kss);
	return(needed);
}

/* Function: ProcessBraceSet
 * Description: Takes a brace set such as: {Tab}, {Tab 3},
 *				{Tab Tab a b c}, {PAUSE 500}, {PAUSE 500 Tab}, etc.
 *              and breaks it into components, then proceeds to press 
 *				the appropriate keys or perform the	special functionality
 *				requested (i.e., PAUSE).  Numeric elements are used in the
 *				special functionality or simply to ensure the previous key
 *				element gets pressed the specified number of times.
 * Note: Returns TRUE (non-zero) on success, FALSE (zero) on failure.
 */
static BOOL ProcessBraceSet(const char *braceset, size_t *len)
{
	enum {NONE, PAUSE, KEY}; /* Various Functionalities */
	int cmd = NONE, count = 0, i = 0;
	BOOL needshift = FALSE;
	char *buffer = NULL, *endbrc = NULL, *token = NULL;
	KeySym sym = 0;

	assert(braceset != NULL);
	assert(len != NULL);

	/* Fail if there isn't a valid brace set */
	if (*braceset != '{' || !strchr(braceset, '}')) {
		return(FALSE);
	}

	/* Create backup buffer because we are using strtok */
	buffer = (char *)malloc(strlen(braceset));
	if (buffer == NULL) {
		return(FALSE);
	}
	/* Ignore beginning { char */
	strcpy(buffer, &braceset[1]);

	/* Get brace end in buffer */
	endbrc = strchr(buffer, '}');
	if (endbrc == NULL) {
		free(buffer);
		return(FALSE);
	}
	/* If we have a quoted }, move over one character */
	if (endbrc[1] == '}') {
		endbrc++;
	}
	/* Terminate brace set */
	*endbrc = NUL;

	/* Store brace set length for calling function.  Include
	 * 2 for {} we ignored */
	*len = strlen(buffer) + 2;
	
	/* Work on the space delimited items in the buffer. */
	if ( !(token = strtok(buffer, " ")) ) {
		free(buffer);
		return(FALSE);
	}
	
	do { /* } while ( (token = strtok(NULL, " ")) ); */
		count = 0;
		if (IsNumber(token)) {
			/* Yes, a number, so convert it for key depresses or for command specific use */
			if ( (count = atoi(token)) <= 0 ) {
				free(buffer);
				return(FALSE);
			}	
		} else {
			cmd = NONE;
			/* Special functionality? */
			if (strcasecmp(token, "PAUSE") == 0) {
				/* Yes, PAUSE, so continue on to get the duration count */
				cmd = PAUSE;
				continue;	
			} else {
				/* No, just a key, so get symbol */
				cmd = KEY;
				if (!GetKeySym(token, &sym)) {
					free(buffer);
					return(FALSE);
				}
				needshift = IsShiftNeeded(sym);
				if (needshift) {
					PressKeyImp(XK_Shift_L);
				}
				/* Press key */
				if (!PressReleaseKeyImp(sym)) {
					if (needshift) {
						ReleaseKeyImp(XK_Shift_L);
					}
					free(buffer);
					return(FALSE);
				}		
				if (needshift) {
					ReleaseKeyImp(XK_Shift_L);
				}
			}
		}
		/* Handle commands that can use a specified count */
		if (count > 0) {
			switch (cmd) {
			case PAUSE:
				/* usleep(500 * 1000) = 500ms */
				usleep(count * 1000);
				break;
			case KEY:
				/* Repeat the last key if needed.  Start at iteration 2
				 * because we have already depressed key once up above */
				/* Use shift if needed */
				if (needshift) {
					PressKeyImp(XK_Shift_L);
				}
				for (i = 2; i <= count; i++) {
					/* Use sym that was already stored from above */
					if (!PressReleaseKeyImp(sym)) {
						if (needshift) {
							ReleaseKeyImp(XK_Shift_L);
						}
						free(buffer);
						return(FALSE);
					}
				}
				if (needshift) {
					ReleaseKeyImp(XK_Shift_L);
				}
				break;
			default:
				/* Fail, we have a count, but an unknown command! */
				free(buffer);
				return(FALSE);
			}; /* switch (cmd) { */
		} /* if (count > 0) { */
	} while ( (token = strtok(NULL, " ")) );	
	
	free(buffer);
	return(TRUE);
}
 
/* Function: SendKeysImp
 * Description: Underlying implementation of the SendKeys routine.  Read
 * 				the SendKeys documentation below for some specifics.
 * Note: Returns TRUE (non-zero) on success, FALSE (zero) on failure.
 *       Also, if you add special character handling below, also ensure
 * 		 the QuoteStringForSendKeys function is accurate in GUITest.pm.
 */
static BOOL SendKeysImp(const char *keys)
{
	KeySym sym = 0;
	size_t bracelen = 0;
	int i = 0;
	BOOL retval = FALSE, shift = FALSE, ctrl = FALSE, 
		 alt = FALSE, modlock = FALSE, needshift = FALSE;

	assert(keys != NULL);

	for (i = 0; i < int(strlen(keys)); i++) {
		switch (keys[i]) {
		/* Brace Set? of quoted/special characters (i.e. {{}, {TAB}, {F1 F2}, {PAUSE 200}) */
		case '{':
			if (!ProcessBraceSet(&keys[i], &bracelen)) {
				return(FALSE);
			}
			/* Skip past the brace set, Note: - 1 because we are at { already */
			i += (bracelen - 1);
			continue;
		/* Modifiers? */
		case '~': retval = PressReleaseKeyImp(XK_Return); break;
		case '+': /* Shift */ 
			retval = PressKeyImp(XK_Shift_L);
			shift = TRUE;
			break;
		case '^':  /* Control */
			retval = PressKeyImp(XK_Control_L);
			ctrl = TRUE;
			break;
		case '%': /* Alt */ 
			retval = PressKeyImp(XK_Alt_L);
			alt = TRUE; 
			break;
		case '(': modlock = TRUE; break;
		case ')': modlock = FALSE; break;
		/* Regular Key? (a, b, c, 1, 2, 3, _, *, %), etc. */
		default:
			if (!GetRegKeySym(keys[i], &sym)) {
				return(FALSE);
			}
			/* Use shift if needed */
			needshift = IsShiftNeeded(sym);
			if (!shift && needshift) {
				PressKeyImp(XK_Shift_L);
			} 
			retval = PressReleaseKeyImp(sym);
			/* Release shift if needed */	
			if (!shift && needshift) {
				ReleaseKeyImp(XK_Shift_L);
			} 
			break;
		}; /* switch (keys[i]) { */
		/* If modlock coming up next, go on to process it */
		if (keys[i + 1] == '(') {
			continue;
		}
		/* Ensure modifiers are clear when needed */
		if (!modlock && shift) {
			ReleaseKeyImp(XK_Shift_L); 
			shift = FALSE; 		
		}
		if (!modlock && ctrl) { 
			ReleaseKeyImp(XK_Control_L); 
			ctrl = FALSE;
		}	
		if (!modlock && alt) {
			ReleaseKeyImp(XK_Alt_L); 
			alt = FALSE;
		}
		if (!retval) {
			return(FALSE);
		}
	} /* for (i = 0; i < strlen(keys); i++) { */

	return(TRUE);
}

/* Function: IsWindowImp
 * Description: Underlying implementation of the IsWindow routine.  Read
 *				the IsWindow documentation below for some specifics.
 * Note: Returns non-zero for true, zero for false.
 */
static BOOL IsWindowImp(Window win)
{
	XWindowAttributes wattrs = {0};
	
	XSetErrorHandler(IgnoreBadWindow);
	return( (BOOL)XGetWindowAttributes(TheXDisplay, win, &wattrs) );
}

/* Function: AddChildWindow
 * Description: Adds the specified window Id to the internally managed
 *				table of available window Ids.  Also handles the memory
 *				allocation for this table.
 * Note: Returns TRUE (non-zero) on success, FALSE (zero) on failure.
 */
static BOOL AddChildWindow(Window win)
{
	enum {INIT = 1, GROW = 2}; /* Memory Allocation */

	if (!win) {
		return(FALSE);
	}

	if (ChildWindows.Ids == NULL) {
		/* Initialize */
		ChildWindows.Ids = (Window *)malloc(INIT * sizeof(Window));
		if (ChildWindows.Ids == NULL) {
			return(FALSE);
		}
		ChildWindows.Max = INIT;
		ChildWindows.NVals = 0;
	} else if (ChildWindows.NVals >= ChildWindows.Max) {
		/* Grow */
		Window *TempIds = NULL;
		TempIds = (Window *)realloc(ChildWindows.Ids, 
                                            (GROW * ChildWindows.Max) * sizeof(Window));
		if (TempIds == NULL) {
			return(FALSE);
		}
		ChildWindows.Max *= GROW;
		ChildWindows.Ids = TempIds;
	}
	/* Place the new window Id in */
	ChildWindows.Ids[ChildWindows.NVals] = win;
	ChildWindows.NVals++;

	return(TRUE);
}

/* Function: ClearChildWindows
 * Description: Clears the table of window Ids.  Memory allocated
 *				in AddChildWindow is not freed here, because
 *				we'll probably want to take advantage of it again. 
 * Note: No return value.
 */
static void ClearChildWindows(void)
{
	if (ChildWindows.Ids) {
		memset(ChildWindows.Ids, 0, ChildWindows.Max * sizeof(Window));
	}
	ChildWindows.NVals = 0;
}

/* Function: FreeChildWindows
 * Description: Deallocates the memory of the window Id table
 * 				that was allocated through AddChildWindow.  This
 *				should be called on exit. 
 * Note: No return value.
 */
static void FreeChildWindows(void)
{
	if (ChildWindows.Ids) {
		free(ChildWindows.Ids);
		ChildWindows.Ids = NULL;
	}
	ChildWindows.NVals = 0;
	ChildWindows.Max = 0;
}

/* Function: EnumChildWindows
 * Description: Obtains the list of window Ids
 * Note: No return value.
 */
static void EnumChildWindows(Window win)
{
   	Window root = 0, parent = 0, *children = NULL;
   	UINT childcount = 0;
	UINT i = 0;

	/* Not a window? */
	if (!IsWindowImp(win)) {
		return;
	}

	/* get list of child windows */
	if (XQueryTree(TheXDisplay, win, &root, &parent, &children, 
				   &childcount)) {
	   	for (i = 0; i < childcount; i++) {
			if (IsWindowImp(children[i])) {
				/* Add Child */
				AddChildWindow(children[i]);
				/* Look for its descendents */
	       		EnumChildWindows(children[i]);
			}
   		}
   		if (children) {
       		XFree(children);
   		}
	}
}

/* **************************************************
 * Start of exported functions.
 * ************************************************** 
 */       

void InitGUITest()
{
    /* Things to do on initialization */
    SetupXDisplay();
    XTestGrabControl(TheXDisplay, True);
}

void DeInitGUITest()
{   
    /* Things to do on deinitialization */
    CloseXDisplay();
    FreeChildWindows();	
}

/*
=item SetEventSendDelay DELAYINMILLISECONDS

Sets the milliseconds of delay between events being sent to the
X display.  It is usually not a good idea to set this to 0.

Please note that this delay will also affect SendKeys.

Returns the old delay amount in milliseconds.
*/

ULONG SetEventSendDelay(ULONG delay) 
{
    /* Returning old delay amount */
    ULONG ret = EventSendDelay;
    EventSendDelay = delay;
    return ret;
}

/*
=item GetEventSendDelay

Returns the current event sending delay amount in milliseconds.
*/

ULONG GetEventSendDelay()
{
    return EventSendDelay;
}

/*
=item SetKeySendDelay DELAYINMILLISECONDS

Sets the milliseconds of delay between keystrokes.

Returns the old delay amount in milliseconds.
*/
ULONG SetKeySendDelay(ULONG delay)
{
    /* Returning old delay amount */
    ULONG ret = KeySendDelay;
    KeySendDelay = delay;
    return ret;
}

/*
=item GetKeySendDelay

Returns the current keystroke sending delay amount in milliseconds.
*/
ULONG GetKeySendDelay()
{
    return KeySendDelay;
}

/*
=item GetWindowName WINDOWID

Returns the window name for the specified window Id.  undef
is returned if name could not be obtained.

  # Return the name of the window that has the input focus.
  my $WinName = GetWindowName(GetInputFocus());
*/
char* GetWindowName(Window win)
{
    char *name = NULL;
    if (IsWindowImp(win)) {
        XFetchName(TheXDisplay, win, &name);
    }
            
    return name;
}

/*
=item SetWindowName WINDOWID, NAME

Sets the window name for the specified window Id.

zero is returned on failure, non-zero for success.
*/

BOOL SetWindowName(Window win, char *name)
{    
    XTextProperty textprop = {0};
    size_t namelen = 0;
    Atom utf8_string = 0;
    Atom net_wm_name = 0;
    Atom net_wm_icon_name = 0;
    BOOL RETVAL = FALSE;
    
    if (IsWindowImp(win)) {
        if (XStringListToTextProperty(&name, 1, &textprop)) {
            XSetWMName(TheXDisplay, win, &textprop);
            XSetWMIconName(TheXDisplay, win, &textprop);
            XFree(textprop.value);
            RETVAL = TRUE;
        }
        /* These UTF8 window name properties can be the properties
         * that get displayed, so we set them too. */
        utf8_string = XInternAtom(TheXDisplay, "UTF8_STRING", True);
        if (utf8_string != None) {
            net_wm_name = XInternAtom(TheXDisplay, "_NET_WM_NAME", True);
            net_wm_icon_name = XInternAtom(TheXDisplay, "_NET_WM_ICON_NAME", True);
            if (net_wm_name != None && net_wm_icon_name != None) {
                namelen = strlen(name);
                XChangeProperty(TheXDisplay, win, net_wm_name, utf8_string, 8,
                                PropModeReplace, (unsigned char *)name, namelen);
                XChangeProperty(TheXDisplay, win, net_wm_icon_name, utf8_string, 8,
                                PropModeReplace, (unsigned char *)name, namelen);
            }
        }
    }
    return RETVAL;
}

/*
=item GetRootWindow

Returns the root window Id.  This is the top/root level window that
all other windows are under.
*/
Window GetRootWindow()
{
    return RootWindow(TheXDisplay, TheScreen);
}

/*
=item GetChildWindows WINDOWID

Returns an array of the child windows for the specified
window Id. 
*/

Window* GetChildWindows(Window win, UINT *nchild)
{
    UINT i = 0;
    Window *children;
    EnumChildWindows(win);

    children = (Window*)malloc(sizeof(Window)*ChildWindows.NVals);
    *nchild = ChildWindows.NVals;
    for (i = 0; i < ChildWindows.NVals; i++) {
        children[i] = ChildWindows.Ids[i];
    }
    ClearChildWindows();
    return children;
}


/*
=item MoveMouseAbs X, Y

Moves the mouse cursor to the specified absolute position.

zero is returned on failure, non-zero for success.
*/
BOOL MoveMouseAbs(int x, int y)
{
    BOOL RETVAL = (BOOL)XTestFakeMotionEvent(TheXDisplay, TheScreen, x, y, 
                                             EventSendDelay);
    XFlush(TheXDisplay);
    return RETVAL;
}

/*
=item GetMousePos

Returns an array containing the position of the mouse cursor.

  my ($x, $y) = GetMousePos(); 
*/
void GetMousePos(int *root_x, int *root_y)
{
    Window root = 0, child = 0;
    int win_x = 0, win_y = 0;
    UINT mask = 0;
    *root_x = 0; 
    *root_y = 0;
    XQueryPointer(TheXDisplay, RootWindow(TheXDisplay, TheScreen),
                  &root, &child, root_x, root_y,
                  &win_x, &win_y, &mask);
}

/*
=item PressMouseButton BUTTON

Presses the specified mouse button.  Available mouse buttons
are: M_LEFT, M_MIDDLE, M_RIGHT.  Also, you could use the logical
Id for the button: M_BTN1, M_BTN2, M_BTN3, M_BTN4, M_BTN5.  These
are all available through the :CONST export tag.

zero is returned on failure, non-zero for success.
*/

BOOL PressMouseButton(int button)
{
    BOOL RETVAL = (BOOL)XTestFakeButtonEvent(TheXDisplay, button, True, 
                                             EventSendDelay);
    XFlush(TheXDisplay);
    return RETVAL;
}

/*
=item ReleaseMouseButton BUTTON

Releases the specified mouse button.  Available mouse buttons
are: M_LEFT, M_MIDDLE, M_RIGHT.  Also, you could use the logical
Id for the button: M_BTN1, M_BTN2, M_BTN3, M_BTN4, M_BTN5.  These
are all available through the :CONST export tag.

zero is returned on failure, non-zero for success.
*/

BOOL ReleaseMouseButton(int button)
{
    BOOL RETVAL = (BOOL)XTestFakeButtonEvent(TheXDisplay, button, False, 
                                             EventSendDelay);
    XFlush(TheXDisplay);
    return RETVAL;
}

/*
=item SendKeys KEYS

Sends keystrokes to the window that has the input focus.

The keystrokes to send are those specified in KEYS.  Some characters
have special meaning, they are:

        Modifier Keys:
        ^    	CTRL
        %    	ALT
        +    	SHIFT

        Other Keys:
        ~    	ENTER
        \n   	ENTER
        \t  	TAB
        ( and ) MODIFIER USAGE
        { and } QUOTE CHARACTERS

Simply, one can send a text string like so:

        SendKeys('Hello, how are you today?');

Parenthesis allow a modifier to work on one or more characters.  For example:

        SendKeys('%(f)q'); # Alt-f, then press q
        SendKeys('%(fa)^(m)'); # Alt-f, Alt-a, Ctrl-m
        SendKeys('+(abc)'); # Uppercase ABC using shift modifier
        SendKeys('^(+(l))'); # Ctrl-Shift-l
        SendKeys('+'); # Press shift

Braces are used to quote special characters, for utilizing aliased key
names, or for special functionality. Multiple characters can be specified
in a brace by space delimiting the entries.  Characters can be repeated using
a number that is space delimited after the preceeding key.

Quote Special Characters

        SendKeys('{{}'); # {
        SendKeys('{+}'); # +

        You can also use QuoteStringForSendKeys to perform quoting.

Aliased Key Names

        SendKeys('{BAC}'); # Backspace
        SendKeys('{F1 F2 F3}'); # F1, F2, F3
        SendKeys('{TAB 3}'); # Press TAB 3 times
        SendKeys('{SPC 3 a b c}'); # Space 3 times, a, b, c

Special Functionality

        # Pause execution for 500 milliseconds
        SendKeys('{PAUSE 500}');

Combinations

        SendKeys('abc+(abc){TAB PAUSE 500}'); # a, b, c, A, B, C, Tab, Pause 500
        SendKeys('+({a b c})'); # A, B, C

The following abbreviated key names are currently recognized within a brace set.  If you
don't see the desired key, you can still use the unabbreviated name for the key.  If you
are unsure of this name, utilize the xev (X event view) tool, press the key you
want and look at the tools output for the name of that key.  Names that are in the list
below can be utilized regardless of case.  Ones that aren't in this list are going to be
case sensitive and also not abbreviated.  For example, using 'xev' you will find that the
name of the backspace key is BackSpace, so you could use {BackSpace} in place of {bac}
if you really wanted to.

        Name    Action
        -------------------
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

zero is returned on failure, non-zero for success.
*/

BOOL SendKeys(char *keys)
{
    BOOL RETVAL = SendKeysImp(keys);   
    return RETVAL;
}


/*
=item PressKey KEY 

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
*/

BOOL PressKey(char *key)
{
    KeySym sym = 0;
    BOOL RETVAL = GetKeySym(key, &sym);
    if (RETVAL) {
        RETVAL = PressKeyImp(sym);
    }
    return RETVAL;
}

/*
=item ReleaseKey KEY 

Releases the specified key.  Normally follows a PressKey call.

One can utilize the abbreviated key names from the table
listed above.

  ReleaseKey('n');

zero is returned on failure, non-zero for success.
*/

BOOL ReleaseKey(char *key)
{
    KeySym sym = 0;

    BOOL RETVAL = GetKeySym(key, &sym);
    if (RETVAL) {
        RETVAL = ReleaseKeyImp(sym);
    }
    return RETVAL;   
}

/*
=item PressReleaseKey KEY 

Presses and releases the specified key.

One can utilize the abbreviated key names from the table
listed above.

  PressReleaseKey('n');

This function is effected by the key send delay.

zero is returned on failure, non-zero for success.
*/

BOOL PressReleaseKey(char *key)
{
    KeySym sym = 0;
    BOOL RETVAL = GetKeySym(key, &sym);
    if (RETVAL) {
        RETVAL = PressReleaseKeyImp(sym);
    }
    return RETVAL;
}

/*
=item IsKeyPressed KEY

Determines if the specified key is currently being pressed.  

You can specify such things as 'bac' or the unabbreviated form 'BackSpace' as
covered in the SendKeys information.  Brace forms such as '{bac}' are
unsupported.  A '{' is taken literally and letters are case sensitive.

  if (IsKeyPressed('esc')) {  # Is Escape pressed?
  if (IsKeyPressed('a')) { # Is a pressed?
  if (IsKeyPressed('A')) { # Is A pressed?

Returns non-zero for true, zero for false.
*/

BOOL IsKeyPressed(char *key)
{
    int pos = 0;
    KeySym sym = 0;
    KeyCode kc = 0, skc = 0;
    BOOL keyon = FALSE, shifton = FALSE;
    char keys_return[KEYMAP_VECTOR_SIZE] = "";
    BOOL RETVAL;
    if (key && GetKeySym(key, &sym)) {
        kc = XKeysymToKeycode(TheXDisplay, sym);
        skc = XKeysymToKeycode(TheXDisplay, XK_Shift_L); 
        XQueryKeymap(TheXDisplay, keys_return);
        for (pos = 0; pos < (KEYMAP_VECTOR_SIZE * KEYMAP_BIT_COUNT); pos++) {
            /* For the derived keycode, are we at the correct bit position for it? */
            if (kc == pos) {
                /* Check the bit at this position to determine the state of the key */
                if ( keys_return[pos / KEYMAP_BIT_COUNT] & (1 << (pos % KEYMAP_BIT_COUNT)) ) {
                    /* Bit On, so key is pressed */
                    keyon = TRUE;
                }
            }
            /* For the shift keycode, ... */
            if (skc == pos) {
                /* Check the bit at this position to determine the state of the shift key */
                if ( keys_return[pos / KEYMAP_BIT_COUNT] & (1 << (pos % KEYMAP_BIT_COUNT)) ) {
                    /* Bit On, so shift is pressed */
                    shifton = TRUE;
                }
            }
        } /* for (pos = 0; pos < (KEYMAP_VECTOR_SIZE * KEYMAP_BIT_COUNT); pos++) { */
    } /* if (key && GetKeySym(key, &sym)) { */
	
    /* Determine result */
    if (keyon) {
        /* Key is on, so use its keysym to determine if shift modifier needs to be verified also */
        if (IsShiftNeeded(sym)) {
            RETVAL = (shifton);
        } else {
            RETVAL = (!shifton);	
        }
    } else {
        /* Key not on, so it is not pressed */
        RETVAL = FALSE;
    }
    
    return RETVAL;
}

/*
=item IsMouseButtonPressed BUTTON

Determines if the specified mouse button is currently being pressed.  

Available mouse buttons are: M_LEFT, M_MIDDLE, M_RIGHT.  Also, you
could use the logical Id for the button: M_BTN1, M_BTN2, M_BTN3,
M_BTN4, M_BTN5.  These are all available through the :CONST export
tag.

  if (IsMouseButtonPressed(M_LEFT)) { # Is left button pressed?

Returns non-zero for true, zero for false.
*/

BOOL IsMouseButtonPressed(int button)
{
    Window root = 0, child = 0;
    int root_x = 0, root_y = 0;
    int win_x = 0, win_y = 0;
    UINT mask = 0;
    BOOL RETVAL;
    
    XQueryPointer(TheXDisplay, RootWindow(TheXDisplay, TheScreen),
                  &root, &child, &root_x, &root_y,
                  &win_x, &win_y, &mask);
    switch (button) {
    case Button1:
        RETVAL = (mask & Button1Mask);
        break;
    case Button2:
        RETVAL = (mask & Button2Mask);
        break;
    case Button3:
        RETVAL = (mask & Button3Mask);
        break;
    case Button4:
        RETVAL = (mask & Button4Mask);
        break;
    case Button5:
        RETVAL = (mask & Button5Mask);
        break;
    default:
        RETVAL = FALSE;
        break;
    };
    return RETVAL;
}

/*
=item IsWindow WINDOWID

zero is returned if the specified window Id is not for something
that can be recognized as a window.  non-zero is returned if it
looks like a window.
*/

BOOL IsWindow(Window win)
{
    return IsWindowImp(win);
}

/*
=item IsWindowViewable WINDOWID

zero is returned if the specified window Id is for a window that
isn't viewable.  non-zero is returned if the window is viewable.
*/

BOOL IsWindowViewable(Window win)
{
    BOOL RETVAL;
    XWindowAttributes wattrs = {0};
    XSetErrorHandler(IgnoreBadWindow);
    if (!XGetWindowAttributes(TheXDisplay, win, &wattrs)) {
        RETVAL = FALSE;
    } else { 
        RETVAL = (wattrs.map_state == IsViewable);
    }
    return RETVAL;
}

/*
=item MoveWindow WINDOWID, X, Y

Moves the window to the specified location.

zero is returned on failure, non-zero for success.
*/

BOOL MoveWindow(Window win, int x, int y)
{   
    BOOL RETVAL;
    XSetErrorHandler(IgnoreBadWindow);
    RETVAL = XMoveWindow(TheXDisplay, win, x, y);
    XFlush(TheXDisplay);
    return RETVAL;
}

/*
=item ResizeWindow WINDOWID, WIDTH, HEIGHT

Resizes the window to the specified size.

zero is returned on failure, non-zero for success.
*/

BOOL ResizeWindow(Window win, int w, int h)
{
    BOOL RETVAL;
    XSetErrorHandler(IgnoreBadWindow);
    RETVAL = XResizeWindow(TheXDisplay, win, w, h);
    XFlush(TheXDisplay);
    return RETVAL;
}

/*
=item IconifyWindow WINDOWID

Minimizes (Iconifies) the specified window.

zero is returned on failure, non-zero for success.
*/


BOOL IconifyWindow(Window win)
{
    BOOL RETVAL;
    XSetErrorHandler(IgnoreBadWindow);
    RETVAL = XIconifyWindow(TheXDisplay, win, TheScreen);
    XFlush(TheXDisplay);
    return RETVAL;
}

/*
=item UnIconifyWindow WINDOWID

Unminimizes (UnIconifies) the specified window.

zero is returned on failure, non-zero for success.
*/

BOOL UnIconifyWindow(Window win)
{
    BOOL RETVAL;
    XSetErrorHandler(IgnoreBadWindow);
    RETVAL = XMapWindow(TheXDisplay, win);
    XFlush(TheXDisplay);
    return RETVAL;
}

/*
=item RaiseWindow WINDOWID

Raises the specified window to the top of the stack, so
that no other windows cover it.

zero is returned on failure, non-zero for success.
*/

BOOL RaiseWindow(Window win)
{
    BOOL RETVAL;
    XSetErrorHandler(IgnoreBadWindow);
    RETVAL = XRaiseWindow(TheXDisplay, win);
    XFlush(TheXDisplay);
    return RETVAL;
}


/*
=item LowerWindow WINDOWID

Lowers the specified window to the bottom of the stack, so
other existing windows will cover it.

zero is returned on failure, non-zero for success.
*/

BOOL LowerWindow(Window win)
{
    BOOL RETVAL;
    XSetErrorHandler(IgnoreBadWindow);
    RETVAL = XLowerWindow(TheXDisplay, win);
    XFlush(TheXDisplay);
    return RETVAL;
}

/*
=item GetInputFocus

Returns the window that currently has the input focus.
*/

Window GetInputFocus()
{
    Window focus = 0;
    int revert = 0;
    XGetInputFocus(TheXDisplay, &focus, &revert);
    return focus;
}


/*
=item SetInputFocus WINDOWID

Sets the specified window to be the one that has the input focus.

zero is returned on failure, non-zero for success.

*/


BOOL SetInputFocus(Window win)
{
    
    Window focus = 0;
    int revert = 0;
    XSetErrorHandler(IgnoreBadWindow);
    /* Note: Per function man page, there is no effect if the time parameter
     *  	 of this call isn't accurate.  Will use CurrentTime.  Also, it
     *		 appears that we can't trust its return value. */
    XSetInputFocus(TheXDisplay, win, RevertToParent, CurrentTime);
    XFlush(TheXDisplay);
    /* Verify that the window now has focus.  Used to determine return value */
    XGetInputFocus(TheXDisplay, &focus, &revert);
    return (focus == win);
}


/*
=item GetWindowPos WINDOWID

Returns an array containing the position information for the specified
window.

  my ($x, $y, $width, $height) = GetWindowPos(GetRootWindow());
*/

void GetWindowPos(Window win, int *x, int *y, int *width, int *height)
{
    XWindowAttributes wattrs = {0};
    Window child = 0, parent = 0, *children = NULL, root = 0;
    UINT childcount = 0; 
    XSetErrorHandler(IgnoreBadWindow);
    XGetWindowAttributes(TheXDisplay, win, &wattrs);
    if (XQueryTree(TheXDisplay, win, &root, &parent, &children, &childcount)) {
        XFree(children);
        XTranslateCoordinates(TheXDisplay, parent, wattrs.root, 
                              wattrs.x, wattrs.y, x, y, &child);
        *width = wattrs.width;
        *height = wattrs.height;
    }
}


/*
=item GetParentWindow WINDOWID

Returns the parent of the specified window.

zero is returned if parent couldn't be determined (i.e., root window).
*/

Window GetParentWindow(Window win)
{
    Window parent = 0, *children = NULL, root = 0;
    UINT childcount = 0; 
    Window RETVAL = 0;
    if (XQueryTree(TheXDisplay, win, &root, &parent, &children, &childcount)) {
        XFree(children);
        RETVAL = parent;
    }
    return RETVAL;
}


/*
=item GetScreenRes

Returns the screen resolution.

  my ($x, $y) = GetScreenRes();
*/

void GetScreenRes(int *x, int *y)
{
    *x = DisplayWidth(TheXDisplay, TheScreen);
    *y = DisplayHeight(TheXDisplay, TheScreen);
}


/*
=item GetScreenDepth

Returns the color depth for the screen.  

Value is represented as bits, i.e. 16.

  my $depth = GetScreenDepth();
*/

int GetScreenDepth()
{
    return DefaultDepth(TheXDisplay, TheScreen);
}

