Guitest is currently a bunch of useful utilities for unit testing
UI's.

Currently, this only supports X11 and Win32.  The core of this module
is a translation of the Perl X11::GUITest and Win32::GuiTest modules.

  http://cpan.uwinnipeg.ca/dist/X11-GUITest
  http://cpan.uwinnipeg.ca/dist/Win32-GuiTest

As of Jan. 8 2006, the guitest Python module is up-to-date with the
X11::GUITest version 0.20.  The Win32 module is based on a slightly
older version of Win32::GuiTest version 1.50.3-ad.

The above were Perl specific and I have converted them to use SWIG
instead.  In theory the swig source (guitest.i) file can be used to
wrap this functionality to other languages.  However, the current
effort focusses on Python.  The wrapping is complete and also includes
full function documentation extracted from the Perl module sources.

The X11 module requires that you have the XTest extensions enabled.
Under X11 there is also a simple wrapper to the `xnee` program.

  http://www.gnu.org/software/xnee/

From the xnee man page:

       The program Xnee can record and replay an X session. Xnee also
       has the ability to distribute events to multiple displays.
       Xnee gets copies of X protocol data from the X server. These
       are either printed to file ( record mode) or replayed and
       synchronised ( replay mode).  During record and replay Xnee can
       distribute the record/replayed events to multiple displays.

The xnee.py module provides two functions, to record and playback X11
events.

The win32 directory contains the winGuiAuto.py module by Simon
Brunning.  This is not used directly by any of the guitest code.  I've
just included this since it is not readily available and presents an
alternative pure Python approach to doing what guitest does.

It would probably be a good idea to try and use python-xlib instead of
guitest in order to make guitest a pure Python module.

 http://python-xlib.sourceforge.net/


The win32 and x11 modules are not similar.  Therefore it is not
possible to write one program that works with either.  It probably
would be a good idea to fix this if necessary later on.

Please note that X11::GUITest uses the GPL license.  Win32::GuiTest is
distributed under GPL/Artistic license.


Prabhu Ramachandran
<prabhu_r at users dot sf dot net>
