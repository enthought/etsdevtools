import glob, os
import unittest
import sys
import traceback
import copy

from utils import printTraceMessage

from simple_harvester import SimpleHarvester

class EnthoughtTestSuite(unittest.TestSuite):
    def __init__(self, tests=(), name="unknown"):
        """ This method takes an additional argument from the parent class's 
            init method, which is used for providing a name.
        """
        self.name = name
        self._tests = []
        self.addTests(tests)
                
    def id(self):
        return self.name

class TestCaseHarvester( SimpleHarvester) :

    def __init__( self, dir_pattern="tests", file_pattern="*test_case.py",
            omit_dirs=['.svn', '.cvs'], omit_filename='__omit__.py', 
            test_pattern="test_" ) :
        """ Create a Harvester of unittest TestSuites.
        
        test_pattern : test case methods must be named with this prefix
        """
        SimpleHarvester.__init__(self, dir_pattern=dir_pattern, 
            file_pattern=file_pattern, omit_dirs=omit_dirs, 
            omit_filename=omit_filename)
            
        self.test_pattern = test_pattern
        self.test_loader = unittest.defaultTestLoader
        self.test_loader.suiteClass = EnthoughtTestSuite

        # there is a design flaw in pyunit: if 2 modules have the same name,
        # then the first module will be run twice. To work around this flaw
        # we keep a list of all modules, then raise an exception when the second
        # module of the same name is found. This applies only to unit test modules
        self.all_modules = []

        
        return


    def suite_for_dir( self, topdir, dir, failed_modules=[] ) :
        """ Builds the test suite.
        Adds to failed_modules any module that won't load.
        """

        try :
            # Required by finally.
            dir_init_name_created = False

            save_default_prefix = self.test_loader.testMethodPrefix
            self.test_loader.testMethodPrefix = self.test_pattern
    
            # The uber-suite!
            suite = EnthoughtTestSuite((), "uber")
            files = glob.glob(dir + os.path.sep + self.file_pattern)
            
            dir_init_name = dir + os.path.sep + '__init__.py'

            if not os.path.exists(dir_init_name):
                dir_init = file(dir_init_name, "w")    
                dir_init.close()
                dir_init_name_created = True
            
            printTraceMessage('suite_for_dir topdir %s dir %s files: %s' % (topdir, dir, files))
            for filename in files:
                # Import the test case module.
                file_name, ext = os.path.splitext(filename)
                module_name = file_name[ len(topdir + os.path.sep):]
                module_name = module_name.replace(os.path.sep, '.')
                try :
                    if (module_name in self.all_modules):
                        raise "Two modules have the name '%s'. This causes a design flaw in pyunit" % module_name
                    printTraceMessage('              import module %s' % module_name)
                    __import__(module_name, globals(), locals())
                    suite.addTest(self.test_loader.loadTestsFromModule( sys.modules[module_name]))
                    self.all_modules.append(module_name)

                except:
                    res = (os.path.abspath(filename), self.exc_info_as_string())
                    failed_modules.append(res)
                    print "Failed to load module: ", filename
                    print res[1]
    
        
        finally :
            self.test_loader.testMethodPrefix = save_default_prefix
            
            if dir_init_name_created:
                # Remove the generated __init__.py and pyc
                os.unlink(dir_init_name)
                if os.path.isfile(dir_init_name+'c'):
                    os.unlink(dir_init_name+'c')

        return suite

    def suite_for_tree( self, dir, failed_modules=[] ) :
        """ Build test suite for all test directories under dir """
        suite = EnthoughtTestSuite((), dir)
        testdirs = self.dirs( dir )
        printTraceMessage('suite_for_tree dir %s testdirs %s' % (dir, testdirs))
        for testdir in testdirs :
            child_suites = self.suite_for_dir( dir, testdir, 
                                            failed_modules=failed_modules )
            suite.addTest( child_suites )

        return suite

    def suites( self, dirs, failed_modules=[] ) :
        """ Return list of suites; one for each dir in dirs
        and append to failed_modules a correpsonding list of modules
        that failed to load creating a list of lists of failed modules.
        """
        printTraceMessage('suites dirs %s' % dirs)

        failed_modules = []
        suites = []
        for dir in dirs :
            dir_failed_modules = []
            suites.append( self.suite_for_tree( dir, dir_failed_modules ) )
            failed_modules.append( dir_failed_modules )
        
        return suites
            
        
    
    def _exc_info( self ):
        """ Return a version of sys.exc_info() with the traceback frame
            minimised; usually the top level of the traceback frame is not
            needed.
            
            borrowed from the standard unittest library.
        """
        exctype, excvalue, tb = sys.exc_info()
        if sys.platform[:4] == 'java': ## tracebacks look different in Jython
            return (exctype, excvalue, tb)
        newtb = tb.tb_next
        if newtb is None:
            return (exctype, excvalue, tb)
        return (exctype, excvalue, newtb)
    
    def exc_info_as_string( self ):
        err = self._exc_info()
        return ''.join(traceback.format_exception(*err))


#### EOF ######################################################################        
