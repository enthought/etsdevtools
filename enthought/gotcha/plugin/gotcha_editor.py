
#### FIXME : Organize these imports!!!!

# Major package imports.
import os
import os.path
import wx

from copy                        import deepcopy
from enthought.gotcha.hotshot_info import HotShotInfo
from enthought.util.numerix      import *
from enthought.chaco.wx.plot     import *
from enthought.chaco.plot_overlay_style import PlotOverlayStyle
from enthought.chaco.plot_style  import PlotStyle
from enthought.chaco.plot_title_style import PlotTitleStyle
from enthought.enable            import Scrolled
from enthought.pyface.api            import MessageDialog
from enthought.traits.api            import Any, File, HasTraits, Instance, Range
from enthought.traits.ui.api         import View
from enthought.enable.wx         import Window

from enthought.envisage.ui       import Editor




try:
    import ctypes
    ul = ctypes.c_ulong( 0 )
    ctypes.windll.kernel32.QueryPerformanceFrequency( ctypes.byref( ul ) )
    frequency = float( ul.value ) 
    
    def as_seconds ( n ):
        global frequency
    
        return '%.4f' % (n / frequency)
    
except:
    def as_seconds ( n ):
        return commatize( n )


# Colors used for labels and bars:
cur_color = 0xD0D0D0FF
colors    = [ 0xFFB0FFFF, 0xB0FFFFFF, 0xFFFFB0FF, 0xFFD0D0FF, 0xD0D0FFFF, 0xB0FFB0FF ]

# Common PlotGroup trait values:
group_traits = {
   'orientation':          'v',
   'index_axis':           'y',
   'plot_origin':          'top left',
   'bg_color':             0xF0F0E0FF
} 

overlay_style = PlotOverlayStyle(
    line_color = 'clear',
    position = 'left',
    padding = 0,
    margin_width = 5,
    border_size = 0,
    bg_color = 'clear'
)

title_style = PlotTitleStyle(
    margin_height = 4,
    padding_height = 4,
    padding_width = 8,
    bg_color = 'cyan',
    border_size = 1,
)

callee_style = PlotStyle(
    plot_bar_width = 100.0,
    plot_border_size = 0,
    plot_bg_color = 'clear',
)

