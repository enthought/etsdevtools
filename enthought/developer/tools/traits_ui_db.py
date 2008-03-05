#-------------------------------------------------------------------------------
#  
#  Traits UI DataBase browser
#  
#  Written by: David C. Morrill
#  
#  Date: 07/14/2006
#  
#  (c) Copyright 2006 by David C. Morrill
#  
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:  
#-------------------------------------------------------------------------------

import shelve
import os

from enthought.traits.api \
    import HasPrivateTraits, List, Str, Any, Instance, Bool, Button

from enthought.traits.ui.api \
    import View, VGroup, HGroup, Item, ValueEditor, TabularEditor, spring

from enthought.traits.ui.tabular_adapter \
    import TabularAdapter
    
from enthought.traits.trait_base \
    import traits_home                             
    
from enthought.developer.api \
    import file_watch, HasPayload
    
#-------------------------------------------------------------------------------
#  Returns the name of the traits UI database:  
#-------------------------------------------------------------------------------
        
def ui_db_name ( ):
    """ Returns the name of the traits UI database.
    """
    return os.path.join( traits_home(), 'traits_ui' )
    
#-------------------------------------------------------------------------------
#  Opens the traits UI database:  
#-------------------------------------------------------------------------------
        
def get_ui_db ( mode = 'r' ):
    """ Opens the traits UI database.
    """
    try:
        return shelve.open( ui_db_name(), flag = mode, protocol = -1 )
    except:
        return None
        
#-------------------------------------------------------------------------------
#  Table editor definition:  
#-------------------------------------------------------------------------------

class TraitsUIDBAdapter ( TabularAdapter ):
    columns = [ ( 'Id', 'id' ) ]

table_editor = TabularEditor(
    selected   = 'selected',
    editable   = False,
    adapter    = TraitsUIDBAdapter(),
    operations = []
)

#-------------------------------------------------------------------------------
#  'TUIDBRecord' class:  
#-------------------------------------------------------------------------------

class TUIDBRecord ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
        
    # Id of the database entry:
    id = Str
    
    #---------------------------------------------------------------------------
    #  Deletes the 'id' from the traits UI data base:  
    #---------------------------------------------------------------------------

    def delete ( self ):
        """ Deletes the 'id' from the traits UI data base.
        """
        db = get_ui_db( mode = 'c' )
        if db is not None:
            del db[ self.id ]
            db.close()

#-------------------------------------------------------------------------------
#  'TraitsUIDB' class:  
#-------------------------------------------------------------------------------

class TraitsUIDB ( HasPrivateTraits ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
     
    # The name of the plugin:
    name = Str( 'Traits UI DB' )
    
    # All items currently in the database:
    all_items = List( TUIDBRecord )
    
    # The value associated with the currently selected traits ui db id:
    value = Instance( HasPayload,
                      connect   = 'from: current selected value',
                      draggable = 'Drag current selected value.' )
    
    # The currently selected traits ui db row:
    selected = Any
    
    # The 'Delete selected id' button:
    delete = Button( 'Delete' )
    
    # Has the UI been initialized yet?
    initialized = Bool( False )
    
    #---------------------------------------------------------------------------
    #  Trait view definitions:  
    #---------------------------------------------------------------------------
        
    traits_view = View(
        VGroup(
            Item( 'all_items',
                  show_label = False,
                  editor     = table_editor,
                  id         = 'all_items'
            ),
            HGroup( 
                spring,
                Item( 'delete', 
                      show_label   = False,
                      enabled_when = 'selected is not None'
                )
            )
        ),
        title     = 'Traits UI DB',
        id        = 'enthought.developer.tools.traits_ui_db',
        width     = 0.40,
        height    = 0.50,
        resizable = True
    )
                 
    #---------------------------------------------------------------------------
    #  Initializes the object:  
    #---------------------------------------------------------------------------
    
    def __init__ ( self, **traits ):
        super( TraitsUIDB, self ).__init__( **traits )
        self.update_all_items()
        
    #---------------------------------------------------------------------------
    #  Determines the set of available database keys:  
    #---------------------------------------------------------------------------
                
    def update_all_items ( self, file_name = None ):
        """ Determines the set of available database keys.
        """
        db = get_ui_db()
        if db is not None:
            keys = db.keys()
            db.close()
            keys.sort()
            self.all_items = [ TUIDBRecord( id = key ) for key in keys ] 
            
    #---------------------------------------------------------------------------
    #  Handles the user selecting a data base id from the table:
    #---------------------------------------------------------------------------
                        
    def _selected_changed ( self, record ):
        """ Handles the user selecting a local variable.
        """
        # Only set up the file watch when a UI is actually active:
        if not self.initialized:
            self.initialized = True
            file_watch.watch( self.update_all_items, ui_db_name() )
            
        if record is not None:
            # Display the contents of the selected data base record:
            db = get_ui_db()
            if db is not None:
                id = record.id
                self.value = HasPayload( payload      = db[ id ],
                                         payload_name = id.split( '.' )[-1],
                                         payload_full_name = id )
                db.close()
        else:
            self.value = None
            
    def _delete_changed ( self ):
        """ Handles the 'delete' button being clicked.
        """
        self.all_items.remove( self.selected )
        self.selected = None
            
    #---------------------------------------------------------------------------
    #  Handles items being deleted from the 'all_items' list:  
    #---------------------------------------------------------------------------
    
    def _all_items_items_changed ( self, event ):
        """ Handles items being deleted from the 'all_items' list.
        """
        for record in event.removed:
            record.delete()
        
#-------------------------------------------------------------------------------
#  Create export objects:
#-------------------------------------------------------------------------------

view = TraitsUIDB()

# Run the tool (if invoked from the command line):
if __name__ == '__main__':
    view.configure_traits()

