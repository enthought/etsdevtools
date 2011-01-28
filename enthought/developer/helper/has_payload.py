#-------------------------------------------------------------------------------
#
#  Defines a HasPayload interface that can be recognized by drag handlers as
#  an object that contains another object (i.e. the 'payload'). This allows
#  the object implementing HasPayload to add additional functionality that the
#  payload object may not have.
#
#  Written by: David C. Morrill
#
#  Date: 07/04/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from enthought.traits.api \
    import HasPrivateTraits, Any, Property

#-------------------------------------------------------------------------------
#  'HasPayload' class:
#-------------------------------------------------------------------------------

class HasPayload ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The 'payload' object:
    payload = Any

    # Payload name:
    payload_name = Property

    # Full payload name:
    payload_full_name = Property

#-- Property Implementations ---------------------------------------------------

    #---------------------------------------------------------------------------
    #  Implementation of the 'payload_name' property:
    #---------------------------------------------------------------------------

    def _get_payload_name ( self ):
        if self._payload_name is not None:
            return self._payload_name

        return self.payload.__class__.__name__

    def _set_payload_name ( self, name ):
        self._payload_name = name

    #---------------------------------------------------------------------------
    #  Implementation of the 'payload_full_name' property:
    #---------------------------------------------------------------------------

    def _get_payload_full_name ( self ):
        if self._payload_full_name is not None:
            return self._payload_full_name

        return self.payload.__class__.__name__

    def _set_payload_full_name ( self, full_name ):
        self._payload_full_name = full_name

