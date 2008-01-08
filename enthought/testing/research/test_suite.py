import unittest

class TestSuite(unittest.TestSuite):
    """ This class augments the standard TestSuite class with 
        information about test classes that were omitted from
        the test and test modules that failed to import.
    """
    def __init__(self, suites, omitted_classes=[], failed_modules=[]):
        unittest.TestSuite.__init__(self, suites)
        self.omitted_classes = omitted_classes
        self.failed_modules = failed_modules
