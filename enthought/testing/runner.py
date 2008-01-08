# best if run with output redirected
# python run.py > out 2>&1


import datetime
import getopt
import os
import re
import string
import sys
import time
import unittest

from simple_harvester import SimpleHarvester
from test_case_harvester import TestCaseHarvester
from coverage import the_coverage as coverage

from utils import setVerboseLevel, getVerboseLevel, \
                printTraceMessage, getExceptionFromStack

class FailedModuleTestSuite(unittest.TestSuite):
    """ This class is only to be used to represent a failed module
        which didn't get setup as a testsuite
    """
    def __init__(self, tests=(), name="unknown"):
        """ This method takes an additional argument from the parent class's 
            init method, which is used for providing a name.
        """
        self.name = name
        self._tests = []
        self.addTests(tests)
                
    def id(self):
        return self.name
        
    def shortDescription(self):
        return "module failed to load"

class XmlTestResult(unittest._TextTestResult):
    """ This class is used to represent unit test results in
        a hierarchical xml file that mirrors the directory
        structure
    """
    def __init__(self, stream, descriptions, verbosity):
        unittest.TestResult.__init__(self)
        self.stream = stream
        self.showAll = False
        self.dots = False
        self.successes = []
        self.descriptions = descriptions
        
    def addSuccess(self, test):
        self.successes.append(test)
        
    def addFailuredModule(self, module, stack):
        #we would add an error for this, but the addError
        # emthod reauires a traceback object & all we have
        # is the string representation
        try:
            self.failures.append((FailedModuleTestSuite((),module), stack))
        except Exception, ex:
            print ex
                    
    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printTestList('error', self.errors)
        self.printTestList('failure', self.failures)
                
    def printSuccesses(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        for test in self.successes:
            try:
                id = test.id()
                classname = id[:id.rfind(".")]
                id = id[id.rfind(".") + 1:]
                self.stream.writeln('    <testcase classname="%s" name="%s">' % 
                                    (classname, id))
                self.stream.writeln('      <success/>')
                self.stream.writeln('    </testcase>')
            except Exception, ex:
                print ex

    def printTestList(self, flavour, errors):
        if (len(errors) > 0):
            pattern = re.compile('(.*)\"(.*)\",(.*)')
            for test, stack in errors:
                #parse the stack just a little bit to get the filename
                filename = re.match(pattern, stack.splitlines()[1]).group(2)
                
                id = test.id()
                desc = self.getDescription(test)
                exc_type = getExceptionFromStack(stack)
                
                stack = stack.replace("<", "&lt;")
                stack = stack.replace(">", "&gt;")
                
                self.stream.writeln('    <testcase classname="%s" name="%s">' % 
                                    (filename, id))
                self.stream.writeln('      <%s type="%s">%s</%s>' %
                                    (flavour, exc_type, stack, flavour))
                self.stream.writeln('    </testcase>')
                                    
                                    
class XmlTestRunner(unittest.TextTestRunner):
    """A test runner class that displays results in xml.
    """
    def __init__(self, stream=sys.stderr, descriptions=1, verbosity=1):
        self.stream = unittest._WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.name = "";

    def run(self, testcase):
        result = XmlTestResult(self.stream, self.descriptions, self.verbosity)
        startTime = time.time()
        testcase(result)
        stopTime = time.time()
        self.timeTaken = float(stopTime - startTime)
                
        self.name = testcase.id()
        
        return result

    def mergeResults(self, results, failed_modules):
        for module, stack in failed_modules:
            results.addFailuredModule(module, stack)

    def writeResults(self, results):
        try:
            testCount = results.testsRun
            failCount = len(results.failures)
            errorCount = len(results.errors)
            passCount = testCount - failCount - errorCount
    
            self.stream.writeln('<testsuite name="%s" time="%.3fs" tests="%d" failures="%d" errors="%d" >' % 
                (self.name, self.timeTaken, testCount, failCount, errorCount) )
    
            results.printErrors()
            results.printSuccesses()
            
            self.stream.writeln("</testsuite>")
        except Exception, ex:
            print ex            

class TestInfo :
    def __init__( self, dir, relativedir, runner, results, suite, failed_modules ) :
        self.dir = dir
        self.relativedir = relativedir
        self.runner = runner
        self.results = results
        self.suite = suite
        self.failed_modules = failed_modules
        
        return
    
    
class Runner:
    
    def __init__( self, subdirs=["."], verbose=10, 
            log_filename="unittest_log.txt", 
            relativedir=".", 
            dir_pattern="tests", 
            file_pattern="*_test_case.py",
            omit_dirs=['.svn', '.cvs'], 
            omit_filename='__omit__.py', 
            test_pattern="test_",
            unittest_redirect=False,
            suppress_coverage=False,
            logdir="./",
            xmlmode=False,
            *args, **kw ) :
        """ Create a test runner that will seach out and run tests in each
            of the directories of 'subdirs'.
            
            subdirs
                starting points for test search
            verbose 
                higher numbers give more detailed output, 1 gives minimal
            log_filename 
                unittest output filename. One in each subdirectory
            omit_dirs 
                omit files where the full name begins with one of
                these prefixes (e.g., [``c:\python23``]), *omit_dirs* names that begin
                with ``.`` are treated as basename patterns (e.g., ``.svn``).
            relativedir 
                report results relative to dir
            xmlmode
                formats reports in xml
        """
        self.subdirs = [ os.path.normcase( os.path.abspath( dir )) 
                        for dir in subdirs ]
        self.unittest_redirect = unittest_redirect
        self.verbose = verbose
        self.log_filename = log_filename
        self.relativedir = os.path.normcase( os.path.abspath( relativedir ) )
        self.relativedir += os.path.sep
        self.suppress_coverage = suppress_coverage
        self.logdir=logdir
        self.xmlmode=xmlmode
        
        self.omit_dirs = []
        for dir in omit_dirs :
            if dir.startswith('.') :
                self.omit_dirs.append( dir )
            else :
                self.omit_dirs.append( os.path.normcase( os.path.abspath( dir ))) 
                
        self.harvester = TestCaseHarvester( 
                            dir_pattern = dir_pattern,
                            file_pattern = file_pattern,
                            omit_filename = omit_filename,
                            omit_dirs=omit_dirs,
                            test_pattern=test_pattern )

        self.startdir = os.getcwd()
        return

    def run_tests( self ) :
        """ Find and run tests returning a list of TestInfo,
        one for each dir in self.subdir
        """

        results = []
        if self.xmlmode:
            xmlstream = open("UnitResults.xml", "w")
            xmlstream.write("<UnitResults>\n")
        for subdir in self.subdirs :
            printTraceMessage("Run tests in curent working directory " + str(subdir))
            os.chdir(subdir)
            try :
                if self.unittest_redirect :
                    results_file = file(self.log_filename, 'w')
                    sys_stdout = sys.stdout
                    sys.stdout = results_file
                    sys_stderr = sys.stderr
                    sys.stderr = results_file
                
                failed_modules = []
                suite = self.harvester.suite_for_tree( subdir, failed_modules )
                
                if self.xmlmode:
                    runner = XmlTestRunner( stream=xmlstream, verbosity=self.verbose)
                else:
                    runner = unittest.TextTestRunner( stream=sys.stdout, verbosity=self.verbose)
                    
                test_results = runner.run( suite )		

                sys.stdout.flush()
                sys.stderr.flush()
                
                if self.unittest_redirect :
                    sys.stdout = sys_stdout
                    sys.stderr = sys_stderr
                    results_file.close()
                
                relativename = os.path.normcase(os.getcwd())
                relativename = relativename.replace( self.relativedir, "")
                
                results.append( TestInfo( os.getcwd(),
                                    relativename,
                                    runner, test_results, suite,
                                    failed_modules ) )
                                    
                if self.xmlmode:
                    runner.mergeResults( test_results, failed_modules)
                    runner.writeResults( test_results )
                                    
            finally :
               os.chdir( self.startdir )
        
        if self.xmlmode:
            xmlstream.write("</UnitResults>\n")
            xmlstream.close()
            
        return results

    def include_unused_modules( self ) :
        """ find all .py files in the visited directories and 
        include all unloaded modules in the coverage results 
        """
        
        printTraceMessage("Looking for unused modules")
        save_dir_pattern = self.harvester.dir_pattern
        self.harvester.dir_pattern = "*"
        save_file_pattern = self.harvester.file_pattern
        self.harvester.file_pattern = "*.py"

        for dir in self.subdirs:
            files = self.harvester.files( dir )
            for file in files :
                if not coverage.cexecuted.has_key(file) :
                    printTraceMessage("unused module added: " + str(file))
                    coverage.cexecuted[file] = {}

        self.harvester.file_pattern = save_file_pattern
        self.harvester.dir_pattern = save_dir_pattern
        return

    def report_subdirectory_subtotals( self, results ) :
        printTraceMessage("Report subtotals")
        ### Get coverage sub totals
        sub_totals = coverage.get_subtotals( 
            self.subdirs, 
            coverage.cexecuted.keys(),
            ignore_errors=1,
            omit_prefixes=self.omit_dirs )
        
        ### report results
        total_tests = 0
        total_pass = 0
        total_errors = 0
        total_failures = 0
        total_failed_modules = 0
        total_statements = 0 
        total_executed = 0

        # what's the longest name?
        max_name = max([20,] \
            + map(len,  map( lambda(result): result.relativedir, results)))
        
        unittest_format = "%%-%ds %%4d Tests run, %%4d Errors, %%4d Failures, %%4d Failed Modules" \
             % max_name
        coverage_format = "%7s Statements, %7d Executed, %5d%% Coverage"
        pass_format = "* %%-%ds %%4d out of %%d Tests ran successfully.\n" % max_name
        fail_format = "* %%-%ds %%4d out of %%d Tests failed.\n" % max_name
        error_format = "* %%-%ds %%4d out of %%d Tests got an error.\n" % max_name

        # create the files we need for reporting
        fname = self.log_filename.split(".")
        pass_file = file(self.logdir + fname[0] + '_pass.' + fname[1], 'w')
        error_file = file(self.logdir + fname[0] + '_error.' + fname[1], 'w')
        fail_file = file(self.logdir + fname[0] + '_fail.' + fname[1], 'w')

        # output subtotals joining test results with coverage stats
        for testinfo in results :
            failed_modules = testinfo.failed_modules
            unittest_results = unittest_format % (
                testinfo.relativedir, testinfo.results.testsRun, 
                len(testinfo.results.errors), len(testinfo.results.failures),
                len(failed_modules) )
            total_tests += testinfo.results.testsRun
            total_errors += len(testinfo.results.errors)
            total_failures += len(testinfo.results.failures)
            total_failed_modules += len(failed_modules)

            if testinfo.results.wasSuccessful():
                total_pass += testinfo.results.testsRun
                pass_file.write(pass_format % (testinfo.relativedir,
                                               testinfo.results.testsRun,
                                               testinfo.results.testsRun))
                pass_file.flush()
            else:
                # set the total pass first
                temp_pass = testinfo.results.testsRun - \
                            len(testinfo.results.errors) - \
                            len(testinfo.results.failures)
                if temp_pass > 0:
                    total_pass += temp_pass
                    pass_file.write(pass_format % (testinfo.relativedir, 
                                                   temp_pass,
                                                   testinfo.results.testsRun))
                    pass_file.flush()
                
                #now deal with the error case
                if len(testinfo.results.errors) > 0:
                    error_file.write(error_format % (testinfo.relativedir, 
                                                     len(testinfo.results.errors),
                                                     testinfo.results.testsRun))
                    for error in testinfo.results.errors:
                        error_file.write("->In %s\n" % error[0].id())
                        error_file.write(error[1])
                    error_file.flush()

                #now deal with the failure case
                if len(testinfo.results.failures) > 0:
                    fail_file.write(fail_format % (testinfo.relativedir, 
                                                   len(testinfo.results.failures),
                                                   testinfo.results.testsRun))
                    for failure in testinfo.results.failures:
                        fail_file.write("->In %s\n" % failure[0].id())
                        fail_file.write(failure[1])
                    fail_file.flush()

            try :
                statements, executed, missing = sub_totals[ testinfo.dir ]
                if statements > 0 :
                    pc = 100.0 * executed / statements
                else:
                    pc = 100.0
                total_statements += statements
                total_executed += executed
            except:
                statements = 'unknown'
                executed = 0
                missing = 0
                pc = 0
                
            if not self.suppress_coverage:
                coverage_results = coverage_format % ( statements, executed, pc )
                print unittest_results, coverage_results
            else:
                print unittest_results        
    
        # output totals
        unittest_results = unittest_format % (
                "Total", total_tests, total_errors, total_failures, 
                total_failed_modules )
        
        if total_statements > 0 :
            pc = (100.0 * total_executed / total_statements )
        else :
            pc = 0.0
            
        if not self.suppress_coverage:
            coverage_results = coverage_format % (
                total_statements, total_executed, pc )
            print unittest_results, coverage_results
        else:
            print unittest_results        
        
        # update totals in reporting files
        pass_file.write("\nTotal=%d" % total_pass)
        pass_file.close()
        error_file.write("\nTotal=%d" % total_errors)
        error_file.close()
        fail_file.write("\nTotal=%d" % total_failures)
        fail_file.close()
                
        return
        
    def report_full_coverage( self, xmlmode, show_missing=0 ) :
        """ print standard coverage report for all .py files """
        printTraceMessage("Report full coverage")

        if not xmlmode:
            print "Coverage details"
            
        coverage.report(coverage.cexecuted.keys(),
                        ignore_errors=1,
                        show_missing=show_missing,
                        omit_prefixes=self.omit_dirs,
                        include_prefixes=self.subdirs,
                        relativedir=self.relativedir,
                        textmode=(not xmlmode), 
                        xmlmode=xmlmode)
        
        # add the coverage to a specific file for reporting
        fname = self.log_filename.split(".")
        coverage_file = file(self.logdir + fname[0] + '_coverage.' + fname[1], 'w')

        # replace stdout with our file
        sys_stdout = sys.stdout
        sys.stdout = coverage_file

        coverage.report(coverage.cexecuted.keys(),
                        ignore_errors=1,
                        show_missing=show_missing,
                        omit_prefixes=self.omit_dirs,
                        include_prefixes=self.subdirs,
                        relativedir=self.relativedir,
                        textmode=(not xmlmode), 
                        xmlmode=xmlmode)
                        
        # restore stdout
        sys.stdout = sys_stdout
        coverage_file.close()

        return
        
    def run( self ) :
        """ Run tests with coverage and print report """

        printTraceMessage("Runner.run start coverage")
        
        ### Turn on coverage
        if not self.suppress_coverage:
            coverage.erase()
            coverage.start()
            printTraceMessage("Runner.run run tests")
        

        ### Run unittests
        results = self.run_tests()

        ### Turn off coverage
        if not self.suppress_coverage:
            printTraceMessage("Runner.run stop coverage")
            coverage.stop()
            coverage.save()
        
        self.include_unused_modules()
        
        if not self.xmlmode:
            self.report_subdirectory_subtotals( results )
        
        if not self.suppress_coverage:
            self.report_full_coverage(self.xmlmode)
            
        return

def usage() :
    print """
usage: run [-b file] [-d dir] [-f suffix] [-h] [-o dir]* [-r dir] [-s dir]* [-t prefix] [dir]*

[-b blocking_file ] : exclude directories with this file (default '__omit__.py')
[-d dir_pattern ] : test directory must match this pattern (defalut 'tests')
[-f file_pattern ] : test file must match this pattern (defalut '*_test_case.py')
[-h] : print this help
[-c] : suppress coverage display (bad pneumonic, but the other letters were taken)
[-o dir]* : don't run tests or include results for the directory dir
[-r dir]  : report results relative to dir or /, 
            ie. eliminate dir as a prefix on reported files
[-s dir]* : run tests in or below subdirectores of the directory dir
[-t test_pattern ] : TestCase subclass method prefix (default 'test_')
[-u] : redirect unittest output to unittest_log.txt
[-v verbositylevel]
[dir]*    : run tests found in or below directory dir
    
Unit tests are run and coverage numbers accumulated.
The coverage statistics are stored in the file ./.coverage.
For each directory specified, or subdirectory of directories specified
following the -s option, unit tests will be located and run. Output
from the unit tests is directed to the file unittest_log.txt in the
specified directories or subdirectories.
    """

def run(subdirs=[], relativedir=".", dir_pattern="tests", logdir="./",
        file_pattern="*_test_case.py", omit_dirs=['c:\python23','.svn','.cvs'],
        omit_filename='__omit__.py', test_pattern="test_", verbose=10,
        unittest_redirect=False, suppress_coverage=False, unexpanded_subdirs=[],
        xmlmode=False) :

    # expand the specified subdirs one level
    printTraceMessage("Create harvester with omit_dirs: " \
        + str(omit_dirs) + " and omit_filename: " + str(omit_filename))
        
    harvester = SimpleHarvester( 
        dir_pattern="*",
        omit_dirs=omit_dirs, 
        omit_filename=omit_filename)
    
    for dir in unexpanded_subdirs :
        printTraceMessage("Harvesting directory " + str(dir))
        dirs = harvester.subdirs( dir )
        subdirs.extend( dirs )

    printTraceMessage("Create Runner")
    
    # run the tests
    runner = Runner( subdirs,
        dir_pattern=dir_pattern,
        file_pattern=file_pattern,
        omit_dirs=omit_dirs, 
        omit_filename=omit_filename,
        relativedir=relativedir,
        test_pattern=test_pattern,
        verbose=verbose,
        unittest_redirect = unittest_redirect,
        suppress_coverage = suppress_coverage,
        logdir=logdir,
        xmlmode=xmlmode
         )

    if not xmlmode:
        print "Unit Tests run at", datetime.datetime.now()
        
    printTraceMessage("Create run")
        
    rc = True
    try:
        runner.run()	 
    except:
        rc = False

    return rc
    
def main() :
    sys.path.insert(0, '.')
    
    subdirs = []
    relativedir = "."

    dir_pattern="tests"
    file_pattern="*_test_case.py"
    omit_dirs=['c:\python23','.svn', '.cvs']
    omit_filename='__omit__.py'
    test_pattern="test_"
    verbose = 10
    unittest_redirect=False
    suppress_coverage=False
    xmlmode=False
    
    try :
        opts, subdirs = getopt.getopt( sys.argv[1:], "b:d:f:ho:r:s:t:uv:cx", 
            ["blocking_file", "dir_pattern", "file_pattern", "help",
             "omit_dirs", "relativedir", "subdirs", "test_pattern", 
             "unittestredirect", "verbose", "suppress_coverage", 'xml'])
            
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    unexpanded_subdirs = []
    for o, a in opts :
        if o in ("-b", "--b", "-blocking_file", "--blocking_file") :
            omit_filename = a

        if o in ("-d", "--d", "-dir_pattern", "--dir_pattern") :
            dir_pattern = a

        if o in ("-f", "--f", "-file_pattern", "--file_pattern") :
            file_pattern = a

        if o in ("-h", "--h", "-help", "--help") :
            usage()
            sys.exit()
        
        if o in ("-o", "--o", "-omit_dirs", "--omit_dirs") :
            path = os.path.normcase( a )
            omit_dirs.append( path )

        if o in ("-r", "--r", "-relativedir", "--relativedir") :
            relativedir = a

        if o in ("-s", "--s", "-subdirs", "--subdirs") :
            unexpanded_subdirs.append( a )

        if o in ("-t", "--t", "-test_pattern", "--test_pattern") :
            test_pattern = a

        if o in ("-u", "--u", "-unittestredirect", "--unittestredirect") :
            unittest_redirect = True

        if o in ("-v", "--v", "-verbose", "--verbose") :
            setVerboseLevel(int(a))
            
        if o in ("-c", "--c", "-suppress_coverage", "--suppress_coverage"):
            suppress_coverage = True
            
        if o in ("-x", "-xml", "--xml"):
            xmlmode = True

    if len(unexpanded_subdirs) == 0 and len(subdirs) == 0:
        subdirs=['.']
        
    printTraceMessage("-blocking_file " + str(omit_filename))
    printTraceMessage("-dir_pattern " + str(dir_pattern))
    printTraceMessage("-file_pattern " + str(file_pattern))
    printTraceMessage("-relativedir " + str(relativedir))
    printTraceMessage("-subdirs " + str(subdirs))
    printTraceMessage("-test_pattern " + str(test_pattern))
    printTraceMessage("-unittestredirect " + str(unittest_redirect))
    printTraceMessage("-verbose " + str(getVerboseLevel()))

    
    return run(subdirs=subdirs, 
               relativedir=relativedir, 
               dir_pattern=dir_pattern,
               file_pattern=file_pattern,
               omit_dirs=omit_dirs,
               omit_filename=omit_filename, 
               test_pattern=test_pattern,
               verbose=verbose,
               unittest_redirect=unittest_redirect,
               suppress_coverage=suppress_coverage,
               unexpanded_subdirs=unexpanded_subdirs,
               xmlmode=xmlmode)        


if __name__ == '__main__':
    print "**********************************"
    print " deprecated, please use marathon"
    print "**********************************"

    rc = main()
    if rc == False:
        sys.exit(1)
    sys.exit(0)
       
        

    
#### EOF ######################################################################        
