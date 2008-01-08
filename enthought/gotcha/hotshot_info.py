#-------------------------------------------------------------------------------
#  
#  Process the contents of a HotShot profiler generated data file into a format  
#  that can be used by Gotcha!.
#  
#  Written by: David C. Morrill (based on the hotshot/log.py file)
#  
#  Date: 03/03/2003
#  
#  (c) Copyright 2003 by Enthought, Inc. 
#  
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import _hotshot
import os.path
import parser
import symbol

from _hotshot import WHAT_ENTER, WHAT_EXIT, WHAT_LINENO, WHAT_DEFINE_FILE, \
                     WHAT_DEFINE_FUNC, WHAT_ADD_INFO

#-------------------------------------------------------------------------------
#  'HotShotInfo' class:
#-------------------------------------------------------------------------------

class HotShotInfo:
    
    def __init__ ( self, logfn ):
        # fileno -> filename
        self._filemap = {}
        # (fileno, lineno) -> filename, funcname
        self._funcmap = {}

        self._reader   = _hotshot.logreader( logfn )
        self._nextitem = self._reader.next
        self._info     = self._reader.info
        if self._info.has_key( 'current-directory' ):
           self.cwd = self._info[ 'current-directory' ]
        else:
           self.cwd = None
        self.root        = FunctionNode( self )
        self._stack      = [ self.root ]
        self._append     = self._stack.append
        self._pop        = self._stack.pop
        self._file_cache = {}
        self._classmap   = {}
        self.process()

    def addinfo ( self, key, value ):
        """This method is called for each additional ADD_INFO record.

        This can be overridden by applications that want to receive
        these events.  The default implementation does not need to be
        called by alternate implementations.

        The initial set of ADD_INFO records do not pass through this
        mechanism; this is only needed to receive notification when
        new values are added.  Subclasses can inspect self._info after
        calling LogReader.__init__().
        """
        pass

    def get_filename ( self, fileno ):
        try:
           return self._filemap[ fileno ]
        except KeyError:
           raise ValueError, "Unknown fileno"

    def get_filenames ( self ):
        return self._filemap.values()

    def get_fileno ( self, filename ):
        filename = os.path.normcase( os.path.normpath( filename ) )
        for fileno, name in self._filemap.items():
            if name == filename:
               return fileno
        raise ValueError, "Unknown filename"

    def get_funcname ( self, fileno, lineno ):
        try:
           return self._funcmap[ ( fileno, lineno ) ]
        except KeyError:
           raise ValueError, "unknown function location"

    #----------------------------------------------------------------------------
    #  Process the contents of the profile data file:
    #----------------------------------------------------------------------------

    def process ( self ):
        while 1:
           try:
              what, tdelta, fileno, lineno = self._nextitem()
           except StopIteration:
              # logreader().next() returns None at the end
              self._reader.close()
              return

            # Handle the most common cases first:

           if what == WHAT_ENTER:
              id  = ( fileno, lineno )
              tos = self._stack[-1]
              tos.in_func += tdelta
              if not hasattr( tos, '_callees' ):
                 tos._callees = {}
              if tos._callees.has_key( id ):
                 fnode = tos._callees[ id ]
              else:
                 tos._callees[ id ] = fnode = FunctionNode( self, id )
              fnode.calls += 1
              self._append( fnode )
              continue

           if what == WHAT_EXIT:
              self._pop().in_func += tdelta
              continue

           if what == WHAT_LINENO:
              continue

           if what == WHAT_DEFINE_FILE:
              filename = os.path.normcase( os.path.normpath( tdelta ) )
              self._filemap[ fileno ] = filename
              continue
               
           if what == WHAT_DEFINE_FUNC:
              filename = self._filemap[ fileno ]
              self._funcmap[ ( fileno, lineno ) ] = ( filename, tdelta )
              continue
               
           if what == WHAT_ADD_INFO:
              # value already loaded into self.info; call the
              # overridable addinfo() handler so higher-level code
              # can pick up the new value
              if tdelta == 'current-directory':
                 self.cwd = lineno
              self.addinfo( tdelta, lineno )
              continue
               
           raise ValueError, 'Unknown event type'

    #----------------------------------------------------------------------------
    #  Helper methods:
    #----------------------------------------------------------------------------

    def source_for ( self, filename ):
        lines = self._file_cache.get( filename, None )
        if lines is None:
           fh = None
           try:
              fh    = open( filename, 'r' )
              lines = map( lambda x: x[:-1], fh.readlines() )
           except:
              lines = []
           if fh is not None:
              fh.close()
           self._file_cache[ filename ] = lines
        return lines
          
    def classname_for ( self, id ):
        classname = self._classmap.get( id, None )
        if classname is not None:
           return classname
        self._classmap[ id ] = ''
        try:
           lines = self.source_for( self.get_filename( id[0] ) )
        except:
           return ''
        lineno = id[1] - 1
        if (lineno < 0) or (lineno >= len( lines )):
           return ''
        line = lines[ lineno ]
        if line.strip()[0:4] == 'def ':
           col = line.find( 'def ' )
           for i in range( lineno - 1, -1, -1 ):
               line = lines[i]
               if ((line.strip()[0:6] == 'class ') and
                   (line.find( 'class ' ) < col)):
                  classname = line.strip()[6:].strip()
                  for c in '(:#':
                      col = classname.find( c )
                      if col >= 0:
                         break
                  else:
                      col = len( classname )
                  self._classmap[ id ] = classname[:col].strip() + '.'
                  break
        return self._classmap[ id ]
    
    def _decode_location ( self, fileno, lineno ):
        try:
            return self._funcmap[(fileno, lineno)]
        except KeyError:
            #
            # This should only be needed when the log file does not
            # contain all the DEFINE_FUNC records needed to allow the
            # function name to be retrieved from the log file.
            #
            if self._loadfile(fileno):
                filename = funcname = None
            try:
                filename, funcname = self._funcmap[(fileno, lineno)]
            except KeyError:
                filename = self._filemap.get(fileno)
                funcname = None
                self._funcmap[(fileno, lineno)] = (filename, funcname)
        return filename, funcname

    def _loadfile ( self, fileno ):
        try:
            filename = self._filemap[fileno]
        except KeyError:
            print "Could not identify fileId", fileno
            return 1
        if filename is None:
            return 1
        absname = os.path.normcase(os.path.join(self.cwd, filename))

        try:
            fp = open(absname)
        except IOError:
            return
        st = parser.suite(fp.read())
        fp.close()

        # Scan the tree looking for def and lambda nodes, filling in
        # self._funcmap with all the available information.
        funcdef = symbol.funcdef
        lambdef = symbol.lambdef

        stack = [st.totuple(1)]

        while stack:
            tree = stack.pop()
            try:
                sym = tree[0]
            except (IndexError, TypeError):
                continue
            if sym == funcdef:
                self._funcmap[(fileno, tree[2][2])] = filename, tree[2][1]
            elif sym == lambdef:
                self._funcmap[(fileno, tree[1][2])] = filename, "<lambda>"
            stack.extend(list(tree[1:]))
     
