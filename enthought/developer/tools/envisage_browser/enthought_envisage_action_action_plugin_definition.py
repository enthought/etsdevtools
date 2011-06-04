#-------------------------------------------------------------------------------
#
#  Extension point adapters for ExtensionPoint subclasses defined in:
#  - envisage.action.action_plugin_definition.py
#
#  Written by: David C. Morrill
#
#  Date: 06/17/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

"""Copyright 2006 by David C. Morrill"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from traitsui.api \
    import VGroup, HGroup, Item

from enthought.developer.tools.envisage_browser.object_adapter \
    import Export

from enthought.developer.tools.envisage_browser.extension_point_adapter \
    import ExtensionPointAdapter

#-------------------------------------------------------------------------------
#  'ActionSetAdapter' class:
#-------------------------------------------------------------------------------

class ActionSetAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    id   = Export
    name = Export

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VGroup(
                  Item( 'name~' ),
                  Item( 'id~' ),
                  label       = 'Description',
                  show_border = True
              )

#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_children ( self ):
        """ Returns the unadapted extension points immediately contained within
            this one.
        """
        return self.adaptee.actions + self.adaptee.groups + self.adaptee.menus

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'id' ]

#-------------------------------------------------------------------------------
#  'ActionAdapter' class:
#-------------------------------------------------------------------------------

class ActionAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    id            = Export
    name          = Export
    accelerator   = Export
    checked       = Export
    description   = Export
    enabled       = Export
    image         = Export
    style         = Export
    tooltip       = Export
    class_name    = Export
    lazy_load     = Export
    function_name = Export
    method_name   = Export
    object        = Export

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VGroup(
                  VGroup(
                      Item( 'name~' ),
                      Item( 'id~' ),
                      Item( 'class_name~' ),
                      Item( 'description~' ),
                      Item( 'tooltip~' ),
                      label       = 'Description',
                      show_border = True
                  ),
                  VGroup(
                      Item( 'object~' ),
                      Item( 'method_name~' ),
                      Item( 'function_name~' ),
                      label       = 'Action',
                      show_border = True
                  ),
                  VGroup(
                      Item( 'image~' ),
                      Item( 'accelerator~' ),
                      HGroup(
                          Item( 'style~',     width = -80 ), '_',
                          Item( 'checked~',   width = -40 ),
                          Item( 'enabled~',   width = -40 ),
                          Item( 'lazy_load~', width = -40 )
                      ),
                      label       = 'Options',
                      show_border = True
                  )
              )

#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_children ( self ):
        """ Returns the unadapted extension points immediately contained within
            this one.
        """
        result = self.adaptee.locations[:]

        if self.adaptee.enabled_when is not None:
            result.append( self.adaptee.enabled_when )

        if self.adaptee.disabled_when is not None:
            result.append( self.adaptee.disabled_when )

        return result

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'id', '*accelerator', '*checked', 'description', '*enabled',
                 '*image', '*style', '*tooltip', 'class_name', '*lazy_load',
                 '*function_name', '*method_name', '*object' ]

#-------------------------------------------------------------------------------
#  'LocationAdapter' class:
#-------------------------------------------------------------------------------

class LocationAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    path   = Export
    after  = Export
    before = Export

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VGroup(
                  Item( 'path~' ),
                  Item( 'after~' ),
                  Item( 'before~' ),
                  label       = 'Description',
                  show_border = True
              )

#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'path', 'after', 'before' ]

#-------------------------------------------------------------------------------
#  'GroupAdapter' class:
#-------------------------------------------------------------------------------

class GroupAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    id         = Export
    class_name = Export
    separator  = Export

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VGroup(
                  Item( 'id~' ),
                  Item( 'class_name~' ),
                  Item( 'separator~', width = -40 ),
                  label       = 'Description',
                  show_border = True
              )

#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_children ( self ):
        """ Returns the unadapted extension points immediately contained within
            this one.
        """
        if self.adaptee.location is not None:
            return [ self.adaptee.location ]

        return []

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'id', 'class_name', 'separator' ]

#-------------------------------------------------------------------------------
#  'MenuAdapter' class:
#-------------------------------------------------------------------------------

class MenuAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    name       = Export
    id         = Export
    class_name = Export

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VGroup(
                  Item( 'name~' ),
                  Item( 'id~' ),
                  Item( 'class_name~' ),
                  label       = 'Description',
                  show_border = True
              )

#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_children ( self ):
        """ Returns the unadapted extension points immediately contained within
            this one.
        """
        result = self.adaptee.groups[:]

        if self.adaptee.location is not None:
            result.append( self.adaptee.location )

        return result

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'name', 'id', 'class_name' ]


#-------------------------------------------------------------------------------
#  'EnabledWhenAdapter' class:
#-------------------------------------------------------------------------------

class EnabledWhenAdapter ( ExtensionPointAdapter ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    cookie        = Export
    parent_cookie = Export
    resource_type = Export

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    content = VGroup(
                  Item( 'cookie~' ),
                  Item( 'parent_cookie~' ),
                  Item( 'resource_type~' ),
                  label       = 'Description',
                  show_border = True
              )

#-- ExtensionPointAdapter Overrides --------------------------------------------

    def get_names ( self ):
        """ Returns the list of trait names for the extension point.
        """
        return [ 'cookie', 'parent_cookie', 'resource_type' ]

#-------------------------------------------------------------------------------
#  'DisabledWhenAdapter' class:
#-------------------------------------------------------------------------------

class DisabledWhenAdapter ( EnabledWhenAdapter ): pass

