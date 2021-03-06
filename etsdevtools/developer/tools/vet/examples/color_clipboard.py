#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: David C. Morrill
# Description: The 'ViewHandler' traits view definition and handler.
#    Usage is:
#    ViewHandler().edit_traits( context = object_to_edit, ... )
#    Generated by the VET tool (version 0.1.0) on Fri Jan 21 20:41:27 2005.
#------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from traitsui.api import Handler, View, Group, Item, RGBColorEditor
from traitsui.menu import MenuBar, Menu, Action, Separator
import traitsui

#-------------------------------------------------------------------------------
#  'ViewHandler' class:
#-------------------------------------------------------------------------------

class ViewHandler ( Handler ):

    #---------------------------------------------------------------------------
    #  Handles the object's 'color' trait changing value:
    #---------------------------------------------------------------------------

    def object_color_changed ( self, info ):
        """ Handles the object's 'color' trait changing value.
        """
        from pyface.wx.clipboard import clipboard as cb
        c      = info.object.color_
        format = info.object.format
        if format == 'Web':
            cb.data = '#%02X%02X%02X' % (
                      int( 255 * c[0] ),
                      int( 255 * c[1] ),
                      int( 255 * c[2] ) )
        elif format == 'Enable':
            cb.data = '( %.3f, %.3f, %.3f, %.3f )' % c
        else:
            cb.data = 'wx.Colour( %d, %d, %d )' % (
                      int( 255 * c[0] ),
                      int( 255 * c[1] ),
                      int( 255 * c[2] ) )

    #---------------------------------------------------------------------------
    #  Handles the object's 'format' trait changing value:
    #---------------------------------------------------------------------------

    def object_format_changed ( self, info ):
        """ Handles the object's 'format' trait changing value.
        """
        self.object_color_changed( info )

    #---------------------------------------------------------------------------
    #  Traits view definition:
    #---------------------------------------------------------------------------

    traits_view = View(
        Group(
            Group(
                Item(
                    editor = RGBColorEditor(),
                    name   = 'color',
                    style  = 'custom'
                ),
                show_labels = False
            ),
            Group(
                Item(
                    name  = 'format',
                    style = 'custom'
                ),
                label       = 'Format',
                show_border = True,
                show_labels = False
            )
        ),
        title   = 'Color Clipboard',
        id      = 'traits.vet.examples.color_clipboard',
        buttons = [ 'OK', 'Cancel' ]
    )

#-------------------------------------------------------------------------------
#  'ViewHandler' test case:
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    import traits.vet.examples.color_info
    ViewHandler().configure_traits( context = {
        'object': traits.vet.examples.color_info.ColorInfo()
    } )
