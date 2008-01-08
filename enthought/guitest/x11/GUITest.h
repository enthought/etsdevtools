/* X11::GUITest ($Id: GUITest.h,v 1.10 2003/12/07 15:46:31 ctrondlp Exp $)
 *  
 * Copyright (c) 2003-2004  Dennis K. Paulsen, All Rights Reserved.
 * Email: ctrondlp@users.sourceforge.net
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
#ifndef GUITest_h
#define GUITest_h


#ifndef BOOL
#define BOOL int
#endif
#ifndef UINT
#define UINT unsigned int
#endif
#ifndef ULONG
#define ULONG unsigned long
#endif

#define NUL '\0'

#define DEF_EVENT_SEND_DELAY 10 /* Value < 10 not recommended */
#define DEF_KEY_SEND_DELAY 0 
#define KEYMAP_VECTOR_SIZE 32
#define KEYMAP_BIT_COUNT 8


typedef struct WindowTable {
	Window *Ids;
	UINT NVals;
	UINT Max;
} WindowTable;

typedef struct KeyNameSymTable {
	char *Name; 
	KeySym Sym;
} KeyNameSymTable;


#endif /* #ifndef GUITest_h */

