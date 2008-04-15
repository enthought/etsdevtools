#-------------------------------------------------------------------------------
#  
#  Python source file syntax checker plugin.
#  
#  Written by: David C. Morrill
#  
#  Date: 07/08/2006
#  
#  (c) Copyright 2006 by David C. Morrill
#  
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from exceptions \
    import SyntaxError

from os.path \
    import exists
    
from enthought.traits.api \
    import File, Int, Str, Bool, false, Button
    
from enthought.traits.ui.api \
    import View, VGroup, HGroup, Item, CodeEditor, spring
    
from enthought.pyface.timer.api \
    import do_after
    
from enthought.developer.features.api \
    import DropFile
    
from enthought.developer.api \
    import Saveable, read_file, file_watch
     
from enthought.developer.helper.themes \
    import TTitle
    
#-------------------------------------------------------------------------------
#  'SyntaxChecker' class:
#-------------------------------------------------------------------------------

class SyntaxChecker ( Saveable ):
    
    #---------------------------------------------------------------------------
    #  Trait definitions:  
    #---------------------------------------------------------------------------

    # The name of the plugin:
    name = Str( 'Syntax Checker' )
    
    # The persistence id for this object:
    id = Str( 'enthought.developer.tools.syntax_checker.state',
              save_state_id = True )
    
    # Should the syntax checker automatically go to the current syntax error?
    auto_goto = Bool( False, save_state = True )
    
    # Should a changed file be automatically reloaded:
    auto_load = Bool( True, save_state = True )
    
    # The name of the file currently being syntax checked:
    file_name = File( drop_file = DropFile( extensions = [ '.py' ],
                                    draggable = True,
                                    tooltip   = 'Drop a Python source file to '
                                          'syntax check it.\nDrag this file.' ),
                      connect   = 'to' )
    
    # The current source code being syntax checked:
    source = Str
    
    # The current syntax error message:
    error = Str
    
    # Current error line:
    error_line = Int
    
    # Current error column:
    error_column = Int
    
    # Current editor line:
    line = Int
    
    # Current editor column:
    column = Int
    
    # 'Go to' button:
    go_to = Button( 'Go To' )
    
    # Can the current file be saved?
    can_save = false
    
    #---------------------------------------------------------------------------
    #  Traits view definitions:  
    #---------------------------------------------------------------------------

    traits_view = View(
        VGroup(
            TTitle( 'file_name' ), 
            Item( 'source@',
                  editor = CodeEditor( selected_line = 'line' ) ),
            TTitle( 'error' ),
            HGroup(
                spring,
                Item( 'go_to', 
                      show_label   = False,
                      enabled_when = '(error_line > 0) and (not auto_goto)' ),
            ),
            show_labels = False
        ),
        title = 'Syntax Checker'
    )
    
    options = View(
        VGroup(
            Item( 'auto_goto',
                  label = 'Automatically move cursor to syntax error'
            ),
            Item( 'auto_load',
                  label = 'Automatically reload externally changed files'
            ),
            show_left = False
        ),
        title   = 'Syntax Checker Options',
        id      = 'enthought.developer.tools.syntax_checker.options',
        buttons = [ 'OK', 'Cancel' ]
    )
        
    #---------------------------------------------------------------------------
    #  Handles the 'auto_goto' trait being changed:  
    #---------------------------------------------------------------------------

    def _auto_goto_changed ( self, auto_goto ):
        """ Handles the 'auto_goto' trait being changed.
        """
        if auto_goto and (self.error_line > 0):
            self._go_to_changed()
    
    #---------------------------------------------------------------------------
    #  Handles the 'Go To' button being clicked:  
    #---------------------------------------------------------------------------

    def _go_to_changed ( self ):
        """ Handles the 'Go To' button being clicked.
        """
        self.line   = self.error_line
        self.column = self.error_column
    
    #---------------------------------------------------------------------------
    #  Handles the 'file_name' trait being changed:  
    #---------------------------------------------------------------------------

    def _file_name_changed ( self, old_name, new_name ):
        """ Handles the 'file_name' trait being changed.
        """
        self._set_listener( old_name, True )
        self._set_listener( new_name, False )
        self._load_file_name( new_name )
        
    #---------------------------------------------------------------------------
    #  Handles the 'source' trait being changed:  
    #---------------------------------------------------------------------------

    def _source_changed ( self, source ):
        """ Handles the 'source' trait being changed.
        """
        if self.can_save:
            if not self._dont_update:
                self.needs_save = True
                do_after( 750, self._syntax_check )
            else:
                self._syntax_check()
            
    #---------------------------------------------------------------------------
    #  Handles the current file being updated:  
    #---------------------------------------------------------------------------

    def _file_changed ( self, file_name ):
        """ Handles the current file being updated.
        """
        if self.auto_load:
            self._load_file_name( file_name )
                
    #---------------------------------------------------------------------------
    #  Sets up/Removes a file watch on a specified file:  
    #---------------------------------------------------------------------------

    def _set_listener ( self, file_name, remove ):
        """ Sets up/Removes a file watch on a specified file.
        """
        if exists( file_name ):
            file_watch.watch( self._file_changed, file_name, remove = remove )
    
    #---------------------------------------------------------------------------
    #  Loads a specified source file:
    #---------------------------------------------------------------------------

    def _load_file_name ( self, file_name ):
        """ Loads a specified source file.
        """
        self._dont_update = True
        self.can_save = True
        source        = read_file( file_name )
        if source is None:
            self.error    = 'Error reading file'
            self.can_save = False
            source     = ''
        self.source = source
        self._dont_update = False
        self.needs_save   = False
            
    #---------------------------------------------------------------------------
    #  Checks the current source for syntax errors:  
    #---------------------------------------------------------------------------

    def _syntax_check ( self ):
        """ Checks the current source for syntax errors.
        """
        try:
            compile( self.source.replace( '\r\n', '\n' ),
                     self.file_name, 'exec' )
            self.error      = 'Syntactically correct'
            self.error_line = 0
        except SyntaxError, excp:
            self.error_line   = excp.lineno
            self.error_column = excp.offset + 1
            self.error        = '%s on line %d, column %d' % ( 
                                excp.msg, excp.lineno, self.error_column )
            if self.auto_goto:
                self._go_to_changed()
            
    #---------------------------------------------------------------------------
    #  Saves the current source back to the associated file:  
    #---------------------------------------------------------------------------

    def save ( self ):
        """ Saves the current source back to the associated file.
        """
        fh = None
        try:
            fh = file( self.file_name, 'wb' )
            fh.write( self.source )
            fh.close()
            self.needs_save = False
        except:
            if fh is not None:
                try:
                    fh.close()
                except:
                    pass
    
#-------------------------------------------------------------------------------
#  Create exported objects:
#-------------------------------------------------------------------------------

view = SyntaxChecker()

