
import os

from enthought.envisage.ui import WorkbenchAction
from enthought.pyface.api import FileDialog, OK

from enthought.gotcha.plugin.gotcha_editor import GotchaEditor

class OpenProfile(WorkbenchAction):
    """ Workbench action to open an existing profile file. """

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self):
        """ Start the profiler. """

        wildcard = FileDialog.create_wildcard('Gotcha! files', '*.prof')
        dialog = FileDialog(title='Open',
                            action='open',
                            directory=os.getcwd(),
                            wildcard=wildcard)
        if dialog.open() == OK:
            editor = GotchaEditor(filename=dialog.path)
            self.window.invoke_later(editor.open)
        
        return
        
#### EOF ######################################################################
