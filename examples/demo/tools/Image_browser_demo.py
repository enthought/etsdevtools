"""
Another demonstration of the ListCanvasEditor using the ImageBrowser tool.

The ImageBrowser tool uses a ListCanvasEditor to display a collection of
Traits image library images specified by their image name. Each item on
the canvas is an ImageItem object, which represents a single image.

For more information about how this program works, refer to the source code
of the ImageBrowser tool (enthought.developer.tools.image_browser.py).

Note: This demo requires the enthought.developer package to be installed.
"""

#-- Imports --------------------------------------------------------------------

from enthought.developer.tools.image_browser \
     import ImageBrowser
     
from enthought.traits.ui.image.image \
     import ImageLibrary
     
# Get the image library volume called 'std':
volume = ImageLibrary.catalog[ 'std' ]

# Create the demo using a subset of the images available in the 'std' volume:
demo = ImageBrowser(
           image_names = [ image.image_name for image in volume.images ] )
        
# Run the demo (if invoked from the command line):
if __name__ == '__main__':
    demo.configure_traits()
    
