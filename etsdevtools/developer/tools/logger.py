#-------------------------------------------------------------------------------
#
#  Display Log Messages plugin.
#
#  Written by: David C. Morrill
#
#  Date: 07/16/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import logging

from traits.api \
    import HasPrivateTraits, Any, Enum, Instance, List, Range, Str, Property

from traitsui.api \
    import View, Item, TableEditor

from traitsui.table_column \
    import ObjectColumn

from traitsui.table_filter \
    import EvalFilterTemplate, RuleFilterTemplate, MenuFilterTemplate

from etsdevtools.developer.api \
    import FilePosition

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# Mapping from our Enum values to the logging module values:
LevelMap = {
    'Debug':    logging.DEBUG,
    'Info':     logging.INFO,
    'Warning':  logging.WARNING,
    'Error':    logging.ERROR,
    'Critical': logging.CRITICAL
}

# Formatters for formatting the various log record fields:
Formatters = {
    'name':       logging.Formatter( '%(name)s' ),
    'level_no':   logging.Formatter( '%(levelno)s' ),
    'level_name': logging.Formatter( '%(levelname)s' ),
    'path_name':  logging.Formatter( '%(pathname)s' ),
    'file_name':  logging.Formatter( '%(filename)s' ),
    'module':     logging.Formatter( '%(module)s' ),
    'line_no':    logging.Formatter( '%(lineno)s' ),
    'created':    logging.Formatter( '%(created)s' ),
    'asctime':    logging.Formatter( '%(asctime)s' ),
    'msecs':      logging.Formatter( '%(msecs)s' ),
    'thread':     logging.Formatter( '%(thread)s' ),
    'process':    logging.Formatter( '%(process)s' ),
    'message':    logging.Formatter( '%(message)s' )
}

#-------------------------------------------------------------------------------
#  'LogHandler' class:
#-------------------------------------------------------------------------------

class LogHandler ( logging.Handler ):

    def __init__ ( self, owner ):
        logging.Handler.__init__( self )
        self.owner = owner

    def emit( self, record ):
        self.owner.emit( record )

#-------------------------------------------------------------------------------
#  Define the LRProperty traits:
#-------------------------------------------------------------------------------

def get_lr_field ( log_record, name ):
    return Formatters[ name ].format( log_record.log_record
           ).split( '\n')[0].strip()

LRProperty = Property( get_lr_field )

#-------------------------------------------------------------------------------
#  'LogRecord' class:
#-------------------------------------------------------------------------------

class LogRecord ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The associated logging log record:
    log_record = Any

    # The name of the logger:
    name = LRProperty

    # Numeric logging level for the message
    level_no = LRProperty

    # Text logging level for the message
    level_name = LRProperty

    # Full path name of the source file where the logging call was issued:
    path_name = LRProperty

    # File name portion of path name:
    file_name = LRProperty

    # Module (name portion of the file name):
    module = LRProperty

    # Source line number where the logging call was issued:
    line_no = LRProperty

    # Time when the LogRecord was created (as returned by time.time()):
    created = LRProperty

    # Human-readable time when the LogRecord was created:
    asctime = LRProperty

    # Millisecond portion of the time when the LogRecord was created:
    msecs = LRProperty

    # Thread ID:
    thread = LRProperty

    # Process ID:
    process = LRProperty

    # The logged message, computed as msg % args:
    message = LRProperty

#-------------------------------------------------------------------------------
#  Logger table editor definition:
#-------------------------------------------------------------------------------

