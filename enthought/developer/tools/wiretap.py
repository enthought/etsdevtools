#-------------------------------------------------------------------------------
#
#  FBI Wiretap plugin
#
#  Written by: David C. Morrill
#
#  Date: 07/17/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasTraits, HasPrivateTraits, Instance, Str, List, false

from enthought.traits.ui.api \
    import View, Item, TableEditor

from enthought.traits.ui.table_column \
    import ObjectColumn

from enthought.traits.ui.value_tree \
    import SingleValueTreeNodeObject, TraitsNode

from enthought.pyface.image_resource \
    import ImageResource

from enthought.developer.features.api \
    import CustomFeature

from enthought.developer.helper.fbi \
    import fbi_wiretap

#-------------------------------------------------------------------------------
#  'WiretapItem' class:
#-------------------------------------------------------------------------------

class WiretapItem ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The object being wiretapped:
    object = Instance( HasTraits )

    # The trait being wiretapped:
    name = Str

    # The condition (if any) for the wiretap:
    condition = Str

    # Wiretap entire object?
    entire_object = false

    #---------------------------------------------------------------------------
    #  Adds the wiretap:
    #---------------------------------------------------------------------------

    def add ( self ):
        """ Adds the wiretap.
        """
        fbi_wiretap.wiretap( ( self.object, self.name, self.condition ), False )

    #---------------------------------------------------------------------------
    #  Removes the wiretap:
    #---------------------------------------------------------------------------

    def remove ( self ):
        """ Removes the wiretap.
        """
        fbi_wiretap.wiretap( ( self.object, self.name, self.condition ), True )

    #---------------------------------------------------------------------------
    #  Handles the 'condition' trait being changed:
    #---------------------------------------------------------------------------

    def _condition_changed ( self, old, new ):
        """ Handles the 'condition' trait being changed.
        """
        fbi_wiretap.wiretap( ( self.object, self.name, old ), True )
        fbi_wiretap.wiretap( ( self.object, self.name, new ), False )

    #---------------------------------------------------------------------------
    #  Handles the 'entire_object' trait being changed:
    #---------------------------------------------------------------------------

    def _entire_object_changed ( self, state ):
        """ Handles the 'entire_object' trait being changed.
        """
        if state:
            fbi_wiretap.wiretap( ( self.object, self.name, self.condition ),
                                 True )
            fbi_wiretap.wiretap( ( self.object, None, self.condition ), False )
            self._name, self.name = self.name, ''
        else:
            self.name = self._name
            fbi_wiretap.wiretap( ( self.object, None, self.condition ), True )
            fbi_wiretap.wiretap( ( self.object, self.name, self.condition ),
                                 False )

#-------------------------------------------------------------------------------
#  Wiretap table editor definition:
#-------------------------------------------------------------------------------

wiretap_table_editor = TableEditor(
    columns = [ ObjectColumn( name     = 'entire_object' ),
                ObjectColumn( name     = 'object',
                              editable = False ),
                ObjectColumn( name     = 'name',
                              editable = False ),
                ObjectColumn( name     = 'condition' ) ],
    deletable          = True,
    configurable       = False,
    auto_size          = False,
    selection_bg_color = 0xFBD391,
    selection_color    = 'black'
)

#-------------------------------------------------------------------------------
#  'Wiretap' plugin:
#-------------------------------------------------------------------------------

class Wiretap ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'Wiretap' )

    feature = Instance( CustomFeature, {
                            'image':    ImageResource( 'drop' ),
                            'can_drop': 'can_drop',
                            'drop':     'drop',
                            'tooltip':  'Drop a trait value here to wiretap '
                                        'it.'
                        },
                        custom_feature = True )

    # The current list of wiretap items:
    wiretaps = List( WiretapItem )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        Item( 'wiretaps',
              id         = 'wiretap',
              show_label = False,
              editor     = wiretap_table_editor
        ),
        id = 'enthought.developer.tools.wiretap'
    )

    #---------------------------------------------------------------------------
    #  Returns whether a specified item can be dropped on the view:
    #---------------------------------------------------------------------------

    def can_drop ( self, item ):
        """ Returns whether a specified item can be dropped on the view.
        """
        if (isinstance( item, SingleValueTreeNodeObject ) and
              isinstance( item.parent, TraitsNode )):
            name   = item.name[1:]
            object = item.parent.value
            for wiretap in self.wiretaps:
                if (object is wiretap.object) and (name == wiretap.name):
                    return False
            return True
        return False

    #---------------------------------------------------------------------------
    #  Handles a specified item being dropped on the view:
    #---------------------------------------------------------------------------

    def drop ( self, item ):
        """ Handles a specified item being dropped on the view.
        """
        name    = item.name[1:]
        object  = item.parent.value
        wiretap = WiretapItem( object = object, name = name )
        self.wiretaps.append( wiretap )
        wiretap.add()

    #---------------------------------------------------------------------------
    #  Handles wiretap items being deleted from the table:
    #---------------------------------------------------------------------------

    def _wiretaps_items_changed ( self, event ):
        """ Handles a wiretap item being deleted from the table.
        """
        for wiretap in event.removed:
            wiretap.remove()

#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

view = Wiretap()

