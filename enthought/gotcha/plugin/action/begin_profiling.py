
from enthought.envisage.ui import WorkbenchAction

from enthought.gotcha.plugin.gotcha_plugin import GotchaPlugin

class BeginProfiling(WorkbenchAction):
    """ Workbench action to start the profiler. """

    def __init__(self, **traits):
        """ Constructor. """

        super(BeginProfiling, self).__init__(**traits)

        GotchaPlugin.instance.on_trait_change(self._profiler_state_change,
                                              'profiler_running')

        self.enabled = not GotchaPlugin.instance.profiler_running

        return
        
    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self):
        """ Start the profiler. """

        GotchaPlugin.instance.start_profiling()
        
        return

    def _profiler_state_change(self, obj, trait_name, old, new):
        """ Called when the profiler starts or stops. """

        self.enabled = not new

        return
        
#### EOF ######################################################################
