#-------------------------------------------------------------------------------
#  
#  Defines the PluginDefinitionAdapter class for adapting Envisage
#  PluginDefinition objects for use with the Envisage plugin browser.
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

from enthought.traits.api \
    import HasPrivateTraits, List, Any, Property

from enthought.traits.ui.api \
    import View, VGroup, HGroup, Tabbed, Item
    
from enthought.traits.ui.menu \
    import NoButtons
    
from enthought.developer.tools.envisage_browser.object_adapter \
    import ObjectAdapter, Export
    
from enthought.developer.tools.envisage_browser.extension_point_adapter \
    import ExtensionPointClassAdapter

#-------------------------------------------------------------------------------
#  'PluginDefinitionAdapter' class:
#-------------------------------------------------------------------------------

class PluginDefinitionAdapter ( ObjectAdapter ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:    
    #---------------------------------------------------------------------------
    
    # The module the associated plugin was defined in:
    module = Any
    
    # The list of plugins that require this one (adapted version):
    adapted_required_by = Property( List )
    
    # The list of required plugins (adapted version):
    adapted_requires = Property( List )
    
    # The list of exported extensions (adapted version):
    adapted_extensions = Property( List )
    
    # The list of all exported extensions (including children)(adapted version):
    adapted_extensions_all = Property( List )
    
    # List of all extension points (including ExtensionItem's):
    extension_points_all = Property( List )
    
    # The child nodes for the tree view:
    nodes = Property( List )
    
    # Re-exported PluginDefinition traits:    
    activator        = Export
    id               = Export
    name             = Export

    #---------------------------------------------------------------------------
    #  Traits view definitions:    
    #---------------------------------------------------------------------------
    
    view = View(
               Tabbed(
                   VGroup(
                       VGroup(
                           Item( 'name~' ),
                           Item( 'id~' ),
                           label       = 'Description',
                           show_border = True
                       ),
                       VGroup(
                           Item( 'application~' ),
                           label       = 'Implementation',
                           show_border = True,
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
               id        = 'enthought.developer.envisage_browser.'
                           'plugin_definition_adapter.PluginDefinitionAdapter',
               title     = 'Plugin Definition',
               resizable = True,
               buttons   = NoButtons
           )
               
#-- Property Implementations -------------------------------------------------

    def _get_adapted_extensions ( self ):
        if self._adapted_extensions is None:
            self._adapted_extensions = []
            gef = self.application.get_extension_for
            fn  = self.file_name    
            for trait_name in self.adaptee.trait_names():
                trait = self.adaptee.trait(trait_name)
                ep_id = getattr(trait, 'contributes_to') 
                if ep_id is not None:
                    self._adapted_extensions.extend(gef(ep, fn) for ep in 
                          self.adaptee.get_extensions(ep_id))
            
        return self._adapted_extensions
        
    def _get_adapted_extensions_all ( self ):
        if self._adapted_extensions_all is None:
            result = self.adapted_extensions[:]
            for extension in self.adapted_extensions:
                result.extend( extension.get_all_children() )
            self._adapted_extensions_all = result
            
        return self._adapted_extensions_all
        
    def _get_extension_points_all ( self ):
        # if self._extension_points_all is None:
        #    items       = []
        #    module      = self.module
        #    module_name = module.__name__
        #    for name in dir( module ):
        #        item = getattr( module, name )
        #        try:
        #            if (issubclass( item, ExtensionItem ) and
        #                (item.__module__ == module_name)):
        #                items.append( item )
        #        except:
        #            pass
        #
        #    self._extension_points_all = self.extension_points + items
        #    
        # return self._extension_points_all
        return self.adaptee.get_extension_points()

    def _get_nodes ( self ):
        if self._nodes is None:
            nodes = []
            if len( self.extension_points_all ) > 0:
                file_name   = self.file_name
                application = self.application
                nodes.append( ExtensionPointsAdapter( extension_points =
                    [ ExtensionPointClassAdapter( adaptee     = ep,
                                                  file_name   = file_name,
                                                  application = application )
                      for ep in self.extension_points_all ] ) )
                
            if len( self.adapted_extensions ) > 0:
                nodes.append( ExtensionsAdapter( 
                                  extensions = self.adapted_extensions ) )
                
            self._nodes = nodes
            
        return self._nodes
        
#-------------------------------------------------------------------------------
#  'RequiredByAdapter' class:  
#-------------------------------------------------------------------------------
                
class RequiredByAdapter ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
    
    required_by = List
        
#-------------------------------------------------------------------------------
#  'RequiresAdapter' class:  
#-------------------------------------------------------------------------------
                
class RequiresAdapter ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
    
    requires = List
    
#-------------------------------------------------------------------------------
#  'ExtensionPointsAdapter' class:
#-------------------------------------------------------------------------------

class ExtensionPointsAdapter ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Traits definitions:  
    #---------------------------------------------------------------------------

    extension_points = List

#-------------------------------------------------------------------------------
#  'ExtensionsAdapter' class:
#-------------------------------------------------------------------------------

class ExtensionsAdapter ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Traits definitions:  
    #---------------------------------------------------------------------------

    extensions = List
    
