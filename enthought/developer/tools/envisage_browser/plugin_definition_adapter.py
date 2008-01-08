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
    
from enthought.envisage \
    import ExtensionItem
    
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
    autostart        = Export
    class_name       = Export
    enabled          = Export
    id               = Export
    name             = Export
    provider_name    = Export
    provider_url     = Export
    version          = Export
    
    requires         = Export
    extension_points = Export
    extensions       = Export

    #---------------------------------------------------------------------------
    #  Traits view definitions:    
    #---------------------------------------------------------------------------
    
    view = View(
               Tabbed(
                   VGroup(
                       VGroup(
                           Item( 'name~' ),
                           Item( 'id~' ),
                           Item( 'version~' ),
                           Item( 'provider_name~' ),
                           Item( 'provider_url~' ),
                           label       = 'Description',
                           show_border = True
                       ),
                       VGroup(
                           Item( 'class_name~' ),
                           Item( 'file_name~' ),
                           HGroup( 
                               Item( 'autostart~', width = -40 ),
                               Item( 'enabled~',   width = -40 )
                           ),
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
               
#-- Property Implementations ---------------------------------------------------

    def _get_adapted_required_by ( self ):
        if self._adapted_required_by is None:
            self._adapted_required_by = self.application.get_plugins_using(
                                                                       self.id )
            
        return self._adapted_required_by
        
    def _get_adapted_requires ( self ):
        if self._adapted_requires is None:
            gpf = self.application.get_plugin_for
            self._adapted_requires = [ gpf( id ) for id in self.requires ]
            
        return self._adapted_requires
        
    def _get_adapted_extensions ( self ):
        if self._adapted_extensions is None:
            gef = self.application.get_extension_for
            fn  = self.file_name
            self._adapted_extensions = [ gef( ep, fn ) 
                                         for ep in self.extensions ]
            
        return self._adapted_extensions
        
    def _get_adapted_extensions_all ( self ):
        if self._adapted_extensions_all is None:
            result = self.adapted_extensions[:]
            for extension in self.adapted_extensions:
                result.extend( extension.get_all_children() )
            self._adapted_extensions_all = result
            
        return self._adapted_extensions_all
        
    def _get_extension_points_all ( self ):
        if self._extension_points_all is None:
            items       = []
            module      = self.module
            module_name = module.__name__
            for name in dir( module ):
                item = getattr( module, name )
                try:
                    if (issubclass( item, ExtensionItem ) and
                        (item.__module__ == module_name)):
                        items.append( item )
                except:
                    pass
            
            self._extension_points_all = self.extension_points + items
            
        return self._extension_points_all
        
    def _get_nodes ( self ):
        if self._nodes is None:
            nodes = []
            if len( self.adapted_required_by ) > 0:
                nodes.append( RequiredByAdapter( 
                                  required_by = self.adapted_required_by ) )
                                  
            if len( self.requires ) > 0:
                nodes.append( RequiresAdapter( 
                                  requires = self.adapted_requires ) )
                
            if len( self.extension_points_all ) > 0:
                file_name   = self.file_name
                application = self.application
                nodes.append( ExtensionPointsAdapter( extension_points =
                    [ ExtensionPointClassAdapter( adaptee     = ep,
                                                  file_name   = file_name,
                                                  application = application )
                      for ep in self.extension_points_all ] ) )
                
            if len( self.extensions ) > 0:
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
    
