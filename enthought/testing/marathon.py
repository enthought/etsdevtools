#!/usr/bin/env python
# This file is borrowed heavily from testoob, with the 
# addition of a directory walker/test harvester

global_dict = globals()
local_dict = locals()

import sys
import fnmatch
import os.path
import traceback

from enthought.testing.utils import getExceptionFromStack

# Note:  xml.etree was added in Python 2.5.
try:
    import xml.etree.ElementTree as ElementTree
except ImportError:
    import elementtree.ElementTree as ElementTree

def parseArgs(printUsage=False):
    usage="""%prog [options] [test_file] [test1 [test2 [...]]]

examples:
  %prog myFile.py                          - run default set of tests
  %prog myFile.py MyTestSuite              - run suite 'MyTestSuite'
  %prog myFile.py MyTestCase.testSomething - run MyTestCase.testSomething
  %prog myFile.py MyTestCase               - run all 'test*' test methods in MyTestCase"""

    if printUsage:
        sys.argv.append("-h")

    parser = testoob_main("enthought.testing.utils.marathon_arg_parser")(usage)
    options, free_args = parser.parse_args()
    
    if len(free_args) == 0:
        parseArgs(printUsage=True)
    file_name = free_args[0]
    test_names = free_args[1:]

    return options, file_name, test_names, parser

def addPythonPath(path):
    from os.path import normpath
    sys.path.insert(0, normpath(path))

def currentFile():
    try:
        return __file__
    except NameError:
        # Python 2.2 compatibility
        return sys.argv[0]

def addTestoobToPath():
    """ Testoob is in the enthought repository temporarily.
        Try to add the testoob path to the sys.path, whether its
        in the enthought repository, or elsewhere
    """
    try:
        import testoob
        sys.path += testoob.__path__
    except:
        from enthought.testing import testoob
        sys.path += testoob.__path__

def fixIncludePath():
    """ The testoob executable is often in the same directory as testoob, so
        we'll try looking back on directory level
    """
    from os.path import dirname, join
    module_path = join(dirname(currentFile()), "..")
    addPythonPath(module_path)
    
def directoryVisitor(arg_tuple, dirname, names):
    """ Omits all directories containing '__omit__.py'
        and returns all the files matching the pattern
    """
    file_list, pattern = arg_tuple
    
    if ("__omit__.py" in names):
        return
    
    for filename in fnmatch.filter(names, pattern):
        absname = os.path.join(dirname, filename)
        file_list.append(absname)
            
def findAllTestFiles(start_dir, pattern):
    """ Walks the filesystem looking for files that match a pattern
    """
    file_list = []
    os.path.walk(start_dir, directoryVisitor, (file_list, pattern))
    return file_list

def exc_info():
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

def testoob_main(attrname):
    """ Copy of testoob's testoob_main() method. This method is
        called with a package's attribute, which will be imported
        and returned. I am not really sure why testoob does this, but
        it does allow for us to override argument parsers with our own.
    """
    
    package = "testoob.main"
    module = attrname
    if attrname.find(".") >= 0:
        separator_index = module.rfind(".")
        package = attrname[:separator_index]
        module = attrname[separator_index + 1:]
    
    try:
        exec "from %(package)s import %(module)s as result" % vars()
    except ImportError:
        fixIncludePath()
        exec "from %(package)s import %(module)s as result" % vars()
        
    return result

def main():
    import os.path

    #if main() is called from another file, then that file wants
    # to be tested, so add it to the argv
    if (os.path.basename(sys.argv[0]) != "marathon.py"):
        sys.argv.append(__file__)
        
    addTestoobToPath()
    options, file_name, test_names, parser = parseArgs()
    
    if (options.directory is not None):
        file_pattern="*_test*.py"
        if (options.glob is not None):
            file_pattern = options.glob
        testfiles = findAllTestFiles(sys.argv[-1], file_pattern)
        results = []
        for testfile in testfiles:
            #strip the -d flag out of the args
            args = [sys.executable]
            for arg in sys.argv[0:-1]:
                if (arg.startswith("-") and not arg.startswith("--")):
                    if (arg == '-d'):
                        continue                 
                    arg = arg.replace('d', '')
                args.append(arg)
                
            resultfile = testfile + ".xml"
            args += ["--xml=" + resultfile, testfile]
            
            # store the results file before spawing so if the file does not
            # get created we know python crashed
            results.append(resultfile)
            
            #spawn the test in another process to keep the test environment clean
            os.spawnv(os.P_WAIT, sys.executable, args)
            
        from enthought.testing.xml_results_writer import XmlResultsWriter
        writer = XmlResultsWriter()
        writer.aggregateResults(results)
        resultfile = "UnitResults.xml"
        if (options.xml is not None):
            resultfile = options.xml
        writer.write(resultfile)
        
        #cleanup all the intermidiate xml files
        import os
        for testfile in testfiles:
            xmlfile = testfile + ".xml"
            if os.path.exists(xmlfile):
                os.unlink(xmlfile);
                
        #read the aggregate result file to print some simple stats to the console
        root = ElementTree.parse(resultfile)
        results = root.find("UnitResults")
        print ""
        print "Aggregate unit test results"
        print ""
        for suite in results.getchildren():
            print "Suite %s %4d tests ran, %4d errors, %4d failures" \
                % (suite.attrib["name"].ljust(30), int(suite.attrib["tests"]), 
                   int(suite.attrib["errors"]), int(suite.attrib["failures"]))
            for inner_suite in suite.getchildren():
                print "      %s %4d tests ran, %4d errors, %4d failures" \
                    % (inner_suite.attrib["name"].ljust(30), int(inner_suite.attrib["tests"]), 
                       int(inner_suite.attrib["errors"]), int(inner_suite.attrib["failures"]))
                
        
    
    else:
        try:
            # Add the path of the ran file to the python path, so that includes
            # from the same directory would work.
            from os.path import dirname, basename
            import os.path
            addPythonPath(dirname(file_name))
            
            # run the file given on the command line
    
            try:
                # normalize the path to strip redundencies. This is necessary
                # for converting the path to the module name
                file_name = os.path.normpath(file_name)
                
                # try to import the file to get the module in sys.modules. 
                # execfile() does not use sys.modules and some tests require 
                # it to find their data files. The relative module name is also
                # put in the sys.modules so it can be referenced
                module_name = file_name[:-3].replace(os.path.sep, ".")
                rel_module_name = module_name[module_name.rfind(".")+1:]
                try:
                    __import__(module_name)
                    sys.modules[rel_module_name] = sys.modules[module_name]
                except:
                    # we tried, if a test fails its the test writers fault
                    pass
                
                print "\n***** Running " + file_name + "*****"
    
                global_dict['__name__'] = basename(file_name).split(".")[0]
                global_dict['__file__'] = file_name
                
                execfile(file_name, global_dict, local_dict)
    
            except ImportError, e:
                if (options.xml is not None):
                    exctype, excvalue, tb = exc_info()
                    stackdump = ""
                    for line in traceback.format_exception(exctype, excvalue, tb):
                        stackdump += line
                    f = open(options.xml, "w")
                    f.write("<results><testsuites><testcase name=\"%s\" time=\"0\">" % (file_name))
                    f.write("<result>failure</result>")
                    f.write("<failure type=\"%s\">%s</failure>" % (excvalue.__class__, stackdump) )
                    f.write("</testcase></testsuites><coverage/></results>")
    
            sys.exit(not testoob_main("_main")(None, None, options, test_names, parser))
        except IOError, e:
            print e
            parseArgs(printUsage=True)

if __name__ == "__main__":
    main()
