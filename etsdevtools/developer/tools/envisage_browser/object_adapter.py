#-------------------------------------------------------------------------------
#
#  Defines the ObjectAdapter class used by all Envisage browser object
#  adapters contained within the main ApplicationAdapter object
#
#  Written by: David C. Morrill
#
#  Date: 06/16/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from traits.api \
    import HasTraits, Instance, Any, Property, Delegate

from etsdevtools.developer.tools.envisage_browser.object_adapter_base \
    import ObjectAdapterBase

#-------------------------------------------------------------------------------
#  Trait definitions:
#-------------------------------------------------------------------------------

# A trait re-exported from the adapted object:
Export = Delegate( 'adaptee' )

#-------------------------------------------------------------------------------
#  'ObjectAdapter' class:
#-------------------------------------------------------------------------------

class ObjectAdapter ( ObjectAdapterBase ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The object we are adapting:
    adaptee = Any

    # The list of base classes for the adapted object:
    base_classes = Property

    # The application this object is associated with:
    application = Any # Instance( ApplicationAdapter )

    # The object containing this ExtensionItem (optional):
    container = Instance( 'ObjectAdapter' )

#-- Property Implementations ---------------------------------------------------

    def _get_base_classes ( self ):
        if self._base_classes is None:
            queue = [ self.adaptee.__class__ ]
            bc    = []
            while len( queue ) > 0:
                klass = queue.pop()
                if klass not in bc:
                    bc.append( klass )
                    queue.extend( klass.__bases__ )
            self._base_classes = bc

        return self._base_classes

