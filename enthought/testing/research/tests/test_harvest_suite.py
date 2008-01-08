# Do we need to do something here to ensure the parent module is in the path?

import os
import shutil
from enthought.testing import harvest_suite

import unittest

# import this file so that we can get to the __file__ and find our local
# directory.
import test_harvest_suite
local_directory = os.path.dirname(test_harvest_suite.__file__)
# ensure it is an absolute path for testing equality in some tests.
local_directory = os.path.abspath(local_directory)

class TestPythonFilesForDirectory(unittest.TestCase):
    """ Note: These tests relying on the files in "tests".  If
              those files change, then the test will need updating.
    """

    def setUp(self):
        # Rename the badsyntax.py.tmp to a .py file.  This is necessary
        # because distributing this file as a .py in an egg results in warning
        # messages from setuptools during egg building and egg installation.
        test_dir = os.path.join(local_directory, 'tests')
        self._temp_file = os.path.join(test_dir, 'bad_syntax.py')
        self._orig_file = self._temp_file + '.tmp'
        shutil.move(self._orig_file, self._temp_file)

        return


    def tearDown(self):
        # Restore our .py.tmp version of the badsyntax.py file.
        shutil.move(self._temp_file, self._orig_file)

        return


    def check_directory_with_python_and_other_files(self):
        test_directory = os.path.join(local_directory,"tests")
        full_paths = harvest_suite.python_files_for_directory(test_directory)

        # ensure we only found the files we were looking for.
        file_names = [os.path.basename(path) for path in full_paths]
        for file_name in file_names:
            assert(file_name in ['test_p1.py', 'test_p2.py', 'blah_p1.py',
                                 'bad_syntax.py'])

        # ensure that they are full paths are report for the files
        dir_names = [os.path.dirname(path) for path in full_paths]
        for dir_name in dir_names:
            assert dir_name == test_directory

    def check_filter_by_prefix(self):
        test_directory = os.path.join(local_directory,"tests")
        full_paths = harvest_suite.python_files_for_directory(test_directory,
                                                         file_prefix='test_')

        # ensure we only found the files we were looking for.
        file_names = [os.path.basename(path) for path in full_paths]
        for file_name in file_names:
            assert(file_name in ['test_p1.py', 'test_p2.py'])

        # ensure that they are full paths are report for the files
        dir_names = [os.path.dirname(path) for path in full_paths]
        for dir_name in dir_names:
            assert(dir_name == test_directory)

    def check_empty_directory(self):
        test_directory = os.path.join(local_directory,"python_files_empty")
        full_paths = harvest_suite.python_files_for_directory(test_directory)

        # shouldn't have found any files there.
        assert len(full_paths) == 0, "actual: %s" % len(full_paths)

    def check_nonexistent_directory(self):
        test_directory = os.path.join(local_directory,"nonexistent")
        full_paths = harvest_suite.python_files_for_directory(test_directory)

        # shouldn't have found any files there.
        assert len(full_paths) == 0

class TestLoadModulesForFiles(unittest.TestCase):
    """ fix me: Need additional tests for handling modules with syntax errors
                that don't load.

        Note: These tests relying on the files in "tests".  If
              those files change, then the test will need updating.
    """

    def setUp(self):
        # Rename the badsyntax.py.tmp to a .py file.  This is necessary
        # because distributing this file as a .py in an egg results in warning
        # messages from setuptools during egg building and egg installation.
        test_dir = os.path.join(local_directory, 'tests')
        self._temp_file = os.path.join(test_dir, 'bad_syntax.py')
        self._orig_file = self._temp_file + '.tmp'
        shutil.move(self._orig_file, self._temp_file)

        return


    def tearDown(self):
        # Restore our .py.tmp version of the badsyntax.py file.
        shutil.move(self._temp_file, self._orig_file)

        return


    def check_python_files(self):
        test_directory = os.path.join(local_directory,"tests")
        full_paths = harvest_suite.python_files_for_directory(test_directory)

        modules, failed_modules = harvest_suite.load_modules_for_files(full_paths)

        assert len(modules) == 3

        # bad_syntax.py should be in this list
        assert len(failed_modules) == 1
        d, base = os.path.split(failed_modules[0][0])
        assert  base == 'bad_syntax.py'

    def check_empty_list(self):

        modules, failed_modules = harvest_suite.load_modules_for_files([])

        # shouldn't have found any files there.
        assert len(modules) == 0

class TestRetreiveTestClassesForModule(unittest.TestCase):

    def check_p1_with_classes(self):
        test_file = os.path.join(local_directory,"tests","test_p1.py")
        modules, failed = harvest_suite.load_modules_for_files([test_file])
        classes, omitted = harvest_suite.retreive_test_classes_for_module(
                                                              modules[0],
                                                              class_prefix='')

        assert len(classes) == 4, "actual: %s" % len(classes)
        for klass in classes:
            assert klass.__name__ in ['TestZero', 'TestOne',
                                      'TestTwo', 'NoTestThree']

