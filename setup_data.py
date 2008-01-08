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
APPTOOLS = etsdep('AppTools', '3.0.0b1')  # -- import of enthought.io in enthought.developer
CHACO = etsdep('Chaco', '3.0.0b1')  # -- imported only in enthought.gotcha
ENTHOUGHTBASE = etsdep('EnthoughtBase', '3.0.0b1')
ENVISAGECORE = etsdep('EnvisageCore', '3.0.0b1')
ENVISAGEPLUGINS = etsdep('EnvisagePlugins', '3.0.0b1')  # -- imported only in enthought.gotcha
TRAITS = etsdep('Traits', '3.0.0b1')
TRAITSBACKENDWX = etsdep('TraitsBackendWX', '3.0.0b1')  # -- imported mostly by enthought.developer, but one from enthought.gotcha
TRAITSGUI = etsdep('TraitsGUI', '3.0.0b1')
TRAITSGUI_DOCK = etsdep('TraitsGUI[dock]', '3.0.0b1')  # -- imported only by enthought.developer.


# A dictionary of the pre_setup information.
INFO = {
    'extras_require': {
        'envisage': [
            ENVISAGECORE,
            ENVISAGEPLUGINS,
            ],
        'developer': [
            APPTOOLS,
            TRAITSBACKENDWX,
            TRAITSGUI_DOCK,
            ],
        'gotcha': [
            CHACO,
            TRAITSBACKENDWX,
            ],

        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
            'cElementTree',
            'elementtree',
            'nose',
            'testoob',
            ],
        },
    'install_requires': [
        ENTHOUGHTBASE,
        TRAITS,
        TRAITSGUI,
        ],
    'name': 'DevTools',
    'version': '3.0.0b1',
    }
