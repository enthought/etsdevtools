#-------------------------------------------------------------------------------
#
#  A feature-enabled tool for viewing the contents of the Traits image library.
#
#  Written by: David C. Morrill
#
#  Date: 11/07/2007
#
#  (c) Copright 2007 by Enthought, Inc.
#
#-------------------------------------------------------------------------------

""" A feature-enabled tool for viewing the contents of the Traits image library.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from os.path \
    import isdir, basename

from enthought.traits.api \
    import HasPrivateTraits, Str, List, File, Directory, Constant, Instance, \
           Int, Property, TraitType, TraitError, cached_property

from enthought.traits.ui.api \
    import View, VGroup, HGroup, Item, TableEditor, UIInfo, Handler, spring

from enthought.traits.ui.table_column \
    import ObjectColumn

from enthought.traits.ui.table_filter \
    import TableFilter

from enthought.traits.ui.image.image \
    import ImageLibrary, ImageInfo

from enthought.traits.ui.key_bindings \
    import KeyBindings, KeyBinding

from enthought.developer.features.api \
    import DropFile

from enthought.developer.helper.traits \
    import Size

from image_browser \
    import ImageItem

# fixme: We need to add a toolkit independent version of the clipboard...
from enthought.util.wx.clipboard \
    import clipboard

#-------------------------------------------------------------------------------
#  Table editor pop-up views:
#-------------------------------------------------------------------------------

class ImageHandler ( Handler ):

    # The UIInfo object for the view:
    info = Instance( UIInfo )

    # The image we want to display:
    image = Instance( ImageItem )

    def init_info ( self, info ):
        self.info = info

    def _image_default ( self ):
        object = self.info.object
        return ImageItem( name = object.image_name, image = object.image_name )

image_view = View(
    Item( 'handler.image', style = 'custom', show_label = False ),
    kind    = 'info',
    handler = ImageHandler
)

description_view = View(
    Item( 'description', style = 'readonly', show_label = False ),
    kind       = 'info',
    width      = 0.20,
    height     = 0.20,
    resizable  = True,
    scrollable = True
)

copyright_view = View(
    Item( 'copyright', style = 'readonly', show_label = False ),
    kind       = 'info',
    width      = 0.20,
    height     = 0.20,
    resizable  = True,
    scrollable = True
)

license_view = View(
    Item( 'license', style = 'readonly', show_label = False ),
    kind       = 'info',
    width      = 0.20,
    height     = 0.20,
    resizable  = True,
    scrollable = True
)

#-------------------------------------------------------------------------------
#  Image library viewer table editor definition:
#-------------------------------------------------------------------------------

class LibraryColumn ( ObjectColumn ):

    editable = False

class NameColumn ( LibraryColumn ):

    def on_dclick ( self, object ):
        clipboard.text_data = "'%s'" % object.image_name

class VolumeColumn ( NameColumn ):

    def get_raw_value ( self, object ):
        name = object.image_name
        return name[ 1: name.find( ':' ) ]

class KeywordsColumn ( LibraryColumn ):

    def get_raw_value ( self, object ):
        return ', '.join( object.keywords )

class TextColumn ( LibraryColumn ):

    def get_raw_value ( self, object ):
        text = getattr( object, self.name )
        col  = text.find( '\n' )
        if col <= 0:
            col = 80
        else:
            col = min( col, 80 )

        return text[ : col ]

class ImageColumn ( NameColumn ):

    def get_raw_value ( self, object ):
        return ''

    def get_image ( self, object ):
        if (object.height <= 32) and (object.width <= 32):
            self.image = object.image_name

            return self.image

        return None

image_table_editor = TableEditor(
    columns = [
        ImageColumn( label = 'Image',      width = 42,
                     auto_editable = True, view  = image_view,
                     horizontal_alignment = 'center' ),
        VolumeColumn(   name = 'volume',      width = 0.10 ),
        NameColumn(     name = 'name',        width = 0.10 ),
        #LibraryColumn(  name = 'image_name',  width = 0.15,
        #                label = 'Image Name' ),
        LibraryColumn(  name = 'width',       width = 0.075,
                        horizontal_alignment = 'center' ),
        LibraryColumn(  name = 'height',      width = 0.075,
                        horizontal_alignment = 'center' ),
        LibraryColumn(  name = 'category',    width = 0.10,
                        horizontal_alignment = 'center' ),
        KeywordsColumn( name = 'keywords',    width = 0.10 ),
        TextColumn(     name = 'description', width = 0.10,
                        auto_editable = True, view  = description_view ),
        TextColumn(     name = 'copyright',   width = 0.10,
                        auto_editable = True, view  = copyright_view ),
        TextColumn(     name = 'license',     width = 0.10,
                        auto_editable = True, view  = license_view ),
    ],
    auto_size           = False,
    editable            = False,
    edit_on_first_click = False,
    show_toolbar        = False,
    filter_name         = 'filter',
    filtered_indices    = 'filtered_indices',
    selection_bg_color  = 0xFBD391,
    selection_color     = 'black',
    selection_mode      = 'rows',
    selected            = 'selected_images'
)

#-------------------------------------------------------------------------------
#  Image library viewer key bindings:
#-------------------------------------------------------------------------------

image_viewer_key_bindings = KeyBindings(
    KeyBinding( binding1    = 'Ctrl-a', method_name = '_select_all',
                description = 'Select all images.' ),
    KeyBinding( binding1    = 'Ctrl-Shift-a', method_name = '_unselect_all',
                description = 'Unselect all images.' ),
    KeyBinding( binding1    = 'Ctrl-c', method_name = '_copy_to_clipboard',
                description = 'Copy selected image names to the clipboard.' ),
    KeyBinding( binding1    = 'Ctrl-k', method_name = 'edit_bindings',
                description = 'Edits the keyboard bindings.' ),
)

#-------------------------------------------------------------------------------
#  'ImageFilter' class:
#-------------------------------------------------------------------------------

class ImageFilter ( TableFilter ):
    """ Filter for ImageInfo objects.
    """

    # The volume name:
    volume = Str

    # The image name:
    image_name = Str

    # The image width:
    width = Size

    # The image height:
    height = Size

    # The image category:
    category = Str

    # The image keyword:
    keyword = Str

    #-- Traits View Definitions ------------------------------------------------

    traits_view = View(
        HGroup(
            Item( 'volume',     width = -65 ),
            '_',
            Item( 'image_name', width = -65, label = 'Name' ),
            '_',
            Item( 'width',      width = -45 ),
            '_',
            Item( 'height',     width = -45 ),
            '_',
            Item( 'category',   width = -65 ),
            '_',
            Item( 'keyword',    width = -65 )
        )
    )

    #-- TableFilter Method Overrides -------------------------------------------

    def filter ( self, object ):
        """ Returns whether a specified object meets the filter criteria.
        """
        name     = object.image_name
        volume   = name[ 1: name.find( ':' ) ].lower()
        keywords = '\n'.join( object.keywords ).lower()
        return ((volume.find( self.volume.lower() )                    >= 0) and
                (object.name.lower().find( self.image_name.lower() )   >= 0) and
                (object.category.lower().find( self.category.lower() ) >= 0) and
                (keywords.find( self.keyword.lower() )                 >= 0) and
                self._width_test(  object.width )                            and
                self._height_test( object.height ))

    #-- Private Methods --------------------------------------------------------

    def _width_test ( self, size ):
        """ Returns whether a specified image width passes the size relation.
        """
        relation, limit = self.width_
        return getattr( self, '_size_' + relation )( size, limit )

    def _height_test ( self, size ):
        """ Returns whether a specified image height passes the size relation.
        """
        relation, limit = self.height_
        return getattr( self, '_size_' + relation )( size, limit )

    def _size_le ( self, size, limit ):
        return (size <= limit)

    def _size_lt ( self, size, limit ):
        return (size < limit)

    def _size_ge ( self, size, limit ):
        return (size >= limit)

    def _size_gt ( self, size, limit ):
        return (size > limit)

    def _size_eq ( self, size, limit ):
        return (size == limit)

    def _size_ne ( self, size, limit ):
        return (size != limit)

    def _size_ignore ( self, size, limit ):
        return True

#-------------------------------------------------------------------------------
#  'ImageLibraryViewer' class:
#-------------------------------------------------------------------------------

class ImageLibraryViewer ( HasPrivateTraits ):

    # The name of the plugin:
    name = Str( 'Image Library Viewer' )

    # The currently selected list of image names:
    image_names = List( Str, connect = 'from: selected image names' )

    # The name of an image volume (i.e. directory or .zip file) to be added to
    # the image library:
    new_volume = File( connect   = 'to: a path or image volume to add to the '
                                   'image library',
                       drop_file = DropFile( extensions = [ '.zip' ],
                           tooltip = 'Drop an image library .zip file to add '
                                     'it to the image library' ) )

    # The name of a directory containing image files to be added to the image
    # library:
    new_directory = Directory( connect = 'to: a directory containing image '
                                      'files to be added to the image library' )

    # The image library being viewed:
    image_library = Constant( ImageLibrary )

    # The list of current selected ImageInfo objects:
    selected_images = List( ImageInfo )

    # The current list of filtered image indices:
    filtered_indices = List( Int )

    # The image filter:
    filter = Instance( ImageFilter, () )

    # The total number of image library images:
    total = Property( depends_on = 'image_library.images' )

    # The current number of filtered image library images:
    current = Property( depends_on = 'filtered_indices' )

    #-- Traits UI View Definitions ---------------------------------------------

    view = View(
        VGroup(
            HGroup(
                Item( 'filter', style = 'custom', show_label = False ),
                '_',
                spring,
                '_',
                Item( 'current',
                      label = 'Current images',
                      style = 'readonly',
                      width = -45 ),
                '_',
                Item( 'total',
                      label = 'Total images',
                      style = 'readonly',
                      width = -45 ),
            ),
            '_',
            Item( 'object.image_library.images',
                  id         = 'images',
                  show_label = False,
                  editor     = image_table_editor
            )
        ),
        title        = 'Image Library Viewer',
        id           = 'enthought.developer.tools.image_library_viewer.'
                       'ImageLibraryViewer',
        width        = 0.75,
        height       = 0.75,
        resizable    = True,
        key_bindings = image_viewer_key_bindings
    )

    #-- Property Implementations -----------------------------------------------

    @cached_property
    def _get_total ( self ):
        return len( self.image_library.images )

    @cached_property
    def _get_current ( self ):
        return len( self.filtered_indices )

    #-- Event Handlers ---------------------------------------------------------

    def _new_volume_changed ( self, volume ):
        """ Handles the 'new_volume' trait being changed.
        """
        try:
            self.image_library.add_volume( volume )
        except TraitError, excp:
            pass # fixme: Display an error dialog here...

    def _new_directory_changed ( self, directory ):
        """ Handles the 'new_directory' trait being changed.
        """
        if isdir( directory ):
            name    = basename( directory )
            catalog = self.image_library.catalog
            if name in catalog:
                count = 2
                while True:
                    new_name = '%s_%d' % ( name, count )
                    if new_name not in catalog:
                        name = new_name
                        break

                    count += 1
            try:
                self.image_library.add_path( name, directory )
            except TraitError, excp:
                pass # fixme: Display an error dialog here...

    def _selected_images_changed ( self ):
        """ Handles the 'selected_image' trait being changed.
        """
        self.image_names = [ img.image_name for img in self.selected_images ]

    #-- Command Handlers -------------------------------------------------------

    def _select_all ( self, info = None ):
        """ Handles the user requesting that all images be selected.
        """
        images = self.image_library.images
        self.selected_images = [ images[i] for i in self.filtered_indices ]

    def _unselect_all ( self, info = None ):
        """ Handles the user requesting that all images be unselected.
        """
        self.selected_images = []

    def _copy_to_clipboard ( self, info = None ):
        """ Copies all currently selected image names to the system clipboard.
        """
        clipboard.text_data = ', '.join( [ "'%s'" % name
                                           for name in self.image_names ] )

#-------------------------------------------------------------------------------
#  Run if invoked from the command line:
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    ImageLibraryViewer().configure_traits()

