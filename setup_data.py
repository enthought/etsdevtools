# Function to convert simple ETS project names and versions to a requirements
# spec that works for both development builds and stable builds.  Allows
# a caller to specify a max version, which is intended to work along with
# Enthought's standard versioning scheme -- see the following write up:
#    https://svn.enthought.com/enthought/wiki/EnthoughtVersionNumbers
def etsdep(p, min, max=None, literal=False):
    require = '%s >=%s.dev' % (p, min)
    if max is not None:
        if literal is False:
            require = '%s, <%s.a' % (require, max)
        else:
            require = '%s, <%s' % (require, max)
    return require


# Declare our ETS project dependencies.
APPTOOLS = etsdep('AppTools', '3.4.0')  # import of enthought.io in enthought.developer
ENTHOUGHTBASE = etsdep('EnthoughtBase', '3.0.6')
ENTHOUGHTBASE_UI = etsdep('EnthoughtBase[ui]', '3.0.6')  # e.util.wx.* imported in developer
ENVISAGECORE = etsdep('EnvisageCore', '3.1.3')
ENVISAGEPLUGINS = etsdep('EnvisagePlugins', '3.1.3')  # -- imported only in enthought.gotcha
TRAITSBACKENDWX = etsdep('TraitsBackendWX', '3.5.0')  # -- imported mostly by enthought.developer, but one from enthought.gotcha
TRAITSGUI = etsdep('TraitsGUI', '3.5.0')
TRAITSGUI_DOCK = etsdep('TraitsGUI[dock]', '3.5.0')  # -- imported only by enthought.developer.
TRAITS_UI = etsdep('Traits[ui]', '3.5.0')


# A dictionary of the pre_setup information.
INFO = {
    'extras_require': {
        'developer': [
            APPTOOLS,
            ENTHOUGHTBASE_UI,
            TRAITSBACKENDWX,
            TRAITSGUI_DOCK,
            ],
        'envisage': [  # -- all plugins are here, even fbi, and developer.
            ENVISAGECORE,
            ENVISAGEPLUGINS,
            ],
        'fbi': [
            # fbi.py internally uses the developer code so requires everything
            # that the developer extra requires.
            APPTOOLS,
            ENTHOUGHTBASE_UI,
            TRAITSBACKENDWX,
            TRAITSGUI_DOCK,
            ],

        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
            'docutils',
            'nose',
            'Pyro',
            'reportlab',
            'setuptools',
            'testoob',
            'wxPython',
            ],
        },
    'install_requires': [
        TRAITSGUI,
        TRAITS_UI,
        ],
    'name': 'ETSDevTools',
    'version': '3.1.1',
}


# Add additional "nonets" dependencies if on Windows.
import sys
if sys.platform == 'win32':
    INFO['extras_require']['nonets'].append('pywin32')
