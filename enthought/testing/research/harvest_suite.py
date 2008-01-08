""" Questions:
        1. In the event a module fails to load, we should probably still
           be able to run the remainder of the tests.  Potentially have
           a flag to toggle this.

    * Reporting on missed files.
    * try/except around methods.

"""

import sys
import os

from sets import Set

import unittest
import traceback

from test_suite import TestSuite

# files/directories to omit from testing.
default_omit = ['.svn', '.cvs']

def test_suite(location, level=10, file_prefix='test_',
               class_prefixes=['Test'], test_prefix='check_',
               omit = default_omit, recurse=1):
    """ fix me: add documentation.
    """

    if isinstance(location, basestring):
        suite = test_suite_for_directory(location, level=level,
                                         file_prefix=file_prefix,
                                         class_prefixes=class_prefixes,
                                         test_prefix=test_prefix,
                                         omit=omit,
                                         recurse=recurse)
    elif ispackage(location):
        suite = test_suite_for_package(location, level=level,
                                       file_prefix=file_prefix,
                                       class_prefixes=class_prefixes,
                                       test_prefix=test_prefix,
                                       omit=omit,
                                       recurse=recurse)
    else:
        suite = test_suite_for_module(location, level=level,
                                      class_prefixes=class_prefixes,
                                      test_prefix=test_prefix)

    return suite

def test_suite_for_module(module, level=10, class_prefixes=['Test'],
                          test_prefix="check_"):
    """ Create a test suite containing all the test classes found for this
        specific module.  Both tests in the module itself and a file named
        ``tests/test_*.py`` where ``*`` is the name of the module is found
        next to the module in the file system are included.

        level
            specifies the test types to run.  level=1 will run all
            level 1 tests.  level=5 will run all test from
            levels 1-5. The default is 10.

        test_prefix
            specifies which methods on the test class to
            include in the test suite.  It defaults to testing
            all methods prefixed with ``check_``.  Please use
            this as the standard way of denoting tests.
            ``benchmark_`` is another common prefix used to denote
            methods that are useful for timing performance of a
            library.

            Note: We don't currently have stuff set up to make use of
            ``benchmark_``, but we plan to.
    """
    full_path = module.__file__
    directory, file_name = os.path.split(full_path)

    test_path = os.path.join(directory,'tests','test_'+file_name)
    modules, failed_modules = load_modules_for_files([full_path, test_path])

    for module in modules:
        classes, omitted_classes = retreive_test_classes_for_module(module,
                                                                 class_prefixes)
        classes = filter_for_level(classes, level)

        suites = []
        for klass in classes:
            suites.append(unittest.makeSuite(klass, test_prefix))

    total_suite = TestSuite(suites, omitted_classes, failed_modules)
    return total_suite

def test_suite_for_package(package, level=10, file_prefix='test_',
                           class_prefixes=['Test'], test_prefix="check_",
                           omit=default_omit, recurse=1):
    """ Create a test suite containing all the test classes found in
        any directory living under the specified packages directory.  If
        you wish for a directory to be omitted, place an ``__omit__.py``
        file within that directory.  This will omit it and all
        sub-directories from the tests.

        level
            specifies the test types to run.  level=1 will run all
            level 1 tests.  level=5 will run all test from
            levels 1-5. The default is 10.

        test_prefix
            specifies which methods on the test class to
            include in the test suite.  It defaults to testing
            all methods prefixed with ``check_``.  Please use
            this as the standard way of denoting tests.
            ``benchmark_`` is another common prefix used to denote
            methods that are useful for timing performance of a
            library.

            Note: We don't currently have stuff set up to make use of
            ``benchmark_``, but we plan to.

        recurse
            default 1.  Search sub-packages that live within this
            package and return their test suites as well.
    """
    full_path = package.__file__
    directory, file_name = os.path.split(full_path)
    base_file, ext = os.path.splitext(file_name)

    assert base_file == "__init__", "%s is not a package" % package

    suite = test_suite_for_directory(directory, level=level,
                                     file_prefix=file_prefix,
                                     class_prefixes=class_prefixes,
                                     test_prefix=test_prefix,
                                     omit=omit,
                                     recurse=recurse)

    return suite

def test_suite_for_directory(directory, level=10, file_prefix='test_',
                             class_prefixes=['Test'], test_prefix='check_',
                             omit=default_omit, recurse=1):
    """ Create a test suite containing all the test classes found in
        in python files that live in that directory.

        level
            specifies the test types to run.  level=1 will run all level 1
            tests.  level=5 will run all test from levels 1-5. The default is 10.

        test_prefix
            specifies which methods on the test class to include in
            the test suite.  It defaults to testing all methods prefixed with
            ``check_``.  Please use this as the standard way of denoting tests.
            ``benchmark_`` is another common prefix used to denote methods that
            are useful for timing performance of a library.

        Note: We don't currently have stuff set up to make use of
        ``benchmark_``, but we plan to.
    """

    # Make sure we haven't handed in an omitted directory
    parent, base_dir = os.path.split(directory)
    if base_dir in omit:
        return TestSuite([])

    res = retreive_test_classes_for_directory(directory,
                                              file_prefix=file_prefix,
                                              class_prefixes=class_prefixes)
    classes, omitted_classes, failed_modules = res
    classes = filter_for_level(classes, level)

    suites = []
    for klass in classes:
        suites.append(unittest.makeSuite(klass, test_prefix))

    if recurse:
        sub_directories = find_subdirectories(directory, omit)
        for sub_directory in sub_directories:
            suite = test_suite_for_directory(sub_directory, level=level,
                                             file_prefix=file_prefix,
                                             class_prefixes=class_prefixes,
                                             test_prefix=test_prefix,
                                             recurse=recurse)
            suites.append(suite)

    total_suite = TestSuite(suites, omitted_classes, failed_modules)

    return total_suite

