#-------------------------------------------------------------------------------
#
#  Plugin for displaying trait listeners for a specified object and trait.
#
#  Written by: David C. Morrill
#
#  Date: 07/21/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from os.path \
    import basename, splitext

from traits.api \
    import HasPrivateTraits, Any, Instance, List, Property, Str

from traitsui.api \
    import View, Item, TableEditor

from traitsui.table_column \
    import ObjectColumn

from etsdevtools.developer.api \
    import FilePosition, TraitValue, read_file

#-------------------------------------------------------------------------------
#  'ListenerItem' class:
#-------------------------------------------------------------------------------

class ListenerItem ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The trait notifier associated with this item:
    notifier = Any

    # The class name of the notifier object:
    class_name = Property

    # The notifier object:
    object = Property

    # The object id of the notifier object:
    object_id = Property

    # Module name of the notifier:
    module_name = Property

    # Method/Function name of the notifier:
    method_name = Property

    # Line number of the notifier:
    line = Property

    # Source file name of the notifier:
    file_name = Property

    # Source line of the notifier:
    source = Property

    # The notifier handler:
    handler = Property

#-- Property Implementations ---------------------------------------------------

    def _get_class_name ( self ):
        if self._class_name is None:
            self._class_name = ''
            if hasattr( self.notifier, 'object' ):
                self._class_name = self.notifier.object().__class__.__name__

        return self._class_name

    def _get_object ( self ):
        if hasattr( self.notifier, 'object' ):
            return self.notifier.object()

        return None

    def _get_object_id ( self ):
        if self._object_id is None:
            self._object_id = ''
            if hasattr( self.notifier, 'object' ):
                self._object_id = '0x%08X' % id( self.notifier.object() )

        return self._object_id

    def _get_module_name ( self ):
        if self._module_name is None:
            self._module_name = splitext( basename( self.file_name ) )[0]

        return self._module_name

    def _get_method_name ( self ):
        if self._method_name is None:
            self._method_name = self.handler.__name__

        return self._method_name

    def _get_line ( self ):
        if self._line is None:
            handler = self.handler
            if hasattr( handler, 'im_func' ):
                handler = handler.im_func
            self._line = handler.func_code.co_firstlineno

        return self._line

    def _get_file_name ( self ):
        if self._file_name is None:
            handler = self.handler
            if hasattr( handler, 'im_func' ):
                handler = handler.im_func
            self._file_name = handler.func_code.co_filename

        return self._file_name

    def _get_source ( self ):
        if self._source is None:
            self._source = ''
            source       = read_file( self.file_name )
            if source is not None:
                try:
                    self._source = source.split( '\n' )[ self.line - 1 ].strip()
                except:
                    pass

        return self._source

    def _get_handler ( self ):
        notifier = self.notifier
        if hasattr( notifier, 'object' ):
            return getattr( notifier.object(), notifier.name )

        return notifier.handler

#-------------------------------------------------------------------------------
#  Listener table editor definition:
#-------------------------------------------------------------------------------

listener_table_editor = TableEditor(
    columns            = [ ObjectColumn( name     = 'class_name',
                                         label    = 'Class Name',
                                         editable = False ),
                           ObjectColumn( name     = 'object_id',
                                         label    = 'Object Id',
                                         editable = False,
                                         horizontal_alignment = 'center' ),
                           ObjectColumn( name     = 'module_name',
                                         label    = 'Module Name',
                                         editable = False ),
                           ObjectColumn( name     = 'method_name',
                                         label    = 'Method Name',
                                         editable = False ),
                           ObjectColumn( name     = 'line',
                                         editable = False,
                                         horizontal_alignment = 'center' ),
                           ObjectColumn( name     = 'file_name',
                                         label    = 'File Name',
                                         editable = False ),
                           ObjectColumn( name     = 'source',
                                         editable = False ) ],
    other_columns      = [ ],
    auto_size          = False,
    selection_bg_color = 0xFBD391,
    selection_color    = 'black',
    selected           = 'selected'
)

#-------------------------------------------------------------------------------
#  'Listener' class:
#-------------------------------------------------------------------------------

class Listener ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'Listener' )

    # The receiver of the trait whose listeners are to be displayed:
    trait_value = TraitValue(
                      droppable = 'Drop a trait here to display its listeners',
                      connect   = 'to: trait' )

    # The currently selected entry's file position:
    file_position = Instance( FilePosition,
                              draggable = 'Drag this file position.',
                              connect   = 'from: file position' )

    # The currently selected entry's object:
    object = Property( draggable = 'Drag this object.' )

    # The list of listener items for the current trait being inspected:
    items = List( ListenerItem )

    # The currently selected listener item:
    selected = Instance( ListenerItem )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        Item( 'items',
              id         = 'items',
              show_label = False,
              editor     = listener_table_editor
        ),
        id = 'etsdevtools.developer.tools.listener'
    )

    #---------------------------------------------------------------------------
    #  Implementation of the 'object' property:
    #---------------------------------------------------------------------------

    def _get_object ( self ):
        if self.selected is not None:
            return self.selected.object

        return None

    #---------------------------------------------------------------------------
    #  Handles the 'selected' trait being changed:
    #---------------------------------------------------------------------------

    def _selected_changed ( self, selected ):
        """ Handles the 'selected' trait being changed.
        """
        self.file_position = FilePosition( file_name = selected.file_name,
                                           name      = selected.method_name,
                                           line      = selected.line )

    #---------------------------------------------------------------------------
    #  Handles the 'trait_value' trait being changed:
    #---------------------------------------------------------------------------

    def _trait_value_changed ( self, trait_value ):
        """ Handles the 'trait_value' trait being changed.
        """
        object, name = trait_value
        notifiers    = object._notifiers( 1 )[:]
        notifiers.extend( object._trait( name, 2 )._notifiers( 1 ) )
        self.items = [ ListenerItem( notifier = notifier )
                       for notifier in notifiers ]

#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

view = Listener()

