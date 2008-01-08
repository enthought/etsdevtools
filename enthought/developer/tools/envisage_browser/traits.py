#-------------------------------------------------------------------------------
#  
#  Trait definitions for use with the Envisage plugin definition browser
#  
#  Written by: David Morrill
#  
#  Date: 06/16/2006
#  
#  (c) Copyright 2006 by David C. Morrill
#  
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from os \
    import access, R_OK
    
from enthought.traits.api \
    import TraitHandler, TraitFactory
    
#-------------------------------------------------------------------------------
#  'TextFile' trait:
#-------------------------------------------------------------------------------

def TextFile ( default = '', **metadata ):
    return Trait( default, trait_text_file, **metedata )
    
TextFile = TraitFactory( TextFile )

    
class TraitTextFile ( TraitHandler ):
    is_mapped = True

    def validate ( self, object, name, value ):
        if access( value, R_OK ):
            return value
            
        self.error( object, name, self.repr( value ) )

    def mapped_value ( self, value ):
        fh = None
        try:
            fh     = file( value, 'rb' )
            mapped = fh.read()
        finally:
            if fh is not None:
                fh.close()
                
        return mapped

    def post_setattr ( self, object, name, value ):
        try:
            setattr( object, name + '_', self.mapped_value( value ) )
        except:
            raise TraitError

    def info ( self ):
        return 'a file name with read access'

    def get_editor ( self, trait ):
        from enthought.traits.ui.api import FileEditor
        return FileEditor()

# Create a resusable instance:        
trait_text_file = TraitTextFile()        