def ispackage(module):
    # fix me: Test against ext modules
    full_path = module.__file__
    directory, file_name = os.path.split(full_path)
    base_file, ext = os.path.splitext(file_name)

    return base_file == "__init__"

def find_subdirectories(directory, omit=default_omit, recurse=1):
    """ Gather all sub-directories within this directory.  If
        recurse=1 (the default), all subdirectories are also
        searched to see if they have a tests directory.

        If user would like to omit a directory, they may place
        an '__omit__.py' file in that directory.
    """
    sub_directories = []

    for file in os.listdir(directory):
        full_path = os.path.join(directory, file)
        omit_path = os.path.join(directory, file, '__omit__.py')
        if (os.path.isdir(full_path) and
            not (file in omit or full_path in omit) and
            not os.path.exists(omit_path)):
            sub_directories.append(full_path)
            if recurse :
                sub = find_subdirectories(full_path)
                sub_directories.extend(sub)

    return sub_directories

def load_modules_for_files(file_list):
    """ Given a list of python files names, load each module
        and return a list of the loaded modules.

        fix me: What should happen if the load fails for a module?
                Should we log it and continue loading others?
                This seems like a good idea to allow tests to run
                even if one test file is broken. *Currently it
                fails with an exception in this case*
    """

    modules = []
    failed_modules = []

    for full_path in file_list:
        directory, file_name = os.path.split(full_path)
        module_name, ext = os.path.splitext(file_name)

        # push the directory onto the python path.
        sys.path.insert(0, directory)

        # Now try an import the module.
        try:
            mod = __import__(module_name)
            modules.append(mod)
        except:
            res = (full_path, exc_info_as_string())
            failed_modules.append(res)
            print "Failed to load module: ", full_path
            print exc_info_as_string()

        # now remove the directory from the path
        del sys.path[0]

    return modules, failed_modules

def python_files_for_directory(directory, file_prefix=''):
    """ Return a list of all the python files in a directory.
        The absolute path for each file is returned. If
        the directory does not exists, an empty list is returned.
    """

    if os.path.exists(directory):
        # grab all the python files from the test directory
        files = os.listdir(directory)

        # filter out files that don't match the file_prefix
        if file_prefix:
            pre_len = len(file_prefix)
            files = [file for file in files if file[:pre_len] == file_prefix]

        # Convert all files names to be their full absolute path.
        full_directory_path = os.path.abspath(directory)
        files = [os.path.join(full_directory_path, file) for file in files]

        # filter out non-python files.
        python_files = [file for file in files if file[-3:] == '.py']


    else:
        python_files = []

    return python_files

def retreive_test_classes_for_module(module, class_prefixes=['Test']):
    """ Return a list of all test classes defined in a module.
        Currently, this is done by testing whether a class derives
        from unittest.TestCase.

        fix me: This may be to specific.  It may be more appropriate
                to test for a pefix name like "test_*" as the class name.
    """
    test_classes = []
    omitted_tests = []

    items = module.__dict__.items()
    for key, value in items:
        # fix me: This barfs when value is a CTraits object
        try:
            # The following failed for traits for some reason, so we're
            # using this try/except approach.
            #is_test_class = inspect.isclass(value) and \
            #                issubclass(value, unittest.TestCase
            is_test_class = issubclass(value, unittest.TestCase)
        except TypeError:
            is_test_class = 0

        if is_test_class:
            for class_prefix in class_prefixes :
                if value.__name__[:len(class_prefix)] == class_prefix:
                    test_classes.append(value)
                    break
            else:
                omitted_tests.append(value)

    return test_classes, omitted_tests

def filter_for_level(classes, level):
    """ Return a list of all classes that have a level attribute <= level.
        If a class doesn't have a level attribute, it is assumed to be
        level=1
    """
    filtered_classes = []
    default_level = 1

    for klass in classes:
        klass_level = getattr(klass, 'level', default_level)
        if klass_level <= level:
            filtered_classes.append(klass)

    return filtered_classes

def retreive_test_classes_for_directory(directory, file_prefix="test_",
                                        class_prefixes=['Test']):
    """ Retreive a list of the test classes from the python modules
        found in a directory.
    """
    python_files = python_files_for_directory(directory, file_prefix)
    modules, failed_modules = load_modules_for_files(python_files)

    # get all test classes from module.
    test_classes = []
    omitted_classes = []
    for module in modules:
        classes, omitted_classes = retreive_test_classes_for_module(module,
                                                               class_prefixes)
        test_classes.extend(classes)
        omitted_classes.extend(omitted_classes)

    #eliminate redundant classes that can occur due to imports
    test_classes = list(Set(test_classes))
    omitted_classes = list(Set(omitted_classes))

    return test_classes, omitted_classes, failed_modules

def _exc_info():
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

def _exc_info_to_string(err):
    """ Converts a sys.exc_info()-style tuple of values into a string.
    """
    return ''.join(traceback.format_exception(*err))

def exc_info_as_string():
    err = _exc_info()
    return _exc_info_to_string(err)