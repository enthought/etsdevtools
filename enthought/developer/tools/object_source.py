#-------------------------------------------------------------------------------
#
#  Object source inspector/debugger plugin
#
#  Written by: David C. Morrill
#
#  Date: 06/25/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import sys

from os.path \
    import join, exists, basename

from enthought.traits.api \
    import HasTraits, HasPrivateTraits, Any, Instance, List, Property, File, \
           Directory, Str

from enthought.traits.ui.api \
    import View, VGroup, HGroup, Item, ListEditor, TreeEditor

from enthought.traits.ui.value_tree \
    import TraitsNode

from enthought.pyface.timer.api \
    import do_later

from enthought.developer.tools.class_browser \
    import CBModuleFile, CBClass, cb_tree_nodes

from enthought.developer.api \
    import HasPayload, FilePosition

from enthought.developer.helper.themes \
    import TTitle

#-------------------------------------------------------------------------------
#  'ObjectDebugger' class:
#-------------------------------------------------------------------------------

class ObjectDebugger ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The object that created this view:
    object_source = Any

    # The path of the file being debugged:
    file_name = File

    # The Python path the file was found in:
    python_path = Directory

    # The name to use on the debugger page:
    name = Property

    # The object being debugged:
    object = Any

    # The module descriptor for the file:
    module = Instance( CBModuleFile )

    # The currently selected object class:
    selected = Any

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View(
        Item( 'module',
              id         = 'browser',
              show_label = False,
              editor     = TreeEditor( nodes    = cb_tree_nodes,
                                       editable = False,
                                       selected = 'selected' ),
              resizable  = True
        ),
        id        = 'enthought.developer.tools.object_source.ObjectDebugger',
        resizable = True
    )

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__ ( self, **traits ):
        """ Initializes the object.
        """
        super( ObjectDebugger, self ).__init__( **traits )
        self.module = CBModuleFile( path        = self.file_name,
                                    python_path = self.python_path,
                                    object      = self.object )
        do_later( self.select_object )

    #---------------------------------------------------------------------------
    #  Selects the class of the current object in the class browser:
    #---------------------------------------------------------------------------

    def select_object ( self ):
        """ Selects the class of the current object in the class browser.
        """
        name = self.object.__class__.__name__
        for cb_class in self.module.get_children():
            if name == cb_class.name:
                self.selected = cb_class
                break

    #---------------------------------------------------------------------------
    #  Handles the 'selected' trait being changed:
    #---------------------------------------------------------------------------

    def _selected_changed ( self, selected ):
        """ Handles a tree node being selected.
        """
        # Read the object's text to force it to calculate the starting
        # line number of number of lines in the text fragment:
        ignore = selected.text

        # Set the file position for the object:
        self.object_source.file_position = FilePosition(
                                           name      = selected.name,
                                           file_name = selected.path,
                                           line      = selected.line_number + 1,
                                           lines     = selected.lines,
                                           object    = self.object )

    #---------------------------------------------------------------------------
    #  The implementation of the 'name' property:
    #---------------------------------------------------------------------------

    def _get_name ( self ):
        return basename( self.file_name )

#-------------------------------------------------------------------------------
#  'ObjectSource' plugin:
#-------------------------------------------------------------------------------

class ObjectSource ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'Object Source' )
    
    # The current item being inspected:
    item = Instance( HasTraits,
                     droppable = 'Drop an object with traits here.',
                     connect   = 'both: object with traits' )

    # Description of the current object being inspected:
    description = Str( 'Drag an object to the circular image above to view '
                       'its source' )

    # The currently selected file position:
    file_position = Instance( FilePosition,
                        draggable = 'Drag currently selected file position.',
                        connect   = 'from: file position' )

    # Current list of items being inspected:
    inspectors = List

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View(
        TTitle( 'description' ),
        Item( 'inspectors@',
              show_label = False,
              editor     = ListEditor( use_notebook = True,
                                       deletable    = True,
                                       page_name    = '.name',
                                       dock_style   = 'tab' )
        )
    )

#-- Event Handlers -------------------------------------------------------------

    #---------------------------------------------------------------------------
    #  Handles the 'item' trait being changed:
    #---------------------------------------------------------------------------

    def _item_changed ( self, item ):
        """ Handles the 'item' trait being changed.
        """
        if isinstance( item, HasPayload ):
            item = item.payload

        if isinstance( item, TraitsNode ):
            item = item.value

        if item is not None:
            inspectors       = []
            self._file_names = []
            description      = ''
            for klass in item.__class__.__mro__:
                module = klass.__module__.split( '.' )
                module_name = module[-1]
                if module_name != '__builtin__':
                    module_name += '.py'
                if len( description ) > 0:
                    description += ' -> '
                description += '%s[%s]' % ( klass.__name__, module_name )
                inspector = self.inspector_for( join( *module ), item )
                if inspector is not None:
                    inspectors.append( inspector )
                    self._file_names.append( inspector.file_name )
            self.inspectors  = inspectors
            self.description = description
            do_later( self.set, item = None )

    #---------------------------------------------------------------------------
    #  Returns the inspector object for a specified class (if possible):
    #---------------------------------------------------------------------------

    def inspector_for ( self, module, object ):
        """ Returns the inspector object for a specified class (if possible).
        """
        for path in sys.path:
            file_name = join( path, module + '.py' )
            if exists( file_name ):
                if file_name in self._file_names:
                    break
                return ObjectDebugger( object_source = self,
                                       file_name     = file_name,
                                       python_path   = path,
                                       object        = object )

        return None

#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

view = ObjectSource()

