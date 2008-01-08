

# Major package imports.
import os
import os.path
import enthought.gotcha as gotcha

from hotshot import Profile


# Envisage library imports.
from enthought.traits.api import Bool, Directory, File, HasTraits, Instance


class Profiler(HasTraits):

    # The filename prefix for the profile files.
    PREFIX = 'gotcha_'

    # The filename suffix for the profile files.
    SUFFIX = '.prof'
    
    #### Profiler interface. ##################################################

    # The HotShot profiler.
    profile = Instance(Profile)

    # The directory to store the HotShot profile files in.
    directory = Directory

    # The most recent file created.
    last_file = File

    # Is the profiler running?
    is_running = Bool(False)
    
    ###########################################################################
    # Public 'Profiler' interface.
    ###########################################################################

    def cleanup(self):
        """ Cleanup all the .prof files in the storage directory. """

        ### Hrmm... Perhaps only cleanup the ones we created?
        for file in os.listdir(self.directory):
            # If the file is a profile file, delete it.
            if self._is_profile_file(file):
                os.remove(file)

        return

    def start(self):
        """ Start the profiler. """

        # Create a hotshot profiler and start it.
        self.last_file = self._get_profile_file()
        self.profile = Profile(self.last_file)

        # self.profile.start()
        import enthought.gotcha as gotcha
        gotcha.profiler = self.profile
        
        self.is_running = True

        return

    def stop(self):
        """ Stop the profiler. """

        self.profile.close()

        import enthought.gotcha as gotcha
        gotcha.profiler = None
        
        self.is_running = False
        
        return

    ###########################################################################
    # Private 'Profiler' interface.
    ###########################################################################

    def _get_profile_file(self):
        """ Get an unused profile filename. """

        highest = 0
        for file in os.listdir(self.directory):
            if self._is_profile_file(file):
                try:
                    prefix_len = len(Profiler.PREFIX)
                    suffix_len = len(Profiler.SUFFIX)
                    highest = max(highest,
                                  int(file[prefix_len:-suffix_len]))
                except Exception, exc:
                    print exc
                    pass

        return os.path.join(self.directory, 'gotcha_%d.prof' % (highest+1))
                                  

    def _is_profile_file(self, file):
        """ Return true if the filename matches a profile file. """

        return (file.startswith(Profiler.PREFIX)) and \
               (file.endswith(Profiler.SUFFIX))
    
#### EOF ######################################################################