class GotchaEditor(Editor):
    """ Envisage editor for viewing Gotcha results. """

    cutoff  = Range( 0.0, 30.0, 20.0, desc = 'the cutoff percentage' )
    cur_file = File
    info = Instance(HotShotInfo)
    file_cache = Any
    all_title = Instance(PlotTitle)
    cur_title = Instance(PlotTitle)
    all_callees = Instance(PlotCanvas)
    cur_callees = Instance(PlotCanvas)
    cur_list = Any

    traits_view = View('cutoff')

    #### 'Window' interface ###################################################
    title = 'Gotcha Profile'
    
    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, filename, **traits):

        super(GotchaEditor, self).__init__(**traits)

        self.cur_file = filename
        self.title = 'Gotcha Profile - %s' % filename

    ###########################################################################
    # 'Window' interface.
    ###########################################################################

    def _create_contents ( self, parent ):

        # Create the main panel.
        main_panel = wx.Panel( parent, -1 )
        main_sizer = wx.BoxSizer( wx.HORIZONTAL )
        main_panel.SetSizer(main_sizer)
        main_panel.SetAutoLayout(True)

        # Set up a splitter control:
        self._swv = swv = wx.SplitterWindow( main_panel, -1 )
        main_sizer.Add(swv, 1, wx.ALL | wx.EXPAND)
        _top = self._create_top_panel(swv)
        _bottom =self._create_bottom_panel(swv)
        swv.SplitHorizontally(_top, _bottom)

        main_sizer.Fit(main_panel)
        main_sizer.Layout()
        
        return main_panel

    ###########################################################################
    # Private 'GotchaEditor' interface.
    ###########################################################################

    def _create_top_panel( self, parent ):

        self._swh = swh = wx.SplitterWindow( parent, -1 )

        self._stack = stack = wx.ListBox( swh, -1, style = wx.LB_SINGLE )
        wx.EVT_LISTBOX( parent, stack.GetId(), self.on_stack_select )

        plots = self._create_plots( swh )

        swh.SplitVertically(stack, plots, -100)

        return swh


    def _create_top_panel( self, parent ):

        self._swh = swh = wx.SplitterWindow( parent, -1 )

        self._stack = stack = wx.ListBox( swh, -1, style = wx.LB_SINGLE )
        wx.EVT_LISTBOX( parent, stack.GetId(), self.on_stack_select )   ### ???

        plots = self._create_top_right( swh )

        swh.SplitVertically(stack, plots, -100)

        return swh

    def _create_top_right( self, parent ):

        panel = wx.Panel( parent, -1 )
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)
        
        plots = self._create_plots(panel)
        sizer.Add(plots, 1, wx.ALL | wx.EXPAND)

        range_slider = self.edit_traits(parent=panel, kind='subpanel')
        sizer.Add(range_slider.control, 0, wx.ALL | wx.EXPAND)
        sizer.Fit(panel)
        sizer.Layout()
        
        return panel


    def _create_bottom_panel( self, parent ):

        font = wx.Font( 9, wx.MODERN, wx.NORMAL, wx.NORMAL )
        self._source = source = wx.ListBox( parent, -1, style = wx.LB_SINGLE )
        source.SetFont( font )

        return source

    def _create_plots( self, parent ):

        panel = wx.Panel( parent, -1 )
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)
        
        self._cur_plot = cur_plot = self._create_current_caller_plot()
        self._all_plot = all_plot = self._create_all_callee_plot()

        group = PlotGroup(cur_plot, all_plot, bg_color='red')
        scrolled = Scrolled(component=PlotComponent(group))
        window = Window(panel, component=scrolled)
        sizer.Add(window.control, 1, wx.EXPAND)

        sizer.Layout()

        return panel

    #---------------------------------------------------------------------------
    #  Handle the user clicking in the 'direct callees' plot window:
    #---------------------------------------------------------------------------
    
    def on_cur_click ( self, event ):
        ignore, index, ignore = self.cur_callees[0].map_xy( event.x, event.y )
        index    = int( index + 0.5 )
        cur_list = self.cur_list
        if index < len( cur_list ):
            self.push_stack( cur_list[ index ] )
       
    #---------------------------------------------------------------------------
    #  Show an error message:
    #---------------------------------------------------------------------------
    
    def show_error ( self, msg ):
        dlg = MessageDialog( None, str( msg ), 'Gotcha Error' )

    #---------------------------------------------------------------------------
    #  Initialize the stack view to the 'root' entry:
    #---------------------------------------------------------------------------
    
    def init_stack ( self ):
        self.file_cache = {}
        stack = self._stack
        stack.Clear()
        stack.Append( '<root>', self.info.root )
        stack.SetSelection( 0 )
        self.on_stack_select()
       
    #---------------------------------------------------------------------------
    #  Push a specified function call entry onto the stack:
    #---------------------------------------------------------------------------
    
    def push_stack ( self, info ):
        if ((not isinstance( info, FakeFunctionNode )) and
            (len( info.callees() ) > 0)):
            stack = self._stack
            stack.Append( info.label( include_filename = True ), info )
            stack.SetSelection( stack.GetCount() - 1 )
            self.on_stack_select()
       
    #---------------------------------------------------------------------------
    #  Handle a new stack entry being selected: 
    #---------------------------------------------------------------------------
    
    def on_stack_select ( self, event = None ):
        stack      = self._stack
        selection  = stack.GetSelection()
        info       = stack.GetClientData( selection )
        selection += 1
        for i in range( stack.GetCount() - selection ):
            stack.Delete( selection )
 
        # Clear the 'all called functions' plot:
        self.all_title.text = 'All functions called from ' + info.label()
        all_callees         = self.all_callees
        del all_callees[:]
        del all_callees.overlays[:] 
 
        # Clear the 'current called functions' plot:
        self.cur_title.text = ('Functions called directly from ' + 
                               info.label())
        cur_callees = self.cur_callees
        del cur_callees[:]
        del cur_callees.overlays[:] 
 
        # Update the 'current called functions' plot:
        ###include_filename = self.menu_filename.checked()
        include_filename = False
        callees          = info.callees().values()
        total_time       = info.total_time()
        callees.sort( lambda l, r: cmp( r.total_time(), l.total_time() ) )
        self.cur_list = callees = [ FakeFunctionNode( info ) ] + callees
        w_value  = PlotValue( map( lambda x: x.total_time() * 
                                   (len( x.callees() ) > 0), callees ),
                              fill_color = 0xFFFFB0FF,
                              style=callee_style)
        wo_value = PlotValue( map( lambda x: x.total_time() * 
                                   (len( x.callees() ) == 0), callees ),
                              fill_color = 0xC0FFC0FF,
                              style=callee_style)
        cur_callees.add( w_value, wo_value )
        i = 0
        for callee in callees:
            tt = callee.total_time()
            w_value.add( PlotOverlay( '%.1f%% %s (%s: %s)' % ( 
                            (100.0 * tt) / total_time, 
                            callee.label( include_filename = include_filename ), 
                            commatize( callee.calls ), as_seconds( tt ) ),
                            index        = i,
                            legend_color = color_for( callee, i ),
                            style        = overlay_style ) )
            i += 1
        cur_callees.plot_min_height = len( callees ) * 26
        
        # Update the 'all called functions' plot:
        all = info.all().values() + [ [ info.id, info.calls, info.in_func ] ]
        all.sort( lambda l, r: cmp( r[2], l[2] ) )
        cutoff = long( (all[0][2] * self.cutoff) / 100 )
        all    = filter( lambda x: x[2] >= cutoff, all )
        if len( all ) == 1:
            all.append( [ ( 0, 0 ), -1, -1 ] )
        
        all_callees.index = xx = PlotValue( arange( float( len( all ) ) ) )
        first = True
        i     = -1
        for callee in callees:
            i         += 1
            callee_all = callee.all()
            if len( callee_all ) == 0:
                continue
            data = []
            for item in all:
                data.append( float( (callee_all.get( item[0], None ) or 
                                     [ None, 0, 0 ])[2] ) )
            data = array( data )
            if alltrue( data == 0.0 ):
                continue
            value = PlotValue( array( data ), 
                               fill_color = color_for( callee, i ),
                               style=callee_style)
            all_callees.add( value )
            if first:
                first = False
                j     = 0
                for item in all:
                    if item[1] >= 0:
                        value.add( PlotOverlay( '%.1f%% %s (%s: %s)' % ( 
                                   (100.0 * item[2]) / total_time,
                                   info.label( item[0], 
                                       include_filename = include_filename ), 
                                   commatize( item[1] ), as_seconds( item[2] )), 
                                   index = j,
                                   style = overlay_style ) )
                    j += 1
        all_callees.plot_min_height = len( all ) * 26
            
        self.update()
        
        self.show_source( info )
       
    
    def _cutoff_changed ( self, old, new ):
        """ Called when the cutoff trait changes. """
        
        self.on_stack_select()
        
    def show_source ( self, info ):
        """ Show the source associated with a specified profile entry. """
        source = self._source
        source.Clear()
        lines = self.info.source_for( info.filename() )
        if len( lines ) > 0:
            n     = len( str( len( lines ) ) )
            lines = map( lambda x, y: '%s: %s' % ( str( x ).rjust( n ), y ),
                         range( 1, len( lines ) + 1 ), lines )
            source.InsertItems( lines, 0 )
            source.SetFirstItem( info.lineno() - 1 )
    
    #---------------------------------------------------------------------------
    #  Handle an update request:
    #---------------------------------------------------------------------------
 
    def update ( self ):
        
        self._cur_plot.update()
        self._all_plot.update()
        
           
    #---------------------------------------------------------------------------
    #  Handle the user exiting the plot test window:
    #---------------------------------------------------------------------------
 
    def on_exit ( self ):
        self.on_close()

    #---------------------------------------------------------------------------
    #  Handle the user closing the plot test window:
    #---------------------------------------------------------------------------
 
    def on_close ( self, event = None ):
        self.save_state()
        self.Destroy()
         
    def _create_current_caller_plot( self ):

        # Initialize the current caller's canvas:
        group = PlotGroup( **group_traits )
        group.axis_index   = PlotAxis( visible = False )
        self.cur_callees = PlotCanvas( plot_type       = 'stackedbar',
                                       plot_border_size = 0,
                                       plot_bg_color   = 'clear',
                                       plot_line_color = ( .75, .75, .75, 1. ),
                                       overlay_font    = 'Arial 9',
                                       weight          = 0.000001 )
        self.cur_callees.axis = PlotAxis(
            visible      = False,
            position     = 'left',
            label_format = lambda x: ('%gK' % (x / 1000)).strip()
        )
        self.cur_callees.on_trait_change( self.on_cur_click, 'left_up' )
        self.cur_title = PlotTitle( bg_color = cur_color,
                                    style = title_style )
        self.cur_callees.add( self.cur_title )
        group.add( self.cur_callees, PlotCanvas( plot_border_size = 0,
                                                 plot_min_height  = 0,
                                                 plot_bg_color    = 'clear') )

        return group
        return PlotComponent(group)

    def _create_all_callee_plot( self ):

        # Initialize the all callees canvas.
        group = PlotGroup( **group_traits )
        group.axis_index   = PlotAxis( visible = False )
        self.all_callees = PlotCanvas( plot_type       = 'stackedbar',
                                       plot_border_size     = 0,
                                       border_color    = 0x00000000,
                                       plot_bg_color   = 'clear',
                                       plot_bar_width  = 100.0,
                                       plot_line_color = ( .75, .75, .75, 1. ),
                                       overlay_font    = 'Arial 9',
                                       weight          = 0.000001 )  
        self.all_callees.axis = PlotAxis(
            visible      = False,
            position     = 'both',
            label_format = lambda x: ('%gK' % (x / 1000)).strip()
        )
        self.all_title = PlotTitle( style = title_style )
        self.all_callees.add( self.all_title )                                              
        group.add( self.all_callees, PlotCanvas( plot_border_size = 0,
                                                 plot_min_height  = 0,
                                                 plot_bg_color    = 'clear') )

        return group
        return PlotComponent(group)

    def _cur_file_changed(self):
        """ Called when the current file changes. """
        
        try:
            if self.cur_file is not None:
                self.info = HotShotInfo( self.cur_file )
                # self.init_stack()
        except Exception, excp:
            import traceback
            traceback.print_exc()
            self.show_error(excp)
        
        return

    def _opened_changed(self):
        """ Called after the window is opened. """

        Editor._opened_changed(self)
        self.init_stack()
        
        return


