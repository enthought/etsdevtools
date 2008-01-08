
# Enthought library imports.
from enthought.envisage import Plugin
from enthought.traits.api import Bool, Instance

# Local imports.
from gotcha_editor import GotchaEditor
from profiler import Profiler


class GotchaPlugin(Plugin):
    """ The Gotcha profiling plugin. """

    # The shared plugin instance.
    instance = None

    #### 'GotchaPlugin' interface. ############################################

    profiler = Instance(Profiler)

    profiler_running = Bool(False)
    
    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **kw):
        """ Creates a new plugin. """

        # Base class constructor.
        super(GotchaPlugin, self).__init__(**kw)

        # Set the shared instance.
        GotchaPlugin.instance = self

        return

    ###########################################################################
    # 'Plugin' interface.
    ###########################################################################

    def start(self, application):
        """ Starts the plugin. """

        pass

    def stop(self, application):
        """ Stops the plugin. """

        # Check if we should delete the profile files.
        if self.preferences.get('cleanup_profiles'):
            self.profiler.cleanup()

        return

    ###########################################################################
    # 'GotchaPlugin' interface.
    ###########################################################################

    def start_profiling(self):
        """ Start the profiler. """

        if self.profiler is None:
            self.profiler = Profiler(directory=self.state_location)

        if not self.profiler.is_running:
            self.profiler.start()
            self.profiler_running = True

        return

    def stop_profiling(self):
        """ Stop the profiler. """

        if self.profiler is not None:
            self.profiler.stop()
            self.profiler_running = False
            
            viewer = GotchaEditor(self.profiler.last_file)
            viewer.open()

        return
    
#### EOF ######################################################################
