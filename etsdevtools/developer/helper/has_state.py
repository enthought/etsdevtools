#-------------------------------------------------------------------------------
#
#  Defines the HasState interface that allows plugins with persistent state to
#  easily manage that state.
#
#  Wrtten by: David C. Morrill
#
#  Date: 07/06/2005
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import shelve

from os.path \
    import join

from traits.api \
    import HasPrivateTraits, Str

from traits.trait_base \
    import traits_home

#-------------------------------------------------------------------------------
#  'HasState' class:
#-------------------------------------------------------------------------------

class HasState ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The persistence id for the plugin:
    id = Str

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__ ( self, **traits ):
        super( HasState, self ).__init__( **traits )
        self.restore_state()

    #---------------------------------------------------------------------------
    #  Returns the persistent state of the object:
    #---------------------------------------------------------------------------

    def get_state ( self ):
        return self.get()

    #---------------------------------------------------------------------------
    #  Saves the current state of the plugin:
    #---------------------------------------------------------------------------

    def save_state ( self ):
        """ Saves the current state of the plugin.
        """
        id = self.id
        if (id != '') and (not self._no_save_state):
            db = self._get_ui_db( mode = 'c' )
            if db is not None:
                db[ id ] = self.get_state()
                db.close()

    #---------------------------------------------------------------------------
    #  Restores the previously saved state of the plugin:
    #---------------------------------------------------------------------------

    def restore_state ( self ):
        """ Restores the previously saved state of the plugin.
        """
        id = self.id
        if id != '':
            db = self._get_ui_db()
            if db is not None:
                self._no_save_state = True
                try:
                    state = db.get( id )
                    if state is not None:
                        self.set( **state )
                except:
                    pass
                self._no_save_state = False
                db.close()

    #---------------------------------------------------------------------------
    #  Returns a reference to the traits UI preference database:
    #---------------------------------------------------------------------------

    def _get_ui_db ( self, mode = 'r' ):
        """ Returns a reference to the traits UI preference database.
        """
        try:
            return shelve.open( join( traits_home(), 'traits_ui' ),
                                flag = mode, protocol = -1 )
        except:
            return None

