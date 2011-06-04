#-------------------------------------------------------------------------------
#
#  A feature-enabled tool for monitoring Traits notification events.
#
#  Written by: David C. Morrill
#
#  Date: 12/05/2007
#
#  (c) Copright 2007 by Enthought, Inc.
#
#-------------------------------------------------------------------------------

""" A feature-enabled tool for monitoring Traits notification events.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from time \
    import time

from traits.ctraits \
    import _trait_notification_handler

from traits.api \
    import HasPrivateTraits, Str, Int, WeakRef, List, Range, Bool, Float, Any, \
           Constant

from traitsui.api \
    import View, HGroup, VGroup, Item, Handler, TableEditor

from traitsui.table_column \
    import ObjectColumn

#-------------------------------------------------------------------------------
#  Event table editor definition:
#-------------------------------------------------------------------------------

class ValueColumn ( ObjectColumn ):

    def get_value ( self, object ):
        return super( ValueColumn, self ).get_value( object
               ).replace( '\n', '\\n' ).replace( '\r', '\\r' )

class DepthColumn ( ObjectColumn ):

    def get_cell_color ( self, object ):
        depth = object.depth
        if depth == 0:
            return self.read_only_cell_color_

        self.cell_color = ( min( 255, int( 63.75 * (depth - 1) ) ),
                            max(   0, int( 63.75 * (5 - depth) ) ),
                            0 )

        return self.cell_color_

events_table_editor = TableEditor(
    columns = [
        ObjectColumn( name = 'class_name', width = 0.15,  editable = False ),
        ObjectColumn( name = 'id',         width = 0.15,  editable = False,
                      label = 'Object Id', format = '%08X' ),
        ObjectColumn( name = 'name',       width = 0.15,  editable = False ),
        ValueColumn(  name = 'old',        width = 0.175, editable = False ),
        ValueColumn(  name = 'new',        width = 0.175, editable = False ),
        DepthColumn(  name = 'depth',      width = 0.05,  editable = False,
                      horizontal_alignment = 'center' ),
        ObjectColumn( name = 'timestamp',  width = 0.15,  editable = False,
                      format = '%.3f', horizontal_alignment = 'right' )
    ],
    show_toolbar       = False,
    editable           = False,
    auto_size          = False,
    selection_bg_color = 0xFBD391,
    selection_color    = 'black'
)

#-------------------------------------------------------------------------------
#  'NotificationEvent' class:
#-------------------------------------------------------------------------------

class NotificationEvent ( HasPrivateTraits ):
    """ Represents a Traits notification event.
    """

    # The name of the receiving object's class:
    class_name = Str

    # The id of the receiving object:
    id = Int

    # A weak reference to the receiving object:
    object = WeakRef

    # The name of the trait that generated the notification:
    name = Str

    # The old value sent with the notification:
    old = Any

    # The new value sent with the notification:
    new = Any

    # The time stamp of when the event notification was generated:
    timestamp = Float

    # The recursion depth of the event handler:
    depth = Int

#-------------------------------------------------------------------------------
#  'EventMonitor' class:
#-------------------------------------------------------------------------------

class EventMonitor ( Handler ):
    """ A feature-enabled tool for monitoring Traits notification events.
    """

    # The list of recent events:
    events = List( NotificationEvent )

    # The maximum number of events to keep:
    max_events = Range( 1, 100000, 30 )

    # Total number of events logged:
    total_events = Int

    # Is event monitoring enabled?
    enabled = Bool( False )

    # The previous Trait notification handler:
    previous_handler = Any

    # The time base used to define time 0:
    time_base = Constant( time() )

    # The current recursion depth of the event monitor:
    depth = Int

    #-- Traits View Definitions ------------------------------------------------

    view = View(
        VGroup(
            HGroup(
                Item( 'enabled' ),
                Item( 'max_events', label = 'Maximum events' ),
                Item( 'total_events', style = 'readonly', width = 70 )
            ),
            Item( 'events',
                  id         = 'events',
                  show_label = False,
                  editor     = events_table_editor
            )
        ),
        id        = 'etsdevtools.developer.tools.event_monitor.EventMonitor',
        title     = 'Traits Notification Event Monitor',
        width     = 0.5,
        height    = 0.5,
        resizable = True
    )

    #-- Handler Class Method Overrides -----------------------------------------

    def init ( self, info ):
        """ Initializes the controls of a user interface.
        """
        # This is a hack to prevent the objects which are part of the event
        # monitor from generating monitored events:
        info.events._no_event_notification       = \
        info.events.model._no_event_notification = \
        info.events.grid._no_event_notification  = True

        return True

    def closed ( self, info, is_ok ):
        """ Handles a dialog-based user interface being closed by the user.
        """
        # Make sure the notification handler has been removed:
        self.enabled = False

    #-- Trait Event Handlers ---------------------------------------------------

    def _enabled_changed ( self, enabled ):
        """ Handles the monitoring state being changed.
        """
        if enabled:
            self.previous_handler = _trait_notification_handler(
                                        self._handle_event )
        else:
            _trait_notification_handler( self.previous_handler )

    #-- Private Methods -------------------------------------------------------

    def _handle_event ( self, handler, args ):
        """ Handles a traits notification event being generated.
        """
        object, name, old, new = args
        if ((not self._ignore_event) and
            (not getattr( object, '_no_event_notification', False ))):
            self._ignore_event = True
            if not isinstance( object, IgnoreClasses ):
                events = self.events
                events.append( NotificationEvent(
                    class_name = object.__class__.__name__,
                    id         = id( object ),
                    object     = object,
                    name       = name,
                    old        = old,
                    new        = new,
                    timestamp  = time() - self.time_base,
                    depth      = self.depth ) )

                delta = (len( events ) - self.max_events)
                if delta > 0:
                    del events[ : delta ]

                self.total_events += 1

            self._ignore_event = False

        self.depth += 1
        try:
            handler( *args )
        finally:
            self.depth -= 1

# The event classes that should be ignored:
IgnoreClasses = ( NotificationEvent, EventMonitor )

# Test code:
if __name__ == '__main__':
    EventMonitor().configure_traits()

