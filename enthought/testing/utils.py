import testoob.testing

_verboseLevel = 10

def setVerboseLevel( level ):
    global _verboseLevel
    _verboseLevel = level
    return

def getVerboseLevel():
    return _verboseLevel

def printTraceMessage(msg, level=11):
    if (level < _verboseLevel):
        print "[TRACE] " + str(msg)

def getExceptionFromStack(stack):
    lines = stack.splitlines()
    line = 1
    while line <= len(lines):
        if (lines[line][0:6] == "  File"):
            line = line + 2
        else:
            return lines[line].split(':')[0]
        
def assert_equals_or_skip(expected, value, msg=None):
    try:
        testoob.testing.assert_equals(expected, value, msg)
    except AssertionError:
        testoob.testing.skip(msg)

def marathon_arg_parser(usage):
    try:
        import optparse
    except ImportError:
        from compatibility import optparse

    try:
        import commandline
        p = commandline.parsing.parser
        using_deprecated_testoob = False
    except Exception, ex:
        # falling back to using the one from svn
        formatter=optparse.TitledHelpFormatter(max_help_position=30)
        p = optparse.OptionParser(usage=usage, formatter=formatter)
        using_deprecated_testoob = True
        
    p.add_option("--version", action="store_true", help="Print the version of testoob")
    p.add_option("-q", "--quiet",   action="store_true", help="Minimal output")
    p.add_option("-v", "--verbose", action="store_true", help="Verbose output")
    p.add_option("-i", "--immediate", action="store_true", help="Immediate feedback about exceptions")
    p.add_option("--vassert", action="store_true", help="Make asserts verbose")
    p.add_option("--glob", metavar="PATTERN", help="Filtering glob pattern")
    p.add_option("-s", "--silent", action="store_true", help="no output to terminal")
    color_choices = ["never", "always", "auto"]
    p.add_option("--color-mode", metavar="WHEN", type="choice", choices=color_choices, default="auto", help="When should output be in color? Choices are " + str(color_choices) + ", default is '%default'")
    p.add_option("--interval", metavar="SECONDS", type="float", default=0, help="Add interval between tests")
    p.add_option("--timeout", metavar="SECONDS", type="int", help="Fail test if passes timeout")
    p.add_option("--stop-on-fail", action="store_true", help="Stop tests on first failure")
    p.add_option("--debug", action="store_true", help="Run pdb on tests that fail")
    p.add_option("--threads", metavar="NUM_THREADS", type="int", help="Run in a threadpool")
    p.add_option("--repeat", metavar="NUM_TIMES", type="int", help="Repeat each test")
    p.add_option("--timed-repeat", metavar="SECONDS", type="float", help="Repeat each test, for a limited time")
    p.add_option("--capture", action="store_true", help="Capture the output of the test, and show it only if test fails")
    coverage_choices = ["silent", "slim", "normal", "massive", "xml"]
    p.add_option("--coverage", metavar="AMOUNT", type="choice", choices=coverage_choices, help="Test the coverage of the tested code, choices are: %s" % coverage_choices)
    p.add_option("--test-method-glob", metavar="PATTERN", help="Collect test methods based on a glob pattern")
    p.add_option("--test-method-regex", metavar="REGEX", help="Collect test methods based on a regular expression")
    profiler_choices = ["hotshot", "profile"]
    p.add_option("--profiler", type="choice", choices=profiler_choices, help="Profile the tests with a profiler, choices are: %s" % profiler_choices)
    p.add_option("--profdata", metavar="FILE", default="testoob.stats", help="Target file for profiling information, default is '%default'")

    #add our custom args
    p.add_option("-d", "--directory",   action="store_true", help="The filename argument is a directory from which this process will spawn new processes for each test file found")

    if (using_deprecated_testoob):
        p.add_option("-l", "--list", action="store_true", help="List the test classes and methods found")
        p.add_option("--list-formatted", metavar="FORMATTER", help="Like option '-l', just formatted (e.g. csv).")
        p.add_option("--regex", help="Filtering regular expression")
        p.add_option("--xml", metavar="FILE", help="output results in XML")
        p.add_option("--html", metavar="FILE", help="output results in HTML")
        p.add_option("--pdf", metavar="FILE", help="output results in PDF (requires ReportLab)")    
        p.add_option("--processes", metavar="NUM_PROCESSES", type="int", help="Run in multiple processes, use Pyro if available")
        p.add_option("--processes_pyro", metavar="NUM_PROCESSES", type="int", help="Run in multiple processes, requires Pyro")
        p.add_option("--processes_old", metavar="NUM_PROCESSES", type="int", help="Run in multiple processes, old implementation")
        p.add_option("--randomize-order", action="store_true", help="Randomize the test order")
        p.add_option("--randomize-seed", metavar="SEED", type="int", help="Seed for randomizing the test order, implies --randomize-order")

    options, parameters = p.parse_args()
    if options.version:
        from __init__ import __version__
        print __version__
        from sys import exit
        exit(0)
    
    return p

### EOF #######################################################################
