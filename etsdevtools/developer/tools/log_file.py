#-------------------------------------------------------------------------------
#
#  Display log messages gleaned from a log file plugin.
#
#  Written by: David C. Morrill
#
#  Date: 01/30/2008
#
#  (c) Copyright 2008 by Enthought, Inc.
#
#-------------------------------------------------------------------------------

""" Display log messages gleaned from a log file plugin.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import wx

from threading \
    import Thread

from time \
    import sleep

from traits.api \
    import HasPrivateTraits, Any, Enum, Instance, List, Range, Str, File, \
           Delegate, Button

from traitsui.api \
    import View, HGroup, Item, TableEditor, CodeEditor, FileEditor, spring

from traitsui.table_column \
    import ObjectColumn

from traitsui.table_filter \
    import TableFilter

from enthought.developer.features.api \
    import DropFile

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# The standard log types:
log_types = set( [ 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' ] )

#-------------------------------------------------------------------------------
#  Trait definitions:
#-------------------------------------------------------------------------------

LogType = Enum( 'Debug', 'Info', 'Warning', 'Error', 'Critical' )

#-------------------------------------------------------------------------------
#  Popup views used by the table editor:
#-------------------------------------------------------------------------------

extra_view = View(
    Item( 'extra',
          style      = 'readonly',
          show_label = False,
          editor     = CodeEditor()
    ),
    kind       = 'popup',
    id         = 'enthought.developer.tools.log_file.extra',
    width      = 0.40,
    height     = 0.30,
    resizable  = True,
    scrollable = True
)

#-------------------------------------------------------------------------------
#  The table editor used to display log records:
#-------------------------------------------------------------------------------

# Mapping of LogRecord types to cell background and text colors:
cell_color_map = {
    'Debug':    wx.WHITE,
    'Info':     wx.WHITE,
    'Warning':  wx.GREEN,
    'Error':    wx.RED,
    'Critical': wx.RED
}

text_color_map = {
    'Debug':    wx.BLACK,
    'Info':     wx.BLACK,
    'Warning':  wx.BLACK,
    'Error':    wx.WHITE,
    'Critical': wx.WHITE
}

class TypeColumn ( ObjectColumn ):

    def get_cell_color ( self, object ):
        return cell_color_map[ object.type ]

    def get_text_color ( self, object ):
        return text_color_map[ object.type ]

log_file_table_editor = TableEditor(
    columns = [ TypeColumn(   name = 'type', width = 0.10,
                              horizontal_alignment = 'center' ),
                ObjectColumn( name = 'date', width = 0.15,
                              horizontal_alignment = 'center' ),
                ObjectColumn( name = 'time', width = 0.15,
                              horizontal_alignment = 'center' ),
                ObjectColumn( name = 'info', width = 0.60, view = extra_view )
              ],
    auto_size           = False,
    editable            = False,
    edit_on_first_click = False,
    show_toolbar        = False,
    filter_name         = 'log_filter',
    selection_bg_color  = 0xFBD391,
    selection_color     = 'black',
)

#-------------------------------------------------------------------------------
#  'LogFilter' class:
#-------------------------------------------------------------------------------

# Log message level mapping:
log_level = {
    'Debug':    0,
    'Info':     1,
    'Warning':  2,
    'Error':    3,
    'Critical': 4
}

class LogFilter ( TableFilter ):

    # The current logging level:
    logging_level = LogType

    #-- TableFilter Method Overrides -------------------------------------------

    def filter ( self, object ):
        """ Returns whether a specified object meets the filter criteria.
        """
        return (log_level[ object.type ] >= log_level[ self.logging_level ])

#-------------------------------------------------------------------------------
#  'LogRecord' class:
#-------------------------------------------------------------------------------

class LogRecord ( HasPrivateTraits ):

    # The type of the log record:
    type = LogType

    # The data on which the log record was created:
    date = Str

    # The time at which the log record was created:
    time = Str

    # The information associated with the log record:
    info = Str

    # The extra (expanded) information associated with the log record:
    extra = Str

#-------------------------------------------------------------------------------
#  'LogFile' class:
#-------------------------------------------------------------------------------

class LogFile ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'LogFile', transient = True )

    # The persistence id for this object:
    id = Str( 'enthought.developer.tools.log_file.state',
              save_state_id = True, transient = True )

    # The name of the log file being processed:
    file_name = File( drop_file = DropFile( extensions = [ '.log' ],
                                      tooltip = 'Drop a log file to display.' ),
                      connect   = 'to', transient = True )

    # The current logging level being displayed:
    logging_level = Delegate( 'log_filter', modify = True )

    # Maximum number of log messages displayed:
    max_records = Range( 1, 10000, 10000, save_state = True )

    # The log record filter:
    log_filter = Instance( LogFilter, (), save_state = True )

    # The current set of log records:
    log_records = List( LogRecord, transient = True )

    # Button used to clear all current log records:
    clear = Button( 'Clear' )

    #-- Private Traits ---------------------------------------------------------

    _lines = Any( [] )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        HGroup(
            Item( 'file_name',
                  id      = 'file_name',
                  springy = True,
                  editor  = FileEditor( entries = 10 )
            ),
            '_',
            Item( 'logging_level' ),
        ),
        '_',
        Item( 'log_records',
              id         = 'log_records',
              show_label = False,
              editor     = log_file_table_editor
        ),
        '_',
        HGroup(
            spring,
            Item( 'clear', show_label = False )
        ),
        title     = 'Log File',
        id        = 'enthought.developer.tools.log_file',
        width     = 0.6,
        height    = 0.5,
        resizable = True
    )

    #-- 'object' Method Overrides ----------------------------------------------

    def __init__ ( self, **traits ):
        """ Initializes the object and starts the background log processing
            thread running.
        """
        self._start_thread()

        super( LogFile, self).__init__( **traits )

    #-- HasTraits Method Overrides ---------------------------------------------

    def copyable_trait_names ( self, **metadata ):
        """ Returns the list of trait names to copy or clone by default.
        """
        return [ 'log_filter', 'max_records' ]

    #-- Trait Event Handlers ---------------------------------------------------

    def _clear_changed ( self ):
        self.log_records = []

    #-- Private Methods --------------------------------------------------------

    def _start_thread ( self ):
        """ Starts the background log processing thread running.
        """
        thread = Thread( target = self._process_log )
        thread.setDaemon( True )
        thread.start()

    def _process_log ( self ):
        """ Processes the current log file.
        """
        file_name = ''
        fh        = None
        while True:
            if file_name != self.file_name:
                file_name = self.file_name

                try:
                    if fh is not None:
                        fh.close()
                except:
                    pass

                fh   = None
                data = ''
                self.log_records = []
                try:
                    fh = open( file_name, 'rb' )
                except:
                    pass

            if fh is not None:
                new_data = fh.read()
                if new_data == '':
                    continue

                data += new_data
                col   = data.rfind( '\n' )
                if col < 0:
                    continue

                self._lines.extend( data[ : col ].split( '\n' ) )
                data = data[ col + 1: ].lstrip()

                records = []
                while True:
                    record = self._next_record()
                    if record is None:
                        break

                    records.insert( 0, record )

                if len( records ) > 0:
                    self.log_records = \
                        (records + self.log_records)[ : self.max_records ]

            sleep( 1 )

    def _next_record ( self ):
        """ Returns the next LogRecord or None if no complete log record is
            found.
        """
        lines = self._lines
        if len( lines ) == 0:
            return None

        type, date_time, info = lines[0].split( '|', 2 )
        type       = type.capitalize()
        date, time = date_time.split()
        info       = info.strip()
        extra      = ''
        for i in range( 1, len( lines ) ):
            line = lines[i]
            col  = line.find( '|' )
            if (col > 0) and (line[ :col ] in log_types):
                extra = '\n'.join( lines[ 1: i ] )
                del lines[ 0: i ]
                break
        else:
            return None

        return LogRecord( type  = type, date = date, time = time, info = info,
                          extra = extra )

    #---------------------------------------------------------------------------
    #  Handles the 'max_records' trait being changed:
    #---------------------------------------------------------------------------

    def _max_records_changed ( self, max_records ):
        """ Handles the 'max_records' trait being changed.
        """
        self.log_records = self.log_records[ -max_records: ]

#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

view = LogFile()

#-------------------------------------------------------------------------------
#  Handle being invoked from the command line:
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    import sys

    if len( sys.argv ) >= 3:
        print 'Usage is: log_file log_file_name'
        sys.exit(1)

    file_name = ('C:\\Documents and Settings\\dmorrill\\Application Data\\'
                 'Enthought\\enthought.vms\\ets.log')
    if len( sys.argv ) >= 2:
        file_name = sys.argv[1]

    view.file_name = file_name
    view.configure_traits( filename = 'log_file.cfg' )

