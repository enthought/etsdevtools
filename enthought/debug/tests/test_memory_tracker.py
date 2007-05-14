# Standard library
import unittest

# Enthought library
from enthought.traits.api import HasTraits, Any
from enthought.debug.memory_tracker import MemoryState, get_all_referrers


class MemoryStateTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_capture_state(self):
        state = MemoryState()
        state.capture_state()

        # really weak test...
        self.assertTrue(len(state.captured_ids)>0)

    def test_find_new_objects_matching_class(self):
        class Foo:
            pass

        # Have a foo before in memory just to make things intersting
        pre_foo = Foo()

        state = MemoryState()
        state.capture_state()
        foo = Foo()
        new_foos = state.find_new_objects_matching_class(Foo)

        self.assertEqual(len(new_foos), 1)
        self.assertEqual(id(new_foos[0]), id(foo))

    def test_get_all_referrers(self):
        """ Are all items in a reference chain actual found in the reference chain?
        """

        class Referrer:
            pass

        class Leaf:
            pass

        # Have a foo before in memory just to make things intersting
        root=Referrer()
        intermediate = Referrer()
        leaf = Leaf()
        intermediate.child = leaf
        root.child = intermediate

        referrers = get_all_referrers(leaf)
        self.assertTrue(id(root) in referrers)
        self.assertTrue(id(intermediate) in referrers)

    def test_get_all_referrers2(self):

        class Referrer:
            pass

        l = []

        # Have a foo before in memory just to make things intersting
        leaf = Referrer()
        l.append(leaf)

        referrers = get_all_referrers(leaf)

        self.assertTrue(id(l) in referrers)


    def test_find_leak_boundary_ids(self):

        class Referrer:
            pass

        l = []

        state = MemoryState()
        state.capture_state()

        # Have a foo before in memory just to make things intersting
        leaf = Referrer()
        l.append(leaf)

        leaks = state.find_leak_boundary_ids(leaf)

        self.assertEqual(len(leaks), 1)

        leaked_ids = leaks[id(l)]

        self.assertEqual(leaked_ids[0], id(leaf))

    def _find_leak_boundary_for_class_helper(self, referrer_class):

        # Construct the root object before we capture the 'peramanent' memory
        # state (or existing memory state...)
        root=referrer_class()
        root.name = 'root'
        print
        print 'id:', id(root)

        # Snapshot all the object ids in the process.
        state = MemoryState()
        state.capture_state()

        # Now build a simple dependency graph: root->intermediate->leaf
        intermediate = referrer_class()
        root.child = intermediate

        leaf = referrer_class()
        intermediate.child = leaf

        # We are pretending that we know 'leaf' is leaked here, and we
        # want to find any objects prior to our capture_state call that
        # refer directly or indirectly to leaf.
        leaks = state.find_leak_boundary_objects(leaf)

        referrer_ids = get_all_referrers(leaf)
        assert(id(root) in referrer_ids)

        import gc
        referrers = gc.get_referrers(intermediate)
        print [type(item) for item in referrers]
        print root.__dict__ in referrers

        self.assertEqual(len(leaks), 1)

        leak_holder, leaked_objects = leaks[0]
        print leaked_objects[0].name
        self.assertEqual(root, leak_holder)
        self.assertEqual(intermediate, leaked_objects[0])


    def _test_find_leak_boundary_oldstyle_class(self):

        class Referrer:
            pass

        self._find_leak_boundary_for_class_helper(Referrer)



    def _test_find_leak_boundary_newstyle_class(self):

        class Referrer(object):
            pass

        self._find_leak_boundary_for_class_helper(Referrer)

    def test_find_leak_boundary_hastraits_class(self):

        class Referrer(HasTraits):
            child = Any
            pass

        self._find_leak_boundary_for_class_helper(Referrer)


if __name__ == '__main__':
    unittest.main()