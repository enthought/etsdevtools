#-------------------------------------------------------------------------------
#  
#  Defines an ImageLibrary LibraryManager for managing changes made to images
#  stored in an ImageLibrary ImageVolume.
#  
#  Written by: David C. Morrill
#  
#  Date: 12/01/2007
#  
#  (c) Copyright 2007 by Enthought, Inc.
#  
#-------------------------------------------------------------------------------

""" Defines an ImageLibrary LibraryManager for managing changes made to images
    stored in an ImageLibrary ImageVolume.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasPrivateTraits, Instance, Int, Bool, List, Event, Button, \
           Property, on_trait_change, cached_property
    
from enthought.traits.ui.api \
    import View, HGroup, Item, Theme, spring
    
from enthought.traits.ui.ui_traits \
    import Image
    
from enthought.traits.ui.image \
    import ImageLibrary, ImageVolume, ImageInfo
    
from enthought.traits.ui.wx.themed_vertical_notebook_editor \
    import ThemedVerticalNotebookEditor
    
from enthought.traits.ui.wx.extra.tabular_editor \
    import TabularEditor, TabularAdapter
    
#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------    

# The 'on_trait_change' listener pattern used by the ImageManager:
image_listener = ('image:[name,description,category,keywords,copyright,'
                  'license,theme:[border.-,content.-,label.-,alignment]]')

#-------------------------------------------------------------------------------
#  'ImageManager' class:  
#-------------------------------------------------------------------------------    

class ImageManager ( HasPrivateTraits ):
    
    # The library image being managed:
    image = Instance( ImageInfo )
    
    # The number of active references to the image:
    count = Int( 1 )
    
    # Has the image been modified in any way?
    modified = Bool( False )
    
    #-- Traits Event Handlers --------------------------------------------------
    
    @on_trait_change( image_listener )
    def _image_modified ( self, object, name, old, new ):
        """ Handles some key part of the image object being modified.
        """
        self.modified = True
        
#-------------------------------------------------------------------------------
#  'VolumeManagerAdapter' class:
#-------------------------------------------------------------------------------

class VolumeManagerAdapter ( TabularAdapter ):
    """ TabularEditor adapter for use with the VolumeManager view.
    """
    # The table columns:
    columns = [ ( 'Image Name', 'image' ) ]
    
    # Adapter properties:
    text  = Property
    image = Property
    
    # Image definitions:
    alert_image = Image( '@ui:alert16' )
    
    #-- Property Implementations -----------------------------------------------
    
    def _get_text ( self):
        return self.item.image.image_name
        
    def _get_image ( self ):
        if self.item.modified:
            return self.alert_image
            
        return None
    
#-------------------------------------------------------------------------------
#  'VolumeManager' class:
#-------------------------------------------------------------------------------

class VolumeManager ( HasPrivateTraits ):
    
    # The image volume being managed:
    volume = Instance( ImageVolume )
    
    # The list of images currently being managed:
    images = List( ImageManager )
    
    # The name of the volume:
    name = Property( depends_on = 'volume' )
    
    # Does the volume have any modified images?
    has_modified = Property( depends_on = 'images.modified' )
    
    # Is the volume empty (i.e. does it have no active images)?
    is_empty = Property( depends_on = 'images' )
    
    # Event fired when the contents of the 'images' view needs to be updated:
    update = Event( on_trait_change = 'images:modified' )
    
    # Button used to save the contents of the volume:
    save = Button( 'Save' )
    
    #-- Traits View Definitions ------------------------------------------------
    
    view = View(
        Item( 'images',
              show_label = False,
              editor     = TabularEditor( 
                               update           = 'update',
                               adapter          = VolumeManagerAdapter(),
                               horizontal_lines = False,
                               operations       = [] )
        ),
        HGroup( 
            spring,
            Item( 'save', 
                  show_label   = False,
                  enabled_when = 'has_modified'
            )
        )
    )
    
    #-- Public methods ---------------------------------------------------------
    
    def add ( self, image ):
        """ Adds a specified *image* **ImageInfo** object to the volume
            manager's collection.
        """
        im = self._find( image )
        if im is not None:
            im.count += 1
            return
                
        self.images.append( ImageManager( image = image ) )
        
    def remove ( self, image ):
        """ Removes a reference to a specified *image* **ImageInfo** object from
            the volume manager's collection.
        """
        im = self._find( image )
        if (im is not None) and (im.count > 0):
            im.count -= 1
            if (im.count == 0) and (not im.modified):
                self.images.remove( im )
                
    #-- Property Implementations -----------------------------------------------
    
    def _get_name ( self ):
        return self.volume.name

    @cached_property
    def _get_has_modified ( self ):
        for image in self.images:
            if image.modified:
                return True
                
        return False
        
    def _get_is_empty ( self ):
        return (len( self.images ) == 0)
        
    #-- Traits Event Handlers --------------------------------------------------
    
    def _save_changed ( self ):
        """ Handles the user clicking the 'Save' button.
        """
        self.volume.save()
        images = self.images
        for image in images[:]:
            image.modified = False
            if image.count == 0:
                images.remove( image )
        
    #-- Private Methods --------------------------------------------------------
    
    def _find ( self, image ):
        """ Attempts to return the **ImageManager** object corresponding to a
            specified *image **ImageInfo** object.
        """
        for im in self.images:
            if image is im.image:
                return im
                
        return None
    
#-------------------------------------------------------------------------------
#  'LibraryManager' class:
#-------------------------------------------------------------------------------    

class LibraryManager ( HasPrivateTraits ):
    
    # The list of image volumes currently being managed:
    volumes = List( VolumeManager )
    
    #-- Traits View Defnitions -------------------------------------------------
    
    view = View(
        Item( 'volumes',
              show_label = False,
              editor     = ThemedVerticalNotebookEditor(
                  closed_theme  = Theme( '@images:GL5', 
                                         content   = ( 0, 0, -2, 0 ), 
                                         alignment = 'center' ),
                  open_theme    = '@ui:GL5TB', 
                  multiple_open = True,
                  scrollable    = True,
                  double_click  = False,
                  page_name     = '.name'
              ),
              item_theme = '@images:XG1'
        )
    )
    
    #-- Public Methods ---------------------------------------------------------
    
    def add ( self, image ):
        """ Adds a specified *image* **ImageInfo** object to the library
            manager's collection.
        """
        vm = self._find( image )
        if not isinstance( vm, VolumeManager ):
            vm = VolumeManager( volume = vm )
            self.volumes.append( vm )
                
        vm.add( image )
        
    def remove ( self, image ):
        """ Removes a reference to a specified *image* **ImageInfo** object from
            the library manager's collection.
        """
        vm = self._find( image )
        if isinstance( vm, VolumeManager ):
            vm.remove( image )
                
    #-- Traits Event Handlers --------------------------------------------------
    
    @on_trait_change( 'volumes:is_empty' )
    def _volume_empty ( self, volume, name, old, empty ):
        """ Handles a VolumeManager becoming empty.
        """
        if empty:
            self.volumes.remove( volume )
                
    #-- Private Methods --------------------------------------------------------
    
    def _find ( self, image ):
        """ Attempts to return the **ImageVolume** object corresponding to a
            specified *image **ImageInfo** object.
        """
        volume = ImageLibrary.find_volume( image.image_name )
        for vm in self.volumes:
            if volume is vm.volume:
                return vm
                
        return volume

# Create the library manager object:        
LibraryManager = LibraryManager()        