class FakeFunctionNode:
          
   def __init__ ( self, real_node ):
       self.id = id        = real_node.id
       self.calls          = real_node.calls
       self._total_time    = real_node.in_func
       self._label_without = real_node.label()
       self._label_with    = real_node.label( include_filename = 1 )
       self._all = all     = deepcopy( real_node.all() )
       entry = all.get( id, None )
       if entry is None:
           all[ id ] = entry = [ id, 0, 0 ]
       entry[1] += 1
       entry[2] += real_node.in_func
       for callee in real_node.callees().values():
           for id, calls, in_func in callee.all().values():
               entry     = all[ id ]
               entry[1] -= calls
               entry[2] -= in_func
               
   def callees ( self ):
       return {}
       
   def label ( self, include_filename = 0 ):
       if include_filename:
           return self._label_with
       return self._label_without
   
   def total_time ( self ):
       return self._total_time
   
   def all ( self ):
       return self._all

#-------------------------------------------------------------------------------
#  Return the color to use for a specified profile entry:
#-------------------------------------------------------------------------------

def color_for ( info, i ):
    if isinstance( info, FakeFunctionNode ):
        return cur_color
    return colors[ i % len( colors ) ]
    
#-------------------------------------------------------------------------------
#  Return a number with commas (e.g. '10,000,000'):
#-------------------------------------------------------------------------------
    
def commatize ( n ):
    result = ''
    n      = str( n )
    while len( n ) > 3:
        result = ',%s%s' % ( n[-3:], result )
        n      = n[:-3]
    return n + result

#### EOF ######################################################################
