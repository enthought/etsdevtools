#-------------------------------------------------------------------------------
#  
#  Defines the Saveable interface that allows plugins with saveable state to
#  easily manage that state using the SaveFeature.
#  
#  Wrtten by: David C. Morrill
#  
#  Date: 07/08/2005
#  
#  (c) Copyright 2006 by David C. Morrill
#  
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasPrivateTraits, false
    
#-------------------------------------------------------------------------------
#  'Saveable' class:
#-------------------------------------------------------------------------------

class Saveable ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------

    # Set true when the object needs to have its state saved:
    needs_save = false
    
    #---------------------------------------------------------------------------
    #  The method called to save the state of the object:
    #---------------------------------------------------------------------------

    def save ( self ):
        raise NotImplementedError
        
