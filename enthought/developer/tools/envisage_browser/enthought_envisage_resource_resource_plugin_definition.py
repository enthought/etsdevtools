#-------------------------------------------------------------------------------
#
#  Extension point adapters for ExtensionPoint subclasses defined in:
#  - envisage.resource.resource_plugin_definition.py
#
#  Written by: David C. Morrill
#
#  Date: 06/21/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from traits.api \
    import HasPrivateTraits, Str, Code, Property


from traitsui.api \
    import VGroup, HGroup, Item, TableEditor

from traitsui.table_column \
    import ObjectColumn

from enthought.developer.tools.envisage_browser.object_adapter \
    import Export

from enthought.developer.tools.envisage_browser.extension_point_adapter \
    import ExtensionPointAdapter

#-------------------------------------------------------------------------------
#  Precedes table editor definition:
#-------------------------------------------------------------------------------

precedes_table_editor = TableEditor(
    columns  = [ ObjectColumn( name = 'precedes',  width = 0.97 ) ],
    editable = False
)

#-------------------------------------------------------------------------------
#  'ResourceManagerAdapter' class:
#-------------------------------------------------------------------------------

class ResourceManagerAdapter ( ExtensionPointAdapter ):

#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_children ( self ):
        """ Returns the unadapted extension points immediately contained within
            this one.
        """
        return self.adaptee.resource_types

#-------------------------------------------------------------------------------
#  'ResourceViewAdapter' class:
#-------------------------------------------------------------------------------

class ResourceViewAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    id            = Export
    class_name    = Export
    resource_type = Export

    class_name_source = Property( Code )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VGroup(
                  Item( 'id~' ),
                  Item( 'class_name~' ),
                  Item( 'resource_type~' ),
                  label       = 'Description',
                  show_border = True
              )

    extra_page = VGroup(
                     Item( 'class_name~' ),
                     VGroup(
                         Item( 'class_name_source~', show_label = False ),
                     ),
                     label = 'Class Source Code',
                     dock  = 'tab',
                     defined_when = "class_name_source != ''"
                 )

#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'id', 'class_name', 'resource_type' ]

#-- Property Implementations ---------------------------------------------------

    def _get_class_name_source ( self, name ):
        return self._get_class_source( name )

#-------------------------------------------------------------------------------
#  'ResourceTypeAdapter' class:
#-------------------------------------------------------------------------------

class ResourceTypeAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    class_name         = Export
    factory_class_name = Export
    precedes           = Export

    precedes_list      = Property

    class_name_source         = Property( Code )
    factory_class_name_source = Property( Code )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VGroup(
                  Item( 'class_name~' ),
                  Item( 'factory_class_name~' ),
                  VGroup(
                      Item( 'precedes_list~',
                            show_label = False,
                            editor     = precedes_table_editor
                      )
                  ),
                  label       = 'Description',
                  show_border = True
              )

    extra_page = VGroup(
                     Item( 'class_name~' ),
                     VGroup(
                         Item( 'class_name_source~', show_label = False ),
                     ),
                     label = 'Class Source Code',
                     dock  = 'tab',
                     defined_when = "class_name_source != ''"
                 )

    extra_page2 = VGroup(
                      Item( 'factory_class_name~' ),
                      VGroup(
                          Item( 'factory_class_name_source~',
                                show_label = False ),
                      ),
                      label = 'Factory Class Source Code',
                      dock  = 'tab',
                      defined_when = "factory_class_name_source != ''"
                 )

#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'class_name', 'factory_class_name', 'precedes' ]

#-- Property Implementations ---------------------------------------------------

    def _get_precedes_list ( self ):
        if self._precedes_list is None:
            self._precedes_list = [ Precedes( precedes = precedes )
                                    for precedes in self.precedes ]
        return self._precedes_list

    def _get_class_name_source ( self, name ):
        return self._get_class_source( name )

    def _get_factory_class_name_source ( self, name ):
        return self._get_class_source( name )

#-------------------------------------------------------------------------------
#  'Precedes' class:
#-------------------------------------------------------------------------------

class Precedes ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    precedes = Str

