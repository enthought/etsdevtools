#-------------------------------------------------------------------------------
#
#  Extension point adapters for ExtensionPoint subclasses defined in:
#  - envisage.core.core_plugin_definition.py
#
#  Written by: David C. Morrill
#
#  Date: 06/22/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from traits.api \
    import HasPrivateTraits, Property, Code, Str

from traitsui.api \
    import VGroup, HGroup, Item, TableEditor

from traitsui.table_column \
    import ObjectColumn

from etsdevtools.developer.tools.envisage_browser.object_adapter \
    import Export

from etsdevtools.developer.tools.envisage_browser.extension_point_adapter \
    import ExtensionPointAdapter

#-------------------------------------------------------------------------------
#  'ApplicationObjectAdapter' class:
#-------------------------------------------------------------------------------

class ApplicationObjectAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    factory_class_name = Export
    class_name         = Export
    uol                = Export
    args               = Export
    kw                 = Export
    properties         = Export

    class_name_source         = Property( Code )
    factory_class_name_source = Property( Code )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VGroup(
                  Item( 'uol~' ),
                  Item( 'class_name~' ),
                  Item( 'factory_class_name~' ),
                  Item( 'args{Positional Arguments}~' ),
                  Item( 'kw{Keyword Arguments~' ),
                  Item( 'properties~' ),
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
        return [ 'uol', 'class_name', 'factory_class_name', '*args', '*kw',
                 '*properties' ]

#-- Property Implementations ---------------------------------------------------

    def _get_class_name_source ( self, name ):
        return self._get_class_source( name )

    def _get_factory_class_name_source ( self, name ):
        return self._get_class_source( name )

#-------------------------------------------------------------------------------
#  'AdadpterFactoryAdapter' class:
#-------------------------------------------------------------------------------

class AdadpterFactoryAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    class_name         = Export
    adaptee_class_name = Export
    adapter_class_name = Export
    target_class_name  = Export

    class_name_source         = Property( Code )
    adaptee_class_name_source = Property( Code )
    adapter_class_name_source = Property( Code )
    target_class_name_source  = Property( Code )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VGroup(
                  Item( 'class_name~' ),
                  Item( 'adaptee_class_name~' ),
                  Item( 'adapter_class_name~' ),
                  Item( 'target_class_name~' ),
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
                      Item( 'adaptee_class_name~' ),
                      VGroup(
                          Item( 'adaptee_class_name_source~',
                                show_label = False ),
                      ),
                      label = 'Adaptee Class Source Code',
                      dock  = 'tab',
                      defined_when = "adaptee_class_name_source != ''"
                 )

    extra_page3 = VGroup(
                      Item( 'adapter_class_name~' ),
                      VGroup(
                          Item( 'adapter_class_name_source~',
                                show_label = False ),
                      ),
                      label = 'Adapter Class Source Code',
                      dock  = 'tab',
                      defined_when = "adapter_class_name_source != ''"
                 )

    extra_page4 = VGroup(
                      Item( 'target_class_name~' ),
                      VGroup(
                          Item( 'target_class_name_source~',
                                show_label = False ),
                      ),
                      label = 'Target Class Source Code',
                      dock  = 'tab',
                      defined_when = "target_class_name_source != ''"
                 )

#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'class_name', 'adaptee_class_name', 'adapter_class_name',
                 'target_class_name' ]

#-- Property Implementations ---------------------------------------------------

    def _get_class_name_source ( self, name ):
        return self._get_class_source( name )

    def _get_adaptee_class_name_source ( self, name ):
        return self._get_class_source( name )

    def _get_adapter_class_name_source ( self, name ):
        return self._get_class_source( name )

    def _get_target_class_name_source ( self, name ):
        return self._get_class_source( name )

#-------------------------------------------------------------------------------
#  'CategoryAdapter' class:
#-------------------------------------------------------------------------------

class CategoryAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    class_name        = Export
    target_class_name = Export

    class_name_source        = Property( Code )
    target_class_name_source = Property( Code )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VGroup(
                  Item( 'class_name~' ),
                  Item( 'target_class_name~' ),
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
                      Item( 'target_class_name~' ),
                      VGroup(
                          Item( 'target_class_name_source~',
                                show_label = False ),
                      ),
                      label = 'Target Class Source Code',
                      dock  = 'tab',
                      defined_when = "target_class_name_source != ''"
                 )

#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'class_name', 'target_class_name' ]

#-- Property Implementations ---------------------------------------------------

    def _get_class_name_source ( self, name ):
        return self._get_class_source( name )

    def _get_target_class_name_source ( self, name ):
        return self._get_class_source( name )

#-------------------------------------------------------------------------------
#  'HookAdapter' class:
#-------------------------------------------------------------------------------

class HookAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    callable_name      = Export
    target_class_name  = Export
    target_method_name = Export
    type               = Export

    target_class_name_source = Property( Code )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VGroup(
                  Item( 'callable_name~' ),
                  Item( 'target_class_name~' ),
                  Item( 'target_method_name~' ),
                  Item( 'type~' ),
                  label       = 'Description',
                  show_border = True
              )

    extra_page = VGroup(
                     Item( 'target_class_name~' ),
                     VGroup(
                         Item( 'target_class_name_source~',
                               show_label = False ),
                     ),
                     label = 'Target Class Source Code',
                     dock  = 'tab',
                     defined_when = "target_class_name_source != ''"
                )

#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'callable_name', 'target_class_name', 'target_method_name',
                 'type' ]

#-- Property Implementations ---------------------------------------------------

    def _get_target_class_name_source ( self, name ):
        return self._get_class_source( name )

#-------------------------------------------------------------------------------
#  'TypeManagerAdapter' class:
#-------------------------------------------------------------------------------

class TypeManagerAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    id                = Export
    adapter_factories = Export
    categories        = Export
    hooks             = Export
    parent            = Export

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VGroup(
                  Item( 'id~' ),
                  Item( 'parent~' ),
                  label       = 'Description',
                  show_border = True
              )

#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_children ( self ):
        """ Returns the unadapted extension points immediately contained within
            this one.
        """
        return (self.adaptee.adapter_factories + self.adaptee.categories +
                self.adaptee.hooks)

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'id', '*adapter_factories', '*categories', '*hooks', 'parent' ]

#-------------------------------------------------------------------------------
#  Defaults table editor definition:
#-------------------------------------------------------------------------------

defaults_table_editor = TableEditor(
    columns  = [ ObjectColumn( name = 'name',  width = 0.20 ),
                 ObjectColumn( name = 'value', width = 0.77 ) ],
    editable = False
)

#-------------------------------------------------------------------------------
#  'PreferencesAdapter' class:
#-------------------------------------------------------------------------------

class PreferencesAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    defaults = Export

    defaults_list = Property

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VGroup(
                  Item( 'defaults_list~',
                        show_label = False,
                        dock       = 'tab',
                        editor     = defaults_table_editor
                  ),
                  label       = 'Description',
                  show_border = True
              )

#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ '*defaults' ]

#-- Property Implementations ---------------------------------------------------

    def _get_defaults_list ( self ):
        if self._defaults_list is None:
            self._defaults_list = [ PreferenceItem( name  = name,
                                                    value = str( value ) )
                                    for name, value in self.defaults.items() ]
        return self._defaults_list

#-------------------------------------------------------------------------------
#  'PreferenceItem' class:
#-------------------------------------------------------------------------------

class PreferenceItem ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    name  = Str
    value = Str

#-------------------------------------------------------------------------------
#  'RunnableAdapter' class:
#-------------------------------------------------------------------------------

class RunnableAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    class_name = Export

    class_name_source = Property( Code )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VGroup(
                  Item( 'class_name~' ),
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
        return [ 'class_name' ]

#-- Property Implementations ---------------------------------------------------

    def _get_class_name_source ( self, name ):
        return self._get_class_source( name )

