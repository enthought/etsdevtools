import glob, os
import unittest
import sys
import traceback
import fnmatch

class SimpleHarvester:

    def __init__( self, dir_pattern="*", file_pattern="*", omit_dirs=[], omit_filename="__omit__" ) :
        """ Create a Harvester of unittest TestSuites.
        
        dir_pattern 
            files must be located in a directory that matches
            (glob) this pattern (directory basename)
        file_pattern 
            files must match (glob) this pattern
        omit_dirs 
             don't traverse directories with these names
        omit_filename 
             don't traverse directories that have this file
        """
        self.dir_pattern = dir_pattern
        self.file_pattern = file_pattern
        self.omit_dirs = omit_dirs
        self.omit_filename = omit_filename
        
#        print "SimpleHarvester dir_pattern: ", dir_pattern, \
#            " file_pattern: ", file_pattern, \
#            " omit_dirs: ", omit_dirs, " omit_filename: ", omit_filename
        return


    def files( self, dir) :
        """ find files matching patterns starting with directory dir. """
        dir = os.path.normcase(dir)
        files = []

        os.path.walk( dir, self._file_visitor, files)

        return files
 
    def dirs( self, dir ) :
        """ find directories matching patterns starting with directory dir """
        dir = os.path.normcase(dir)
        dirs = []

        os.path.walk( dir, self._dir_visitor, dirs )
        
        return dirs

    def subdirs( self, dir ) :
        """ return list of subdirectories of dir, non-recursive.
        dir must not be blocked by omit rules.
        Subdirectories must not be blocked by omit rules to be returned.
        """
        dir = os.path.normcase(dir)
        dirs = []

        cwd = os.getcwd()
        
        try :
            os.chdir( dir )
            
            if not self._block_dir( dir ):
                files = glob.glob( self.dir_pattern )
                for file in files :
                    if os.path.isdir( file ) and not self._block_dir( file ) :
                        dirs.append( dir + os.path.sep + file )

        finally:
            os.chdir( cwd )
        
        return dirs


    def _block_dir( self, dir ) :
        """ dir absolute path or relative to the current working directory
        return 1 if dir should be blocked, 0 otherwise """
        block = 0

        basename = os.path.basename( dir )
        if os.path.isdir( dir ) :
            omit_fullname = dir + os.path.sep + self.omit_filename
            if ( dir in self.omit_dirs or basename in self.omit_dirs
                or os.path.exists(omit_fullname) ) :
                block = 1
        else :
            # block all non directories
            block = 0

        return block

    def _file_visitor(self, files, dirname, names):
        """ Visitor that finds all files in all directores named self.dir_pattern.
        Traversal down is stopped if a directory contains the omit file.
        """
        # if current dir has omit file don't go deeper
        if self.omit_filename in names :
            del names[:]

        else :
            local_files = []
            for file in names[:] :
                fullname = dirname + os.path.sep + file
                if self._block_dir( fullname ) :
                    names.remove(file)
                elif os.path.isfile( fullname ) :
                    local_files.append( fullname )
            
            dir_match = fnmatch.filter( [os.path.basename(dirname)], self.dir_pattern )
            if len(dir_match) > 0 :
                local_files = fnmatch.filter( local_files, "*" + os.path.sep + self.file_pattern )
                files += local_files
        
        return
        
    def _dir_visitor(self, dirs, dirname, names):
        """ Visitor that finds all directores named self.dir_pattern.
        Traversal down is stopped if a directory contains the omit file.
        """
        # if current dir has omit file don't go deeper
        if self.omit_filename in names :
            del names[:]

        else :
            # does current dir match?
            dir_match = fnmatch.filter( [os.path.basename(dirname)], self.dir_pattern )
            if len(dir_match) > 0 :
                dirs.append(dirname)

            for file in names[:] :
                if self._block_dir( dirname + os.path.sep + file ) :
                    names.remove(file)

        return

                  
#### EOF ###################################################################### 
