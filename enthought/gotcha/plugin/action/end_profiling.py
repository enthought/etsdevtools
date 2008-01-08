
from enthought.envisage.ui import WorkbenchAction

from enthought.gotcha.plugin.gotcha_plugin import GotchaPlugin

class EndProfiling(WorkbenchAction):
    """ Workbench action to end the profiler. """

    def __init__(self, **traits):
        """ Constructor. """

        super(EndProfiling, self).__init__(**traits)

        GotchaPlugin.instance.on_trait_change(self._profiler_state_change,
                                              'profiler_running')

        self.enabled = GotchaPlugin.instance.profiler_running
    
    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self):
        """ Start the profiler. """

        GotchaPlugin.instance.stop_profiling()
        
        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _profiler_state_change(self, obj, trait_name, old, new):
        """ Called when the profiler starts or stops. """

        self.enabled = new

        return
    
#### EOF ######################################################################
