#-------------------------------------------------------------------------------
#
#  Returns the contents of a text file as a string.
#
#  Written by: David C. Morrill
#
#  Date: 07/01/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Returns the contents of a file as a string:
#-------------------------------------------------------------------------------

def read_file ( file_name, mode = 'rb' ):
    """ Returns the contents of a text file as a string.
    """
    fh = result = None

    try:
        fh     = file( file_name, mode )
        result = fh.read()
    except:
        pass

    if fh is not None:
        try:
            fh.close()
        except:
            pass

    return result
