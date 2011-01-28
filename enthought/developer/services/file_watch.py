#-------------------------------------------------------------------------------
#
#  Service for watching for file changes.
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

import wx

from os.path \
    import abspath, getsize, getmtime, exists

from enthought.traits.api \
    import HasPrivateTraits, Str, Int, Long, Any, Bool, List, Callable

from threading \
    import Thread, Lock

from time \
    import sleep

#-------------------------------------------------------------------------------
#  'WatchedFile' class:
#-------------------------------------------------------------------------------

class WatchedFile ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The name of the file being watched:
    file_name = Str

    # Does the file exist?
    file_exists = Bool( False )

    # The last time the file was updated:
    mtime = Any

    # The last known size of the file:
    size = Long

    # List of callables to be notified when the file changes:
    handlers = List( Callable )

    #---------------------------------------------------------------------------
    #  Handles the 'file_name' trait being changed:
    #---------------------------------------------------------------------------

    def _file_name_changed ( self ):
        """ Handles the 'file_name' trait being changed.
        """
        self.update()

    #---------------------------------------------------------------------------
    #  Updates the current state of the file:
    #---------------------------------------------------------------------------

    def update ( self ):
        """ Updates the current state of the file.
        """
        file_name        = self.file_name
        self.file_exists = exists( file_name )
        if self.file_exists:
            try:
                self.mtime = getmtime( file_name )
                self.size  = getsize(  file_name )
            except:
                self.mtime = self.size = -1

    #---------------------------------------------------------------------------
    #  Notifies all handlers of a change to the file:
    #---------------------------------------------------------------------------

    def notify ( self ):
        """ Notifies all handlers of a change to the file.
        """
        file_name = self.file_name
        for handler in self.handlers:
            wx.CallAfter( handler, file_name )

    #---------------------------------------------------------------------------
    #  Process any file changes that may have occurred:
    #---------------------------------------------------------------------------

    def process ( self ):
        """ Process any file changes that may have occurred.
        """
        file_name   = self.file_name
        file_exists = exists( file_name )
        if not self.file_exists:
            if not file_exists:
                return
        else:
            try:
                if (file_exists and
                    (self.mtime == getmtime( file_name )) and
                    (self.size  == getsize(  file_name ))):
                    return
            except:
                return

        self.update()
        self.notify()

    #---------------------------------------------------------------------------
    #  Adds a new handler:
    #---------------------------------------------------------------------------

    def add_handler ( self, handler ):
        """ Adds a new handler.
        """
        if handler not in self.handlers:
            self.handlers.append( handler )

    #---------------------------------------------------------------------------
    #  Removes an existing handler:
    #---------------------------------------------------------------------------

    def remove_handler ( self, handler ):
        """ Removes an existing handler.
        """
        try:
            self.handlers.remove( handler )
            return (len( self.handlers ) > 0)
        except:
            return True


#-------------------------------------------------------------------------------
#  'FileWatch' class:
#-------------------------------------------------------------------------------

class FileWatch ( HasPrivateTraits ):

    #---------------------------------------------------------------------------
    #  Starts the service running:
    #---------------------------------------------------------------------------

    def start ( self ):
        """ Starts the service running.
        """
        self._running       = True
        self._watched_files = []
        self._lock          = Lock()
        self._thread        = Thread( target = self._watch )
        self._thread.setDaemon( True )
        self._thread.start()

    #---------------------------------------------------------------------------
    #  Shuts the service down:
    #---------------------------------------------------------------------------

    def close ( self ):
        """ Shuts the service down.
        """
        self._running = False
        self._thread.join()

    #---------------------------------------------------------------------------
    #  Sets up/Removes a file watch for a specified file:
    #---------------------------------------------------------------------------

    def watch ( self, handler, file_name, remove = False ):
        """ Sets up/Removes a file watch for a specified file.
        """
        if not self._running:
            self.start()

        self._lock.acquire()
        try:
            file_name = abspath( file_name )
            for wf in self._watched_files:
                if file_name == wf.file_name:
                    break
            else:
                wf = None

            if remove:
                if (wf is not None) and (not wf.remove_handler( handler )):
                    self._watched_files.remove( wf )
            else:
                if wf is None:
                    wf = WatchedFile( file_name = file_name )
                    self._watched_files.append( wf )
                wf.add_handler( handler )
        finally:
            self._lock.release()

    #---------------------------------------------------------------------------
    #  Watches a list of WatchedFile objects for changes:
    #---------------------------------------------------------------------------

    def _watch ( self ):
        """ Watches a list of WatchedFile objects for changes.
        """
        while self._running:
            try:
                self._lock.acquire()
                for wf in self._watched_files:
                    wf.process()
            finally:
                self._lock.release()

            if self._running:
                sleep( 0.5 )

#-------------------------------------------------------------------------------
#  Create export objects:
#-------------------------------------------------------------------------------

file_watch = FileWatch()

