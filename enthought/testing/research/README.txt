Not much here yet... 

Most of the heavy lifting happens in harvest_suite.py.  Check its doc-strings
out for more info.

Usage
-----
    C:\wrk\eric\tests>python
    Enthought Edition build 1057
    Python 2.3.3 (#51, Feb 16 2004, 04:07:52) [MSC v.1200 32 bit (Intel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from enthought.testing import harvest_suite
    >>> from enthought.testing import run_tests
    >>> run_tests(harvest_suite)
    ...................
    ----------------------------------------------------------------------
    Ran 19 tests in 0.172s
    
Tasks
-----

*. Add a reporter that will report on the failed_modules and omitted_classes
   information in our TestSuite.
*. Better docs.
*. Integrate into build/tests process.  
*. Integrate code coverage information?
*. Convert all enthought modules to use the required testing format.
*.     


