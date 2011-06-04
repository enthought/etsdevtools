#-------------------------------------------------------------------------------
#
#  Feature-based plugin base class for managing lists of viewable objects.
#
#  Written by: David C. Morrill
#
#  Date: 02/21/2007
#
#  (c) Copyright 2007 by Enthought, Inc.
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from traits.api \
    import HasPrivateTraits, HasStrictTraits, Instance, Str, List, Constant, \
           Any

from traitsui.api \
    import View, Item, ListEditor

from traitsui.menu \
    import NoButtons

from etsdevtools.developer.features.api \
    import CustomFeature, is_not_none

from etsdevtools.developer.features.connect_feature \
    import can_connect

from pyface.image_resource \
    import ImageResource

#-------------------------------------------------------------------------------
#  'ObjectListView' class:
#-------------------------------------------------------------------------------

class ObjectListView ( HasPrivateTraits ):

    #-- Trait Definitions ------------------------------------------------------

    # The class contained in the list:
    klass = Any

    # The list of all current objects:
    objects_list = List

    # The currently selected object:
    selected_object = Any

    # The name of the trait incoming/outgoing data is connected to:
    selected_trait = Str

    # Feature button for creating a new shell:
    new_object_button = Instance( CustomFeature, {
                           'image':   ImageResource( 'new_object' ),
                           'click':   '_new_object',
                           'tooltip': 'Click to create a new view.'
                       },
                       custom_feature = True )

    #-- Trait View Definitions -------------------------------------------------

    view = View(
        Item( 'objects_list',
              style      = 'custom',
              show_label = False,
              editor     = ListEditor( use_notebook = True,
                                       deletable    = True,
                                       selected     = 'selected_object',
                                       page_name    = '.name',
                                       export       = 'DockWindowShell',
                                       dock_style   = 'tab' )
        )
    )

    #-- Object Class Methods ---------------------------------------------------

    def __init__ ( self, **traits ):
        """ Initializes the object.
        """
        super( ObjectListView, self ).__init__( **traits )

        selected_trait = None
        traits = self.traits( connect = can_connect )
        if len( traits ) == 1:
            selected_trait, trait = traits.items()[0]
            connect = trait.connect
            col     = connect.find( ':' )
            if col >= 0:
                connect = connect[ : col ].strip()
            if connect == 'both':
                connect = 'to'
        else:
            traits = self.trait_name( droppable = is_not_none )
            if len( traits ) == 1:
                selected_trait = traits[0]
                connect = 'to'
            else:
                traits = self.trait_names( draggable = is_not_none )
                if len( traits ) == 1:
                    selected_trait = traits[0]
                    connect = 'from'

        if selected_trait is not None:
            self.selected_trait = selected_trait
            self.new_object_button.enabled = (connect == 'from')
            if connect == 'to':
                self.on_trait_change( self._new_from_external, selected_trait )
            else:
                self.on_trait_change( self._select_from_external,
                                      selected_trait )
                self._new_object()

    #-- Overridable Methods ----------------------------------------------------

    def new_object ( self, **traits ):
        """ Returns a new object to be viewed (must be overridden).
        """
        return DefaultObject()

    #-- Feature Event Handlers -------------------------------------------------

    def _new_object ( self, **traits ):
        """ Creates a new view object.
        """
        object = self.new_object( **traits )
        self.objects_list.append( object )
        self.selected_object = object

    def _new_from_external ( self, data ):
        trait = self.selected_trait
        for object in self.objects_list:
            if data == getattr( object, trait ):
                self.selected_object = object
                break
        else:
            self._new_object( **{ self.selected_trait: data } )

    #-- Event Handlers ---------------------------------------------------------

    def _selected_object_default ( self ):
        """ Returns the default value for the 'selected_object' trait.
        """
        if len( self.objects_list ) > 0:
            return self.objects_list[0]

        return None

    def _selected_object_changed ( self, selected ):
        """ Handles the 'selected_object' trait being changed.
        """
        if (selected is not None) and (self.selected_trait != ''):
            setattr( self, self.selected_trait,
                     getattr( selected, self.selected_trait ) )

    def _select_from_external ( self, data ):
        """ Connects externally supplied data to the current selected object.
        """
        if self.selected is not None:
            setattr( self.selected, self.selection_trait, data )
        else:
            self._new_from_external( data )

#-------------------------------------------------------------------------------
#  'DefaultObject' class:
#-------------------------------------------------------------------------------

class DefaultObject ( HasStrictTraits ):

    #-- Trait Definitions ------------------------------------------------------

    message = Constant( "You did not override the 'new_object' method or "
                        "specify a 'klass' value." )

    #-- Traits View Definitions ------------------------------------------------

    view = View( Item( 'message', style = 'readonly', show_label = False ) )

