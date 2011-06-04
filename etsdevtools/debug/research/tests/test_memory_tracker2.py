# Standard library
import unittest

# Enthought library
from etsdevtools.debug.research.memory_tracker2 import TrackedClassObject

class TrackedClassObjectTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_list(self):
        lst = []
        tracked_object = TrackedClassObject.from_object(lst)

        self.assertEqual(tracked_object.class_name, 'list')
        self.assertEqual(tracked_object.id, id(lst))
        self.assertEqual(tracked_object.group_id(), 'list')

