import unittest
from sys import stderr

from enthought.testing.harvest_suite import test_suite, default_omit

def run_tests(location, level=10, file_prefix='test_', 
              class_prefixes=['Test','test_'], test_prefix='check_',
              omit = default_omit, recurse=1, 
              run_class=unittest.TextTestRunner, verbose=1,
              stream=stderr):
    
    suite = test_suite(location, level=level, file_prefix=file_prefix, 
                       class_prefixes=class_prefixes, test_prefix=test_prefix,
                       omit=omit, recurse=recurse)         
                
    runner = run_class(verbosity=verbose, stream=stream)
    res = runner.run(suite)
    return runner, res, suite
