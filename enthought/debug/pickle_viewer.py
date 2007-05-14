#-------------------------------------------------------------------------------
#
#  A utility for displaying the contents of a Python pickle file graphically.
#
#  Written by: David C. Morrill
#
#  Date: 06/19/2006
#
#  (c) Copyright 2006 by Enthought, Inc.
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports
#-------------------------------------------------------------------------------

from cPickle \
    import load
    
from enthought.traits.api \
    import HasPrivateTraits, Any, Str, File, View, VGroup, Item, ValueEditor

from enthought.traits.ui.menu \
    import NoButtons

#-------------------------------------------------------------------------------
#  'PickleViewer' class:
#-------------------------------------------------------------------------------

class PickleViewer ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------

    # The name of the pickle file we are viewing:
    file_name = File

    # The contents of the pickle file:
    contents = Any
    
    # Status message:
    status = Str( 'Enter the name of a Python pickle file.' )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    view = View( 
               VGroup(
                   Item( 'status~' ),
                   Item( 'file_name' ),
                   VGroup( 
                       Item( 'contents@', 
                             show_label = False,
                             editor     = ValueEditor() 
                       ),
                       label = 'Pickle Contents',
                       show_border = True 
                   )
               ),
               title     = 'Pickle Viewer',
               id        = 'enthought.debug.pickle_viewer.PickleViewer',
               width     = 0.5,
               height    = 0.5,
               resizable = True,
               buttons   = NoButtons
           )

#-- Event Handlers -------------------------------------------------------------

    def _file_name_changed ( self, file_name ):
        """ Handles the 'file_name' trait being changed.
        """
        fh = None
        for mode in [ 'rb', 'r' ]:
            try:
                fh = file( file_name, mode )
                self.contents = load( fh )
                self.status   = 'Pickle loaded.'
                fh.close()
                return
            except:
                if fh is None:
                    break
                fh.close()
                fh = None
        self.contents = None 
        self.status   = 'Not a valid Python pickle file.'

#-------------------------------------------------------------------------------
#  Start the utility:
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    PickleViewer().configure_traits()
