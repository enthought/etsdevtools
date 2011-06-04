#-------------------------------------------------------------------------------
#
#  Hotshot-based profiling results plugin.
#
#  Written by: David C. Morrill
#
#  Date: 08/05/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import hotshot, hotshot.stats

from os.path \
    import split, splitext

from traits.api \
    import HasPrivateTraits, Str, Instance, List, Int, Float, File, Range, \
           Any, TraitValue, Property, property_depends_on, on_trait_change

from traitsui.api \
    import View, VGroup, Tabbed, Item, TableEditor, ListEditor

from traitsui.table_column \
    import ObjectColumn

from traitsui.table_filter \
    import EvalFilterTemplate, RuleFilterTemplate, MenuFilterTemplate, \
           EvalTableFilter

from pyface.timer.api \
    import do_later

from etsdevtools.developer.api \
    import FilePosition

from etsdevtools.developer.features.api \
    import DropFile

#-------------------------------------------------------------------------------
#  'Stats' class:
#-------------------------------------------------------------------------------

class Stats ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the file containing the code:
    file_name = File

    # The path name of the file:
    path_name = Str

    # The module name of the file:
    module_name = Str

    # The line number of the function:
    line = Int

    # The name of the function:
    function = Str

    # The cumulative number of calls made to the function:
    cumulative_calls = Float

    # The total number of calls made to the function:
    n_calls = Float

    # The total time spent in the function:
    total_time = Float

    # The total time spent per call:
    total_time_per_call = Float

    # The cumulative time spent in the function:
    cumulative_time = Float

    # The cumulative time spent per call:
    cumulative_time_per_call = Float

    #---------------------------------------------------------------------------
    #  Initializes the object:
    #---------------------------------------------------------------------------

    def __init__ ( self, key, value, fraction = 1.0, **traits ):
        super( Stats, self ).__init__( **traits )

        self.file_name, self.line, self.function = key
        self.cumulative_calls, self.n_calls, self.total_time, \
            self.cumulative_time, callers = value
        self.path_name, module_name = split( self.file_name )
        self.module_name = splitext( module_name )[0]

        if self.n_calls > 0:
            self.total_time_per_call = self.total_time / self.n_calls

        if self.cumulative_calls > 0:
            self.cumulative_time_per_call = (self.cumulative_time /
                                             self.cumulative_calls)

        self.cumulative_calls *= fraction
        self.n_calls          *= fraction
        self.total_time       *= fraction
        self.cumulative_time  *= fraction

#-------------------------------------------------------------------------------
#  Static table editor column definition:
#-------------------------------------------------------------------------------

columns = [
    ObjectColumn( name     = 'path_name',
                  label    = 'Path',
                  editable = False ),
    ObjectColumn( name     = 'module_name',
                  label    = 'Module',
                  editable = False ),
    ObjectColumn( name     = 'function',
                  editable = False ),
    ObjectColumn( name     = 'line',
                  editable = False,
                  horizontal_alignment = 'center' ),
]

other_columns = [
    ObjectColumn( name     = 'file_name',
                  label    = 'File Name',
                  editable = False )
]

#-------------------------------------------------------------------------------
#  'StatsCollection' class:
#-------------------------------------------------------------------------------

