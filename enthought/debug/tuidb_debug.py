#-------------------------------------------------------------------------------
#  
#  Traits UI DataBase debugger
#  
#  Written by: David C. Morrill
#  
#  Date: 01/16/2006
#  
#  (c) Copyright 2006 by Enthought, Inc.
#  
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:  
#-------------------------------------------------------------------------------

import shelve
import os

from enthought.traits.api \
    import HasPrivateTraits, List, Str, Any, View, Item, Handler, VGroup, \
           HSplit, TableEditor, ValueEditor
    
from enthought.traits.trait_base \
    import traits_home                             
    
from enthought.traits.ui.table_column \
    import ObjectColumn
    
from enthought.traits.ui.menu \
    import NoButtons
    
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
                
table_editor = TableEditor(
    columns      = [ ObjectColumn( name = 'id', editable = False ) ],
    configurable = False,
    editable     = False,
    sortable     = False,
    auto_size    = False,
    on_select    = 'object.select_id'
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
                                           
#-------------------------------------------------------------------------------
#  'TUIDBDebugger' class:  
#-------------------------------------------------------------------------------

class TUIDBDebugger ( Handler ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------
        
    # All items currently in the database:
    all_items = List( TUIDBRecord )
    
    # The value associated with the currently selected traits ui db id:
    value = Any
    
    #---------------------------------------------------------------------------
    #  Trait view definitions:  
    #---------------------------------------------------------------------------
        
    traits_view = View(
        HSplit(
            Item( 'all_items', editor = table_editor, id = 'all_items' ),
            Item( 'value',     editor = ValueEditor() ),
            show_labels = False,
            id          = 'splitter'
        ),
        title     = 'Traits UI DB Debugger',
        id        = 'enthought.debug.tuidb_debug.TUIDBDebugger',
        width     = 0.5,
        height    = 0.3,
        resizable = True,
        buttons   = NoButtons
    )
                 
    #---------------------------------------------------------------------------
    #  Initializes the object:  
    #---------------------------------------------------------------------------
    
    def __init__ ( self, **traits ):
        super( TUIDBDebugger, self ).__init__( **traits )
        self.update_all_items()
        
    #---------------------------------------------------------------------------
    #  Determines the set of available database keys:  
    #---------------------------------------------------------------------------
                
    def update_all_items ( self ):
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
                        
    def select_id ( self, record ):
        """ Handles the user selecting a local variable.
        """
        db = get_ui_db()
        if db is not None:
            self.value = db[ record.id ]
            db.close()
        
#-------------------------------------------------------------------------------
#  Create export objects:
#-------------------------------------------------------------------------------

tuidb_debugger = TUIDBDebugger()

#-------------------------------------------------------------------------------
#  Run the utility:  
#-------------------------------------------------------------------------------
                   
if __name__ == '__main__':
    tuidb_debugger.configure_traits()
