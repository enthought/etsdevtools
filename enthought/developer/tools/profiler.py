#-------------------------------------------------------------------------------
#  
#  Hotshot-based profiling plugin
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

import sys

import enthought.developer.helper.profiler as profiler_module

from types \
    import UnboundMethodType

from enthought.traits.api \
    import HasPrivateTraits, Str, Instance, List, Directory, Bool, Any

from enthought.traits.ui.api \
    import View, HGroup, Item, TableEditor
           
from enthought.traits.ui.table_column \
    import ObjectColumn
    
from enthought.pyface.image_resource \
    import ImageResource
    
from enthought.pyface.dock.features.api \
    import CustomFeature
    
from enthought.pyface.timer.api \
    import do_later
    
from enthought.developer.api \
    import PythonFilePosition, FilePosition, import_module
    
from enthought.developer.helper.profiler \
    import begin_profiling, end_profiling, profile

#-------------------------------------------------------------------------------
#  Profiler table editor definition:
#-------------------------------------------------------------------------------

profiler_table_editor = TableEditor(
    columns = [ ObjectColumn( name     = 'package_name', 
                              label    = 'Package',
                              editable = False ),
                ObjectColumn( name     = 'module_name', 
                              label    = 'Module',
                              editable = False ),
                ObjectColumn( name     = 'class_name',
                              label    = 'Class',
                              editable = False ),
                ObjectColumn( name     = 'method_name',
                              label    = 'Method',
                              editable = False ) ],
    auto_size          = False,
    selection_bg_color = 0xFBD391,
    selection_color    = 'black',
    deletable          = True
)

#-------------------------------------------------------------------------------
#  'Profiler' plugin:
#-------------------------------------------------------------------------------