class StatsCollection ( HasPrivateTraits ):

    # The individual profile statistics records:
    stats = List( Stats )

    # The currently selected stats item:
    selected = Instance( Stats )

    # The maximum number of cumulative calls for all of the stats:
    max_cumulative_calls = Property

    # The maximum number of calls for all of the stats:
    max_n_calls = Property

    # The maximum total time for all of the stats:
    max_total_time = Property

    # The maximum total time per call for all of the stats:
    max_total_time_per_call = Property

    # The maximum cumulative time for all of the stats:
    max_cumulative_time = Property

    # The maximum cumulative time per call for all of the stats:
    max_cumulative_time_per_call = Property

    #-- Traits View Definitions ------------------------------------------------

    def default_traits_view ( self ):
        return View(
            Item( 'stats',
                  show_label = False,
                  editor     = TableEditor(
                      columns = columns + [
                          ObjectColumn(
                              name     = 'cumulative_calls',
                              label    = 'C. Calls',
                              format   = '%.0f',
                              editable = False,
                              maximum  = TraitValue(
                                  delegate = self,
                                  name     = 'max_cumulative_calls' ) ),
                          ObjectColumn(
                              name     = 'n_calls',
                              label    = '# Calls',
                              format   = '%.0f',
                              editable = False,
                              maximum  = TraitValue(
                                  delegate = self,
                                  name     = 'max_n_calls' ) ),
                          ObjectColumn(
                              name     = 'total_time',
                              label    = 'T. Time',
                              format   = '%.5f',
                              editable = False,
                              maximum  = TraitValue(
                                  delegate = self,
                                  name     = 'max_total_time' ) ),
                          ObjectColumn(
                              name     = 'total_time_per_call',
                              label    = 'T. Time/Call',
                              format   = '%.5f',
                              editable = False,
                              maximum  = TraitValue(
                                  delegate = self,
                                  name     = 'max_total_time_per_call' ) ),
                          ObjectColumn(
                              name     = 'cumulative_time',
                              label    = 'C. Time',
                              format   = '%.5f',
                              editable = False,
                              maximum  = TraitValue(
                                  delegate = self,
                                  name     = 'max_cumulative_time' ) ),
                          ObjectColumn(
                              name     = 'cumulative_time_per_call',
                              label    = 'C. Time/Call',
                              format   = '%.5f',
                              editable = False,
                              maximum  = TraitValue(
                                  delegate = self,
                                  name = 'max_cumulative_time_per_call' ) ) ],
                      other_columns      = other_columns,
                      filters            = [ EvalFilterTemplate,
                                             RuleFilterTemplate,
                                             MenuFilterTemplate ],
                      search             = EvalTableFilter(),
                      auto_size          = False,
                      selection_bg_color = 0xFBD391,
                      selection_color    = 'black',
                      selected           = 'selected'
                )
            )
        )

    #-- Property Implementations -----------------------------------------------

    @property_depends_on( 'stats' )
    def _get_max_cumulative_calls ( self ):
        return max( [ stat.cumulative_calls for stat in self.stats ] )

    @property_depends_on( 'stats' )
    def _get_max_n_calls ( self ):
        return max( [ stat.n_calls for stat in self.stats ] )

    @property_depends_on( 'stats' )
    def _get_max_total_time ( self ):
        return max( [ stat.total_time for stat in self.stats ] )

    @property_depends_on( 'stats' )
    def _get_max_total_time_per_call ( self ):
        return max( [ stat.total_time_per_call for stat in self.stats ] )

    @property_depends_on( 'stats' )
    def _get_max_cumulative_time ( self ):
        return max( [ stat.cumulative_time for stat in self.stats ] )

    @property_depends_on( 'stats' )
    def _get_max_cumulative_time_per_call ( self ):
        return max( [ stat.cumulative_time_per_call for stat in self.stats ] )

#-------------------------------------------------------------------------------
#  'ProfilerStats' class:
#-------------------------------------------------------------------------------

