#-------------------------------------------------------------------------------
#  
#  A developer tools demo.
#  
#  Written by: David C. Morrill
#  
#  Date: 02/28/2008
#  
#  (c) Copyright 2008 by Enthought, Inc.
#  
#-------------------------------------------------------------------------------
    
#-------------------------------------------------------------------------------
#  Run the demo:
#-------------------------------------------------------------------------------
        
if __name__ == '__main__':
    import sys
    
    from os.path import split, dirname, abspath

    from enthought.traits.ui.demo.demo import Demo, DemoPath
    
    path, name = split( dirname( abspath( sys.argv[0] ) ) )
    Demo( path = path, 
          root = DemoPath( name = name, use_files = False )
    ).configure_traits() 

