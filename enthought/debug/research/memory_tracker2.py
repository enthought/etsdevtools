import gc
import weakref

from enthought.traits.api import HasTraits, Int, Str, Any, List, Dict

class TrackedClassObject(HasTraits):

    # id of object
    id = Int

    # name of the class for the object
    class_name = Str

    # weakref to actual object.
    object_ref = Any

    @classmethod
    def from_object(cls, obj):
        obj_id = id(obj)
        class_name = obj.__class__.__name__

        # fixme.  Don't have a strong handle on the difference between
        #         ref() and proxy()
        try:
            object_ref = weakref.ref(obj)
        except TypeError:
            # Some types like lists are not weakreferencable...
            object_ref = None

        return cls(id=obj_id, class_name=class_name, object_ref=object_ref)


    def group_id(self):
        return self.class_name

    def __repr__(self):
        """ Short string representation of object.
        """
        s = "%s(%s)" % (self.class_name, self.id)
        return s

class TrackedClassObjectFactory(HasTraits):

    # A Class or type object.  Default to matching any object.
    matching_class = Any(object)

    # The TrackedObject class to be created for matching classes
    factory_class = Any(TrackedClassObject)

    def match(self, obj):
        return isinstance(obj, self.matching_class)

    def from_object(self, obj):
        return self.factory_class.from_object(obj)



class MemoryState(HasTraits):

    # List of trackers for objects in memory.
    tracked_object_factories = List(Any)

    total_object_count = Int

    untracked_object_count = Int

    tracked_items = Dict(Str, Any)

    def _tracked_object_factories_default(self):
        self.tracked_object_factories = [TrackedClassObjectFactory]

    def capture_state(self):
        """ Capture the current state of the system memory
        """

        # Clean up any objects that can be so that we don't get spurious counts.
        gc.collect()

        objs = gc.get_objects()
        self.total_object_count = len(objs)

        for obj in objs:
            for tracker in self.tracked_object_factories:
                if tracker.match(obj):
                    tracked_item = tracker.from_object(obj)
                    self.tracked_items[tracked_item.group_id] = tracked_item
            else:
                self.untracked_object_count += 1