class ProfilerStats ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The ProfileViewer object that created this object:
    owner = Any

    # The short name of the file containing the profile statistics being viewed:
    name = Str

    # The name of the file containing the profiler statistics being viewed:
    file_name = File

    # The Hotshot stats object created from the specified file:
    hs_stats = Any

    # The individual profile statistics records:
    stats = Instance( StatsCollection, () )

    # The individual profile statistics records for the currently selected item:
    dd_stats = Instance( StatsCollection, () )

    # Selection history:
    selected_stats = Instance( StatsCollection, () )

    # Dictionary of all functions that call a specified function (closure)
    # (i.e. keys are tuples of the form: ( file, line, function )):
    callers = Any

    # Dictionary of all functions called from a specified function (closure):
    # (i.e. keys are tuples of the form: ( file, line, function )):
    callees = Any

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        Tabbed(
            Item( 'stats',
                  label      = 'Profile',
                  id         = 'stats',
                  style      = 'custom',
                  show_label = False,
                  dock       = 'tab'
            ),
            Item( 'dd_stats',
                  label      = 'Profile For Current Selection',
                  id         = 'dd_stats',
                  style      = 'custom',
                  show_label = False,
                  dock       = 'tab'
            ),
            Item( 'selected_stats',
                  label      = 'Selection History',
                  id         = 'selected_stats',
                  style      = 'custom',
                  show_label = False,
                  dock       = 'tab'
            ),
            id = 'tabbed'
        ),
        id = 'etsdevtools.developer.tools.profile_viewer.ProfilerStats'
    )

    #-- Trait Event Handlers ---------------------------------------------------

    #---------------------------------------------------------------------------
    #  Handles the 'file_name' trait being changed:
    #---------------------------------------------------------------------------

    def _file_name_changed ( self, file_name ):
        """ Handles the 'file_name' trait being changed.
        """
        self.hs_stats = hotshot.stats.load( file_name )
        stats         = [ Stats( key, value )
                          for key, value in self.hs_stats.stats.items() ]
        stats.sort( lambda l, r: cmp( r.cumulative_time, l.cumulative_time ) )
        self.stats.stats = stats[ : self.owner.max_rows ]
        self.compute_callers()
        self.compute_callees()

    #---------------------------------------------------------------------------
    #  Handles the 'selected' trait being changed:
    #---------------------------------------------------------------------------

    @on_trait_change('stats:selected,dd_stats:selected,selected_stats:selected')
    def _selected_changed ( self, stats ):
        """ Handles the 'selected' trait being changed.
        """
        if stats is None:
            return

        # Update the view's export information:
        self.owner.stats_position = FilePosition( file_name = stats.file_name,
                                                  line      = stats.line )

        # Update the selection history:
        file_name = stats.file_name
        line      = stats.line
        for stats2 in self.selected_stats.stats:
            if (file_name == stats2.file_name) and (line == stats2.line):
                break
        else:
            self.selected_stats.stats = \
                (self.selected_stats.stats + [ stats ])[-10:]

        # Provide the detailed 'drill-down' information for the selection:
        self.drill_down( stats )

    #---------------------------------------------------------------------------
    #  Computes the closure of the callers for each function:
    #---------------------------------------------------------------------------

    def compute_callers ( self ):
        """ Computes the closure of the callers for each function.
        """
        self.callers = callers = {}
        stats   = self.hs_stats.stats
        for key, value in stats.items():
            cur_callers = {}
            keys = value[-1].keys()
            while len( keys ) > 0:
                akey = keys.pop()
                if akey not in cur_callers:
                    cur_callers[ akey ] = None
                    if akey in callers:
                        cur_callers.update( callers[ akey ] )
                    else:
                        keys.extend( stats[ akey ][-1].keys() )
            callers[ key ] = cur_callers

    #---------------------------------------------------------------------------
    #  Computes the closure of the callees for each function:
    #---------------------------------------------------------------------------

    def compute_callees ( self ):
        """ Computes the closure of the callees for each function.
        """
        self.callees = callees = {}
        stats   = self.hs_stats.stats
        for key, callers in self.callers.items():
            for caller in callers.keys():
                callees.setdefault( caller, {} )[ key ] = None

    #---------------------------------------------------------------------------
    #  Computes the 'drill-down' information for a specified stats object:
    #---------------------------------------------------------------------------

    def drill_down ( self, stats ):
        """ Computes the 'drill-down' information for a specified stats object.
        """
        # Compute the adjusted fraction of callers for each callee in closure:
        key     = ( stats.file_name, stats.line, stats.function )
        callees = self.callees.get( key, {} ).copy()
        callees[ key ] = 1.0
        for callee, fraction in callees.items():
            if fraction is None:
                self.get_fraction( callee, callees )

        # Compute the set of statistics that apply to just the closure:
        hs_stats = self.hs_stats.stats
        dd_stats = [ Stats( callee, hs_stats[ callee ], fraction )
                     for callee, fraction in callees.items() ]
        dd_stats.sort( lambda l, r: cmp( r.cumulative_time, l.cumulative_time ))
        self.dd_stats.stats = dd_stats[ : self.owner.max_rows ]

    #---------------------------------------------------------------------------
    #  Get the adjusted fraction of calls within a specified closure for a
    #  specified function:
    #---------------------------------------------------------------------------

    def get_fraction ( self, callee, callees ):
        """ Get the adjusted fraction of calls within a specified closure for a
            specified function.
        """
        # fixme: This code does not calculate the correct weighting for graphs
        # with loops. Needs more work...

        # Give it a value, to prevent recursive loop:
        callees[ callee ]  = 1.0
        total   = included = 0.0
        callers = self.hs_stats.stats[ callee ][-1]
        for caller, count in callers.items():
            total += count
            if caller in callees:
                fraction = callees[ caller ]
                if fraction is None:
                    fraction = self.get_fraction( caller, callees )
                included += (fraction * count)
        callees[ callee ] = fraction = (included / total)

        return fraction