#-------------------------------------------------------------------------------
#  'FunctionNode' class:
#-------------------------------------------------------------------------------
       
class FunctionNode:
    
   def __init__ ( self, info, id = None ):
       self._info   = info
       self.id      = id or ( 0, 0 )
       self.calls   = 0
       self.in_func = 0  

   def total_time ( self ):
       if not hasattr( self, '_total_time' ):
          tt = self.in_func
          if hasattr( self, '_callees' ):
             for callee in self._callees.values():
                 tt += callee.total_time()
          self._total_time = tt
       return self._total_time
       
   def callees ( self ):
       if hasattr( self, '_callees' ):
          return self._callees
       return {}
       
   def all ( self ):
       if not hasattr( self, '_all' ):
          if not hasattr( self, '_callees' ):
             return {}
          all     = {}
          callees = self._callees.values()
          for callee in callees:
              all[ callee.id ] = [ callee.id, callee.calls, callee.in_func ]
          for callee in callees:
              for id, calls, in_func in callee.all().values():
                  if not all.has_key( id ):
                     all[ id ] = entry = [ id, 0, 0 ]
                  else:
                     entry = all[ id ]
                  entry[1] += calls
                  entry[2] += in_func
          self._all = all
       return self._all
       
   def info ( self, id ):
       try:
          filename, funcname = self._info._funcmap[ id ]
          return ( filename, funcname, id[1] )
       except:
          return ( 'Unknown', 'Unknown', id[1] )
       
   def filename ( self ):
       return self.info( self.id )[0]
       
   def funcname ( self ):
       return self.info( self.id )[1]
   
   def lineno ( self ):
       return self.info( self.id )[2]
          
   def label ( self, id = None, include_filename = 0 ):
       id = id or self.id
       if id is None:
          return '<root>'
       filename, funcname, lineno = self.info( id )
       if include_filename:
          return '%s%s [%s:%d]' % ( self._info.classname_for( id ), funcname, 
                                    os.path.basename( filename ), lineno )
       return '%s%s' % ( self._info.classname_for( id ), funcname )
          
   def __repr__ ( self ):
       filename, funcname, lineno = self.info( self.id )
       basename = os.path.basename( filename )
       return '%s [%s:%d] called %s, total time: %d' % ( 
              funcname, basename, lineno, plural_of( self.calls, 'time' ), 
              self.total_time() ) 

#-------------------------------------------------------------------------------
#  Return the correct plural form of a number:
#-------------------------------------------------------------------------------
              
def plural_of ( n, suffix ):
    if n == 1:
       return '%d %s' % ( n, suffix )
    return '%d %ss' % ( n, suffix ) 
