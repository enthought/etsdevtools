For the most recent documentation, refer to https://svn.enthought.com/enthought/wiki/UnitTesting


= Marathon =

In the enthought/testing dir you will find several scripts related to running unit tests. Currently, the preferred method of testing is to run marathon.py. The marathon.py script is a customization of [http://testoob.sf.net testoob]. Marathon offers all of the features of testoob with the addition of allowing for running test suites in separate processes and aggregating the results. To find what command line options are available, run 
{{{
python marathon.py -h
}}}

== Running a lot of tests ==
Marathon can run many test suites spread throught a file system. Marathon will recursively search from a given directory to find all the unit tests, to do so, run
{{{
python marathon.py -d <top_level_dir>
}}}

File and tests names can be specified as well in order to narrow the total tests ran. Refer to the command line help for these arguments.

== Running a test suite ==
Marathon can also be used for running single test suites, which are test cases contained in a single python file. There are two ways to do this, to run a single test suite by calling marathon from the command line, run
{{{
python marathon.py <test_file>
}}}

To run your test by running the file containing your test suite from the command line, add the following to your test file:
{{{
if __name__ == "__main__":
    from enthought.testing import marathon
    marathon.main()
}}}
Then run the file from the command line:
{{{
python <your_test_suite_file.py>
}}}

== Running a single test ==
If you're interested in only a single test, marathon can do that too. Better yet, it can run only test methods matching a criteria expressed with a glob style expression or a regular expression.

'''note:''' due to the nature of regex and glob expressions, you may need to wrap the command line argument in double quotes.

If you want to only run tests that start with "test_partial_", you could run
{{{
python marathon.py <test_file> --test-method-glob=test_partial_*
}}}
or if you want to run all tests that start with "test_" or "check_", you could run
{{{
python marathon.py <test_file> --test-method-regex=^(test_.*)|(check_.*)
}}}

== Aggregate results ==
If marathon.py is ran with the -d option, it will recursively search all subdirectories for unit tests. Simple test results will be written to the console, and detailed results will be written to !UnitResults.xml (unless the --xml flag is used to specify the filename)

== Skipping tests ==
Sometimes its useful to temporarily disable unit tests, for example during refactoring. Commenting out unit tests is bad because it doesn't provide feedback to remind you to re-enable the tests. Fortunately, testoob supports skipping of unit tests:
{{{
class ATestCase(unittest.TestCase):
    def test_foo(self):
      import testoob.testing
      testoob.testing.skip("a good reason")

      this_function_would_fail()
}}}
Of course, it may make since to embed some logic, such as wrapping your 
import if you're inthe middle of refactoring code:
{{{
class ATestCase(unittest.TestCase):
    def test_foo(self):
      try:
         import a.b.c
      except ImportError, e:
         import testoob.testing
         testoob.testing.skip("Import Error: " + str(e))
}}}
When you run the test, you should see:
{{{
S
Skipped 1 tests
 - test_foo (import error: cannot import name a.b.c)
}}}