#-------------------------------------------------------------------------------
#  'ProfileViewer' plugin:
#-------------------------------------------------------------------------------

class ProfileViewer ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'Profile Viewer' )

    # The persistence id for this object:
    id = Str( 'etsdevtools.developer.tools.profile_viewer.state',
              save_state_id = True )

    # Maximum number of open profiler stats allowed:
    max_stats = Range( 1, 50, 50, mode = 'spinner', save_state = True )

    # Maximum number of profiler rows displayed:
    max_rows = Range( 1, 10000, 1000, mode = 'spinner', save_state = True )

    # Name of the current profile results file to display:
    file_position = Instance( FilePosition,
                        drop_file = DropFile( extensions = [ '.prof' ],
                            tooltip = 'Drop a profile statistics file to '
                                      'analyze it.\nDrag this file.' ),
                        connect = 'to: profiler results file' )

    # Currently selected profiler statistics line file information:
    stats_position = Instance( FilePosition,
             draggable = 'Drag the currently selected statistics file position',
             connect   = 'from: selected profiler statistics entry' )

    # Current list of profile results being viewed:
    stats = List( ProfilerStats )

    #---------------------------------------------------------------------------
    #  Traits view definitions:
    #---------------------------------------------------------------------------

    traits_view = View(
        Item( 'stats@',
              show_label = False,
              editor     = ListEditor( use_notebook = True,
                                       deletable    = True,
                                       page_name    = '.name',
                                       dock_style   = 'tab' )
        )
    )

    options = View(
        Item( 'max_stats',
              label = 'Maximum number of open profiler stats',
              width = -70
        ),
        Item( 'max_rows',
              label = 'Maximum number of table rows displayed',
              width = -70
        ),
        title   = 'Profile Viewer Options',
        id      = 'etsdevtools.developer.tools.profile_viewer.options',
        buttons = [ 'OK', 'Cancel' ]
    )

    #---------------------------------------------------------------------------
    #  Handles the 'file_position' trait being changed:
    #---------------------------------------------------------------------------

    def _file_position_changed ( self, file_position ):
        """ Handles the 'file_position' trait being changed.
        """
        if file_position is not None:
            do_later( self.set, file_position = None )

            # Try to create a new ProfilerStats viewer:
            try:
                p_stats = ProfilerStats( owner     = self,
                                         name      = file_position.name,
                                         file_name = file_position.file_name )
            except:
                return

            stats = self.stats

            # Make sure the # of stats doesn't exceed the maximum allowed:
            if len( stats ) >= self.max_stats:
                del stats[0]

            # Add the new stats to the list of stats (which will cause it to
            # appear as a new notebook page):
            stats.append( p_stats )

    #---------------------------------------------------------------------------
    #  Handles the 'max_stats' trait being changed:
    #---------------------------------------------------------------------------

    def _max_stats_changed ( self, max_inspectors ):
        """ Handles the 'max_stats' trait being changed.
        """
        delta = len( self.stats ) - max_stats
        if delta > 0:
            del self.stats[ : delta ]

#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

view = ProfileViewer()

