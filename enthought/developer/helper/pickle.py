#-------------------------------------------------------------------------------
#
#  Defines the 'get_pickle' and 'set_pickle' functions for easy getting and
#  setting of persistent values in the traits ui database.
#
#  Written by: David C. Morrill
#
#  Date: 07/15/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import shelve
import os

from traits.trait_base \
    import traits_home

#-------------------------------------------------------------------------------
#  Opens the traits UI database:
#-------------------------------------------------------------------------------

def get_ui_db ( mode = 'r' ):
    """ Opens the traits UI database.
    """
    try:
        return shelve.open( os.path.join( traits_home(), 'traits_ui' ),
                            flag = mode, protocol = -1 )
    except:
        return None

#-------------------------------------------------------------------------------
#  Gets the value of a specified pickle name:
#-------------------------------------------------------------------------------

def get_pickle ( name, default = None ):
    """ Gets the value of a specified pickle name.
    """
    result = default
    db     = get_ui_db()
    if db is not None:
        result = db.get( name, default )
        db.close()

    return result

#-------------------------------------------------------------------------------
#  Sets the value of a specified pickle name:
#-------------------------------------------------------------------------------

def set_pickle ( name, value ):
    """ Sets the value of a specified pickle name.
    """
    db = get_ui_db( mode = 'c' )
    if db is not None:
        db[ name ] = value
        db.close()
        return True

    return False