class TestFilterForLevel(unittest.TestCase):

    def check_default(self):
        test_file = os.path.join(local_directory,"tests","test_p1.py")
        modules, failed = harvest_suite.load_modules_for_files([test_file])
        classes, omitted = harvest_suite.retreive_test_classes_for_module(
                                                         modules[0],
                                                         class_prefix='Test')

        level = 10
        filtered_classes = harvest_suite.filter_for_level(classes,level)

        assert len(filtered_classes) == 3
        for klass in filtered_classes:
            assert klass.__name__ in ['TestZero', 'TestOne','TestTwo']

    def check_level2(self):
        test_file = os.path.join(local_directory,"tests","test_p1.py")
        modules, failed = harvest_suite.load_modules_for_files([test_file])
        classes, omitted = harvest_suite.retreive_test_classes_for_module(
                                                         modules[0],
                                                         class_prefix='Test')

        level = 1
        filtered_classes = harvest_suite.filter_for_level(classes,level)

        assert len(filtered_classes) == 2
        for klass in filtered_classes:
            assert klass.__name__ in ['TestZero', 'TestOne']

class TestRetreiveTestClassesForDirectory(unittest.TestCase):

    def check_unfiltered(self):
        test_dir = os.path.join(local_directory,"tests")
        res = harvest_suite.retreive_test_classes_for_directory(test_dir,
                                                              file_prefix='',
                                                              class_prefix='')
        classes, omitted, failed = res

        assert len(classes) == 6
        class_names = ['TestZero', 'TestOne','TestTwo', 'TestP2One',
                       'TestFour','NoTestThree']
        for klass in classes:
            assert klass.__name__ in class_names

    def check_class_filtered_default(self):
        test_dir = os.path.join(local_directory,"tests")
        res = harvest_suite.retreive_test_classes_for_directory(test_dir,
                                                              file_prefix='')
        classes, omitted, failed = res

        assert len(classes) == 5

        class_names = ['TestZero', 'TestOne','TestTwo', 'TestP2One',
                       'TestFour']
        for klass in classes:
            assert klass.__name__ in class_names

class TestTestSuiteForDirectory(unittest.TestCase):

    def check_simple(self):
        test_dir = os.path.join(local_directory,"tests")
        suite = harvest_suite.test_suite_for_directory(test_dir,
                                                     recurse=0)

        assert suite.countTestCases() == 5

    def check_level1(self):
        test_dir = os.path.join(local_directory,"tests")
        suite = harvest_suite.test_suite_for_directory(test_dir, level=1,
                                                     recurse=0)

        assert suite.countTestCases() == 3

    def check_benchmark(self):
        test_dir = os.path.join(local_directory,"tests")
        suite = harvest_suite.test_suite_for_directory(test_dir, level=1,
                                                      test_prefix='benchmark_',
                                                      recurse=0)
        assert suite.countTestCases() == 1

    def check_recurse(self):
        test_dir = os.path.join(local_directory,"tests")
        suite = harvest_suite.test_suite_for_directory(test_dir, recurse=1)
        assert suite.countTestCases() == 6

    def check_omit_dir(self):
        test_dir = os.path.join(local_directory, "package")
        omit_dir = os.path.join(local_directory, "package", "blah")
        suite = harvest_suite.test_suite_for_directory(test_dir, recurse=1,
                                                     omit=[omit_dir])

        assert suite.countTestCases() == 0, "actual: %s" % suite.countTestCases()


class TestTestSuite(unittest.TestCase):
    def check_module(self):
        import p1
        suite = harvest_suite.test_suite(p1)
        assert suite.countTestCases() == 4, "actual: %s" % suite.countTestCases()

    def check_package(self):
        import package
        suite = harvest_suite.test_suite(package)
        assert suite.countTestCases() == 1, "actual: %s" % suite.countTestCases()

    def check_directory(self):
        test_dir = os.path.join(local_directory,"tests")
        suite = harvest_suite.test_suite(test_dir, recurse=1)
        assert suite.countTestCases() == 6, "actual: %s" % suite.countTestCases()

def test_suite(level=1):
    suites = []
    suites.append(unittest.makeSuite(TestPythonFilesForDirectory, 'check_'))
    suites.append(unittest.makeSuite(TestLoadModulesForFiles, 'check_'))
    suites.append(unittest.makeSuite(TestRetreiveTestClassesForModule, 'check_'))
    suites.append(unittest.makeSuite(TestFilterForLevel, 'check_'))
    suites.append(unittest.makeSuite(TestRetreiveTestClassesForDirectory, 'check_'))
    suites.append(unittest.makeSuite(TestTestSuiteForDirectory, 'check_'))
    suites.append(unittest.makeSuite(TestTestSuite, 'check_'))
    total_suite = unittest.TestSuite(suites)
    return total_suite

if __name__ == "__main__":
    # use a helper method for building the test suites.
    uber_suite = test_suite()

    # Or... eating our own dogfood.
    #import harvest_suite
    #uber_suite = harvest_suite.test_suite(harvest_suite)

    # Run the test suite!
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(uber_suite)