class Profiler ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'Profiler' )
    
    # The persistence id for this object:
    id = Str( 'enthought.developer.tools.profiler.state', save_state_id = True )
    
    # Custom button used to begin profiling:
    start = Instance( CustomFeature, {
                            'image':   ImageResource( 'start_profiler' ),
                            'click':   'start_profiler',
                            'tooltip': 'Click to being profiling.',
                            'enabled': False
                      },
                      custom_feature = True )
    
    # Custom button used to end profiling:
    stop = Instance( CustomFeature, {
                            'image':   ImageResource( 'stop_profiler' ),
                            'click':   'stop_profiler',
                            'tooltip': 'Click to end profiling.',
                            'enabled': False
                      },
                      custom_feature = True )
                      
    # Current item to be added to the profile:
    profile = Instance( PythonFilePosition,
                        droppable = 'Drop a class or method item here to '
                                    'profile it.',
                        connect   = 'to: class or method item' )
                        
    # The FilePosition of the file used to store the most recent profiling
    # statistics:
    file_position = Instance( FilePosition,
                              draggable = 'Drag profile statistics file name.',
                              connect   = 'from: profile statistics file name' )
                        
    # Current list of methods being profiled:
    profiles = List( save_state = True )
    
    # The directory used to store profiler data files:
    path = Directory( save_state = True )
    
    # Should classes be expanded into individual methods:
    expand_classes = Bool( False, save_state = True )
    
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------
    
    traits_view = View(
        Item( 'profiles',
              id         = 'profiles',
              show_label = False,
              editor     = profiler_table_editor
        ),
        id = 'enthought.developer.tools.profiler'
    )
    
    options = View(
        Item( 'path',
              label = 'Profiler Data Files Path', 
              width = -300
        ),
        '_',
        HGroup(
            Item( 'expand_classes',
                  label = 'Expand classes to show methods'
            ),
            show_left = False
        ),
        title   = 'Profiler Options',
        id      = 'enthought.developer.tools.profiler.options',
        buttons = [ 'OK', 'Cancel' ]
    )
    
    #---------------------------------------------------------------------------
    #  Starts profiling:
    #---------------------------------------------------------------------------

    def start_profiler ( self ):
        """ Starts profiling.
        """
        begin_profiling( self.path )
        self.start.enabled = False
        self.stop.enabled  = True
    
    #---------------------------------------------------------------------------
    #  Stops profiling:
    #---------------------------------------------------------------------------

    def stop_profiler ( self ):
        """ Stops profiling.
        """
        end_profiling()
        self.file_position = FilePosition( 
                                 file_name = profiler_module.profile_name )
        self.stop.enabled  = False
        self.set_start()
        
    #---------------------------------------------------------------------------
    #  Sets the current state of the 'start profiling' button:  
    #---------------------------------------------------------------------------
    
    def set_start ( self ):
        """ Sets the current state of the 'start profiling' button.
        """
        self.start.enabled = (len( self.profiles ) > 0)
    
    #---------------------------------------------------------------------------
    #  Handles the 'profile' trait being changed:  
    #---------------------------------------------------------------------------

    def _profile_changed ( self, file_position ):
        """ Handles the 'profile' trait being changed.
        """
        if file_position is not None:
            do_later( self.set, profile = None )
            if file_position.class_name != '':
                if file_position.method_name != '':
                    self.add_method( file_position )
                else:
                    self.add_class( file_position )
                    
    #---------------------------------------------------------------------------
    #  Adds a new method to the list of profiled methods:  
    #---------------------------------------------------------------------------

    def add_method ( self, file_position ):
        """ Adds a new method to the list of profiled methods.
        """
        # Get the particulars:
        module_name = '%s.%s' % ( file_position.package_name,
                                  file_position.module_name )
        class_name  = file_position.class_name
        method_name = file_position.method_name
        
        # Make sure we are not already profiling it:
        for pm in self.profiles:
            if ((module_name == pm.module_name) and 
                (class_name  == pm.class_name)  and
                (method_name == pm.method_name)):
                return False
                
        module, klass = self.get_module_class( file_position )
        if module is None:
            return False
            
        # Set up the profiler intercept:
        method = self.set_handler( klass, method_name ) 
        if method is None:
            return False
        
        # Add the method to the list of profiled methods:
        self.profiles.append( ProfileMethod( klass = klass, method = method ) )
        
        # Indicate the method was successfully added:
        return True
        
    #---------------------------------------------------------------------------
    #  Adds all of the methods for a class to the list of profiled methods:  
    #---------------------------------------------------------------------------

    def add_class ( self, file_position ):
        """ Adds all of the methods for a class to the list of profiled methods.
        """
        # Get the module and class:                
        module, klass = self.get_module_class( file_position )
        if module is None:
            return False
            
        # Add each method found in the class:
        method_position = PythonFilePosition( **file_position.get(
                              'package_name', 'module_name', 'class_name' ) )
        for name in klass.__dict__.keys():
            if isinstance( getattr( klass, name ), UnboundMethodType ):
                method_position.method_name = name
                self.add_method( method_position )

    #---------------------------------------------------------------------------
    #  Returns the module and class for a specified file position:    
    #---------------------------------------------------------------------------
                
    def get_module_class ( self, file_position ):
        """ Returns the module_name, module and class for a specified file position.
        """
        # Get the full module name:
        module_name = '%s.%s' % ( file_position.package_name,
                                  file_position.module_name )
                
        # Locate the module containing the class:
        module = import_module( module_name )
        if module is None:
            # fixme: Report some kind of an error here...
            return ( None, None )
       
        # Locate the class containing the method:
        klass = getattr( module, file_position.class_name, None )
        if klass is None:
            # fixme: Report some kind of an error here...
            return ( None, None )
        
        # Return the module and class:
        return ( module, klass ) 
        
    #---------------------------------------------------------------------------
    #  Sets up the handler for a specified class's method:  
    #---------------------------------------------------------------------------

    def set_handler ( self, klass, method_name ):
        """ Sets up the handler for a specified class's method.
        """
        method = getattr( klass, method_name, None )
        if method is not None:
            def handler ( *args, **kw ):
                return profile( method, *args, **kw )
            
            setattr( klass, method.__name__, handler )
            return method
            
        # fixme: Report some kind of error here...
        return None
        
    #---------------------------------------------------------------------------
    #  Handles the 'profiles' trait being changed:  
    #---------------------------------------------------------------------------

    def _profiles_changed ( self, profiles ):
        """ Handles the 'profiles' trait being changed.
        """
        for pm in profiles:
            if pm.klass is None:
                # fixme: Need to check for errors in the next two statements...
                module, pm.klass = self.get_module_class( 
                    PythonFilePosition( **pm.get( 'package_name', 'module_name',
                                               'class_name', 'method_name' ) ) )
                pm.method = self.set_handler( pm.klass, pm.method_name )
                
        self.set_start()
                                               
    def _profiles_items_changed ( self, event ):
        """ Handles the 'profiles' trait being changed.
        """
        for pm in event.removed:
            pm.restore()
            
        self.set_start()
        
#-------------------------------------------------------------------------------
#  'ProfileMethod' class:
#-------------------------------------------------------------------------------

class ProfileMethod ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
    
    # The original class the method belongs to:
    klass = Any

    # The original method extracted from the class:
    method = Any
    
    # The name of the associated package:
    package_name = Str
    
    # The name of the associated module:
    module_name = Str
    
    # The name of the associated class:
    class_name = Str
    
    # The name of the associated method:
    method_name = Str
    
    #---------------------------------------------------------------------------
    #  Initializes the object:  
    #---------------------------------------------------------------------------
    
    def __init__ ( self, **traits ):
        """ Initializes the object.
        """
        super( ProfileMethod, self ).__init__( **traits )
        
        module_name = self.klass.__module__
        col = module_name.rfind( '.' )
        if col >= 0:
            self.package_name = module_name[:col]
        self.module_name = module_name[col + 1:]
        self.class_name  = self.klass.__name__
        self.method_name = self.method.__name__
        
    #---------------------------------------------------------------------------
    #  Returns a persistible form of the object state:  
    #---------------------------------------------------------------------------

    def __getstate__ ( self ):
        return self.get( 'package_name', 'module_name', 'class_name',
                         'method_name' )
        
    #---------------------------------------------------------------------------
    #  Restores the original method for a class:  
    #---------------------------------------------------------------------------

    def restore ( self ):
        """ Restores the original method for a class.
        """
        setattr( self.klass, self.method_name, self.method )

#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

view = Profiler()
        
