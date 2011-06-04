#-------------------------------------------------------------------------------
#
#  Defines the base adapter class used for creating Envisage ExtensionPoint
#  adapters. This is also the class used as the adapter for Envisage extension
#  points for which an explicit adapter class cannot be found.
#
#  Written by: David C. Morrill
#
#  Date: 06/16/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import sys

from types import FunctionType

from os.path \
    import join, exists

from traits.api \
    import List, Property

from traitsui.api \
    import View, Tabbed, VGroup, Item, Include, ListEditor

from traitsui.menu \
    import NoButtons

from enthought.developer.tools.envisage_browser.object_adapter \
    import ObjectAdapter

#-------------------------------------------------------------------------------
#  'ExtensionPointClassAdapter' class:
#-------------------------------------------------------------------------------

class ExtensionPointClassAdapter ( ObjectAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the extension point:
    name = Property

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View(
               Tabbed(
                   VGroup(
                       VGroup(
                           Item( 'name~' ),
                           label       = 'Description',
                           show_border = True
                       ),
                       VGroup(
                           Item( 'file_name~' ),
                           label       = 'Implementation',
                           show_border = True
                       ),
                       label = 'Definition',
                       dock  = 'tab'
                   ),
                   VGroup(
                       Item( 'file_name~' ),
                       VGroup(
                           Item( 'source~', show_label = False )
                       ),
                       label = 'Source Code',
                       dock  = 'tab'
                   ),
                   id = 'tabbed'
               ),
               id        = 'enthought.developer.tools.envisage_browser.'
                          'extension_point__adapter.ExtensionPointClassAdapter',
               title     = 'Extension Point Class Definition',
               resizable = True,
               buttons   = NoButtons
           )

#-- Property Implementations ---------------------------------------------------

    def _get_name ( self ):
        return self.adaptee.id

#-------------------------------------------------------------------------------
#  'ExtensionPointAdapter' class:
#-------------------------------------------------------------------------------

class ExtensionPointAdapter ( ObjectAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the extension point:
    name = Property

    # The list of available trait names:
    names = Property

    # List of all parent objects:
    parents = List

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        Tabbed(
            VGroup(
                Include( 'content' ),
                VGroup(
                    Item( 'file_name~' ),
                    label       = 'Implementation',
                    show_border = True
                ),
                label = 'Definition',
                dock  = 'tab'
            ),
            VGroup(
                Item( 'file_name~' ),
                VGroup(
                    Item( 'source~', show_label = False ),
                ),
                label = 'Source Code',
                dock  = 'tab'
            ),
            VGroup(
                Item( 'parents@',
                      show_label = False,
                      editor     = ListEditor( use_notebook = True,
                                               view         = 'simple' )
                ),
                label        = 'Contained In',
                dock         = 'tab',
                defined_when = 'len( parents ) > 0'
            ),
            Include( 'extra_page' ),
            Include( 'extra_page2' ),
            Include( 'extra_page3' ),
            Include( 'extra_page4' ),
            id = 'tabbed'
        ),
        id        = 'enthought.developer.tools.envisage_browser.'
                    'extension_point_adapter.ExtensionPointAdapter',
        title     = 'Extension Point Definition',
        resizable = True,
        buttons   = NoButtons
    )

    simple = View(
        VGroup(
            Include( 'content' )
        )
    )

#-- Public Methods -------------------------------------------------------------

    def get_all_children ( self ):
        """ Returns adapted version of all extension points contained within
            this one.
        """
        gef       = self.application.get_extension_for
        file_name = self.file_name
        result    = []
        queue     = [ ( self, child ) for child in self.get_children() ]
        while len( queue ) > 0:
            container, child = queue.pop()
            ep = gef( child, file_name, container )
            result.append( ep )
            queue.extend( [ ( ep, child ) for child in ep.get_children() ] )

        return result

    def get_children ( self ):
        """ Returns the unadapted extension points immediately contained within
            this one.

            Note: This method should be overridden by subclasses.
        """
        return []

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.

            Note: This method should be overridden by subclasses.
        """
        return []

#-- Property Implementations ---------------------------------------------------

    def _get_name ( self ):
        if isinstance(self.adaptee, FunctionType):
            name = self.adaptee.func_name
        else:
            name = 'Instance of ' + self.adaptee.__class__.__name__
        return name

    def _get_names ( self ):
        if self._names is None:
            self._names = self.get_names()

        return self._names

    def _parents_default ( self ):
        parents = []
        item    = self
        while item.container is not None:
            item = item.container
            parents.append( item )
        return parents

    def _get_class_source ( self, name ):
        fname  = '_' + name
        result = getattr( self, fname )
        if result is None:
            class_name = getattr( self, name[:-7], '' )
            if class_name == '':
                setattr( self, fname, '' )
                return ''

            root   = join( *class_name.split( '.' )[:-1] ) + '.py'
            result = ''
            for path in sys.path:
                name = join( path, root )
                if exists( name ):
                    fh = None
                    try:
                        fh     = file( name, 'rb' )
                        result = fh.read()
                    except:
                        pass
                    if fh is not None:
                        fh.close()
                    break

            setattr( self, fname, result )

        return result

