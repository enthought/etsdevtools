""" A view containing a file browser. """


# Standard library imports.
import logging
import glob

from os \
    import listdir, sep

from os.path \
    import exists, join, isdir, isfile, splitext

# Enthought library imports.
from envisage.api import IExtensionRegistry
from envisage.api import ExtensionPoint
from pyface.workbench.api import View
from traitsui.menu import Action as TraitsAction, Menu as TraitsMenu
from etsdevtools.developer.tools.file_browser import FileBrowser, RootNode, PathNode, FileNode
from pyface.api import GUI
from traits.api import Instance, Property, implements, Dict, Any
from traitsui.api import Handler, View as TraitsView, Item, TreeEditor, InstanceEditor
from traitsui.tree_node import ObjectTreeNode

# Setup a logger for this module.
logger = logging.getLogger(__name__)

class ObjectFileNode(ObjectTreeNode):
    """
    """

    node_for = [FileNode]

    label = 'name'

#    def get_icon(self, object, is_expanded):
#        if splitext(object.file_name)[1] == '.py':
#            return 'python'
#        else:
#            return super(ObjectFileNode, self).get_icon(object, is_expanded)

    def get_menu(self, object):
        """
        """

        actions = [TraitsAction(name = 'Open',
                                action = 'open')]

        if splitext(object.file_name)[1] == '.py':
            actions.append(TraitsAction(name = 'Run',
                                        action = 'run'))
        menu = TraitsMenu( *actions )
        return menu

#-------------------------------------------------------------------------------
#  Tree editor definition:
#-------------------------------------------------------------------------------

class FileBrowserHandler(Handler):

    info = Any

    def init_info(self, info):
        self.info = info

    def run(self, info, object):
        self.info.object.run(object.file_name)

tree_editor = TreeEditor(
    editable  = False,
    selected  = 'selected',
    nodes     = [
        ObjectTreeNode( node_for   = [ RootNode ],
                        auto_open  = True,
                        label      = 'path' ),
        ObjectTreeNode( node_for   = [ PathNode ],
                        auto_close = True,
                        label      = 'name' ),
        ObjectFileNode()
    ]
)

class FileBrowserView(View, FileBrowser):
    """ A view containing a file browser. """

    #### 'IView' interface ####################################################

    # The part's globally unique identifier.
    id = 'etsdevtools.developer.tools.file_browser'

    # The part's name (displayed to the user).
    name = 'Workspace'

    # The default position of the view relative to the item specified in the
    # 'relative_to' trait.
    position = 'bottom'

    #### 'IExtensionPointUser' interface ######################################

    traits_view = TraitsView(
        Item( name       = 'root',
              editor     = tree_editor,
              show_label = False
              ), handler=FileBrowserHandler
              )

    ###########################################################################
    # 'View' interface.
    ###########################################################################

    def create_control(self, parent):
        """ Creates the toolkit-specific control that represents the view. """


        self.ui = self.edit_traits(parent=parent, kind='subpanel')
        # Register the file browser as a service.
        self.window.application.register_service(FileBrowser, self)
        return self.ui.control

    def run(self, filename=None, shell=None):
        """
        """
        if filename is None:
            filename = self.path

        if shell is None:
            shell = self.window.get_view_by_id(
                'envisage.plugins.python_shell_view'
            )

        if shell is not None:
            self.run_dir(shell, filename)

    def run_dir(self, view, path):
        if isfile(path):
            self.run_script(view, path)
        elif isdir(path):
            for file in glob.iglob(join(path, '*.py')):
                self.run_script(view, file)
        for dir in glob.iglob(join(path, '*') + sep):
            self.run_dir(view, dir)
        return

    def run_script(self, view, filename):
        view.execute_command('%run  ' + '"%s"' % filename, hidden=False)


#### EOF ######################################################################
