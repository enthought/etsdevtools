#-------------------------------------------------------------------------------
#
#  Plugin for testing/developing Traits UI views.
#
#  Written by: David C. Morrill
#
#  Date: 07/08/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from os.path \
    import exists

from traits.api \
    import HasTraits, HasPrivateTraits, List, File, Str, Instance, Bool

from traitsui.api \
    import View, VGroup, Item, ListEditor

from pyface.timer.api \
    import do_later

from pyface.image_resource \
    import ImageResource

from etsdevtools.developer.features.api \
    import CustomFeature

from etsdevtools.developer.api \
    import file_watch

from etsdevtools.developer.helper.themes \
    import TTitle

#-------------------------------------------------------------------------------
#  'ViewTester' class:
#-------------------------------------------------------------------------------

class ViewTester ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'View Tester' )

    # Peristent state id for this view:
    id = Str( 'etsdevtools.developer.tools.view_tester.state',
              save_state_id = True )

    # Should a changed file be automatically reloaded:
    auto_load = Bool( True, save_state = True )

    # Should old view be automatically closed when a new one is run?
    auto_close = Bool( True, save_state = True )

    # Custom feature for creating a dynamic 'run' button:
    run_button = Instance( CustomFeature, {
                               'image':   ImageResource( 'run' ),
                               'click':   'run_file',
                               'tooltip': 'Click to run the current file',
                               'enabled': False },
                               custom_feature = True )

    # The source file containing the view code to be tested:
    file_name = File( droppable = 'Drag a Python source code file here.' )

    # The object containing the view being tested:
    view_objects = List( HasTraits )

    # Information message on how to use the view tester:
    info = Str( "Drag a Python file containing an object named 'view' to the "
                "tab for this view." )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        TTitle( 'info', visible_when = 'len(view_objects)==0' ),
        Item( 'view_objects@',
              editor     = ListEditor( use_notebook = True,
                                       deletable    = True,
                                       dock_style   = 'tab',
                                       export       = 'DockWindowShell' ),
              show_label = False
        ),
        title = 'View Tester'
    )

    options = View(
        VGroup(
            Item( 'auto_load',
                  label = 'Automatically run a changed file '
            ),
            Item( 'auto_close',
                  label = 'Automatically close old views'
            ),
            show_left = False
        ),
        title   = 'View Tester Options',
        id      = 'etsdevtools.developer.tools.view_tester.options',
        buttons = [ 'OK', 'Cancel' ]
    )

    #---------------------------------------------------------------------------
    #  Handles the 'file_name' trait being changed:
    #---------------------------------------------------------------------------

    def _file_name_changed ( self, old, new ):
        """ Handles the 'file_name' trait being changed.
        """
        self.set_listener( old, True )
        self.set_listener( new, False )
        self.run_button.enabled = False
        if new != '':
            self.run_file()

    #---------------------------------------------------------------------------
    #  Runs the current file and creates it view:
    #---------------------------------------------------------------------------

    def run_file ( self ):
        """ Runs the current file and creates it view.
        """
        dic = {}
        try:
            execfile( self.file_name, dic, dic )
        except:
            import traceback
            traceback.print_exc()
            raise

        view = dic.get( 'view' )
        if view is None:
            view = dic.get( 'demo' )
        if view is not None:
            if self.auto_close:
                self.view_objects = [ view ]
            else:
                self.view_objects.append( view )

        self.run_button.enabled = False

    #---------------------------------------------------------------------------
    #  Sets up/Removes a file watch on a specified file:
    #---------------------------------------------------------------------------

    def set_listener ( self, file_name, remove ):
        """ Sets up/Removes a file watch on a specified file.
        """
        if exists( file_name ):
            file_watch.watch( self.file_changed, file_name, remove = remove )

    #---------------------------------------------------------------------------
    #  Handles the current file being updated:
    #---------------------------------------------------------------------------

    def file_changed ( self, file_name ):
        """ Handles the current file being updated.
        """
        if self.auto_load:
            self.run_file()
        else:
            self.run_button.enabled = True

    #---------------------------------------------------------------------------
    #  Handles the 'auto_load' trait being changed:
    #---------------------------------------------------------------------------

    def _auto_load_changed ( self, auto_load ):
        """ Handles the 'auto_load' trait being changed.
        """
        if auto_load and self.run_button.enabled:
            self.run_file()

        self.run_button.enabled = False

#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

view = ViewTester()