logger_table_editor = TableEditor(
    columns = [ ObjectColumn( name     = 'level_name',
                              label    = 'Level',
                              editable = False,
                              horizontal_alignment = 'center' ),
                ObjectColumn( name     = 'message',
                              editable = False ) ],
    other_columns = [
                ObjectColumn( name     = 'name',
                              label    = 'Logger Name',
                              editable = False ),
                ObjectColumn( name     = 'level_no',
                              label    = 'Level #',
                              editable = False,
                              horizontal_alignment = 'center' ),
                ObjectColumn( name     = 'path_name',
                              editable = False ),
                ObjectColumn( name     = 'file_name',
                              editable = False ),
                ObjectColumn( name     = 'module',
                              editable = False ),
                ObjectColumn( name     = 'line_no',
                              label    = 'Line #',
                              editable = False,
                              horizontal_alignment = 'center' ),
                ObjectColumn( name     = 'created',
                              label    = 'Raw Time Created',
                              editable = False ),
                ObjectColumn( name     = 'asctime',
                              label    = 'Time Created',
                              editable = False ),
                ObjectColumn( name     = 'msecs',
                              label    = 'Milliseconds',
                              editable = False ),
                ObjectColumn( name     = 'thread',
                              label    = 'Thread Id',
                              editable = False ),
                ObjectColumn( name     = 'process',
                              label    = 'Process Id',
                              editable = False ) ],
    filters = [ EvalFilterTemplate,
                RuleFilterTemplate,
                MenuFilterTemplate ],
    auto_size          = False,
    sortable           = False,
    selection_bg_color = 0xFBD391,
    selection_color    = 'black',
    selected           = 'selected'
)

#-------------------------------------------------------------------------------
#  'Logger' class:
#-------------------------------------------------------------------------------

class Logger ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'Logger' )

    # The persistence id for this object:
    id = Str( 'etsdevtools.developer.tools.logger.state', save_state_id = True )

    # Maximum number of log messages displayed:
    max_records = Range( 1, 10000, 100, save_state = True )

    # Current logging level:
    logging_level = Enum( 'Debug', 'Info', 'Warning', 'Error', 'Critical',
                          save_state = True )

    # Log handler:
    log_handler = Instance( LogHandler )

    # Log record formatter:
    formatter = Instance( logging.Formatter, ( '%(levelname)s: %(message)s', ) )

    # Current selected log record:
    selected = Instance( LogRecord, allow_none = False )

    # The current set of log records:
    log_records = List( LogRecord )

    # Currently selected entries file position information:
    file_position = Instance( FilePosition,
                              draggable = 'Drag file position information',
                              connect   = 'from: file position' )

    # Currently selected entries associated traceback information:
    traceback = Str( connect = 'from: traceback text' )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        Item( 'log_records',
              id         = 'log_records',
              show_label = False,
              editor     = logger_table_editor
        ),
        id = 'etsdevtools.developer.tools.logger'
    )

    options = View(
        Item( 'logging_level',
              width = 100
        ),
        Item( 'max_records',
              label = 'Max # log messages'
        ),
        title   = 'Logger Options',
        id      = 'etsdevtools.developer.tools.logger.options',
        buttons = [ 'OK', 'Cancel' ]
    )

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__ ( self, **traits ):
        self.log_handler = LogHandler( self )
        self.log_handler.setLevel( LevelMap[ self.logging_level ] )
        root_logger = logging.getLogger()
        root_logger.addHandler( self.log_handler )
        super( Logger, self).__init__( **traits )

    #---------------------------------------------------------------------------
    #  Handles the 'logging_level' trait being changed:
    #---------------------------------------------------------------------------

    def _logging_level_changed ( self, logging_level ):
        """ Handles the 'logging_level' trait being changed.
        """
        self.log_handler.setLevel( LevelMap[ logging_level ] )

    #---------------------------------------------------------------------------
    #  Handles the 'max_records' trait being changed:
    #---------------------------------------------------------------------------

    def _max_records_changed ( self, max_records ):
        """ Handles the 'max_records' trait being changed.
        """
        self.log_records = self.log_records[ -max_records: ]

    #---------------------------------------------------------------------------
    #  Handles a new log record being selected:
    #---------------------------------------------------------------------------

    def _selected_changed ( self, record ):
        """ Handles a new log record being selected.
        """
        log_record         = record.log_record
        self.file_position = FilePosition( file_name = log_record.pathname,
                                           line      = log_record.lineno )
        msg = self.formatter.format( log_record )
        col = msg.find( '\n' )
        if col >= 0:
            self.traceback = msg[ col + 1: ]

    #---------------------------------------------------------------------------
    #  Handles a log record being emitted:
    #---------------------------------------------------------------------------

    def emit ( self, log_record ):
        """ Handles a log record being emitted.
        """
        if len( self.log_records ) >= self.max_records:
            del self.log_records[0]
        self.log_records.append( LogRecord( log_record = log_record ) )

#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

view = Logger()

