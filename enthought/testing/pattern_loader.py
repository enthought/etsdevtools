import unittest
import re
import fnmatch

class RegexLoader(unittest.TestLoader):
    def __init__(self, pattern):
        unittest.TestLoader.__init__(self)
        unittest.TestLoader.testMethodPrefix = pattern

    def getTestCaseNames(self, testCaseClass):
        """Return a sorted sequence of method names found within testCaseClass
        """
        testFnNames = filter(lambda n,p=self.testMethodPrefix: re.match(p, n) is not None,
                             dir(testCaseClass))
        for baseclass in testCaseClass.__bases__:
            for testFnName in self.getTestCaseNames(baseclass):
                if testFnName not in testFnNames:  # handle overridden methods
                    testFnNames.append(testFnName)
        if self.sortTestMethodsUsing:
            testFnNames.sort(self.sortTestMethodsUsing)
        return testFnNames

class GlobLoader(unittest.TestLoader):

    def __init__(self, pattern):
        unittest.TestLoader.__init__(self)
        unittest.TestLoader.testMethodPrefix = pattern
            
    def getTestCaseNames(self, testCaseClass):
        """Return a sorted sequence of method names found within testCaseClass
        """
        testFnNames = filter(lambda n,p=self.testMethodPrefix: fnmatch.fnmatch(n, p),
                             dir(testCaseClass))
        for baseclass in testCaseClass.__bases__:
            for testFnName in self.getTestCaseNames(baseclass):
                if testFnName not in testFnNames:  # handle overridden methods
                    testFnNames.append(testFnName)
        if self.sortTestMethodsUsing:
            testFnNames.sort(self.sortTestMethodsUsing)
        return testFnNames
