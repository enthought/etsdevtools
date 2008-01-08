import unittest

class TestZero(unittest.TestCase):
    # run level for test defaults to 1
    def check_one(self):
        pass
        
    def benchmark_one(self):
        pass
    
class TestOne(unittest.TestCase):
    level = 1 # run level for test
    def check_one(self):
        pass

class TestTwo(unittest.TestCase):
    level = 2 # run level for test
    def check_one(self):
        pass
    def check_two(self):
        pass

class NoTestThree(unittest.TestCase):
    def check_one(self):
        pass
    
class NonTestClass:
    pass

def some_function():
    pass

a_variable=0            