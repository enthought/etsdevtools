# Standard library imports
import sys
import gc
import weakref

# Enthought library imoprts
from enthought.traits.api import HasTraits, Int, Str, Any, List, Dict, Property

class MemoryState(HasTraits):

    # List of all object ids at a point in time within the program.
    captured_ids = Any

    difference_ids = Property

    def capture_state(self):

        self.captured_ids = set([id(obj) for obj in self.get_objects()])

        return

    def _get_difference_ids(self):

        current_ids = set([id(obj) for obj in self.get_objects()])

        return current_ids.difference(self.captured_ids)


    def find_new_objects_matching_class(self, klass):

        # Get all objects in the process that are from this class.
        klass_objs = [obj for obj in self.get_objects()
                      if isinstance(obj, klass)]

        # Create a dict that maps object ids to the objects
        id_to_object = {}
        for item in klass_objs:
            id_to_object[id(item)] = item

        # List of leaked items
        new_items = []
        for obj_id in self.difference_ids:
            if id_to_object.has_key(obj_id):
                new_items.append(id_to_object[obj_id])

        return new_items

    def find_leak_boundary_ids(self, leaked_item):
        """
            Given an object that you know has leaked, finds the items from
            the captured_ids that refer to objects in the reference chain
            to the leaked item.  This returns a dict with keys that are
            object ids in the captured_ids list.  The value is a list of all
            the object ids that are in the reference chain to leaked_item
            that are *not* in the captured_ids list.

            Clear as mud.
        """

        # Find all items that are in the reference chain to this item.
        referrer_ids = get_all_referrers(leaked_item)

        # Remove the calling frame's id from the referrer_ids because we don't
        # care about references from it.
        id_to_object = id_to_existing_objects()


        # This is the set of referrring ids that weren't saved in our
        # 'permanent' id set.
        leaked_ids = referrer_ids  - self.captured_ids

        # Remove references that only exist in local scope.
        leaked_ids &= set(id_to_object.keys())

        bad_links = dict()

        # Found all items in the leaked set that are referred to by something
        # in the permanent set.
        for item_id in leaked_ids:
            referrers = gc.get_referrers(id_to_object[item_id])
            referrer_ids = set([id(item) for item in referrers])
            # Find all objects in the 'permanent' (captured) ids that refer
            # to the leaked item.
            permanent_referrer_ids = referrer_ids & self.captured_ids
            for permanent_id in permanent_referrer_ids:
                referred_to = bad_links.setdefault(permanent_id,[])
                referred_to.append(item_id)

        cur_frame_id = id(sys._getframe())
        back_frame_id = id(sys._getframe().f_back)

        for remove_id in [cur_frame_id, back_frame_id]:
            if bad_links.has_key(remove_id):
                del bad_links[remove_id]

        return bad_links

    def find_leak_boundary_objects(self, leaked_item):
        """ Return the objects along the boundary between 'permanent' memory
            and 'leaked' memory.

            See find_leak_boundary_ids for more info.
        """
        id_leak_dict = self.find_leak_boundary_ids(leaked_item)
        print
        print id_leak_dict

        # We need to check and see if the calling frame is being flagged as
        # leaked.  If it is, remove it.
        back_frame_id = id(sys._getframe().f_back)
        if id_leak_dict.has_key(back_frame_id):
            del id_leak_dict[back_frame_id]
        print id_leak_dict

        # Translate all ids back into their actual objects
        object_leak_list = id_dict_to_object_tuples(id_leak_dict)

        # The first object in each object_leak_list pair is the 'referring'
        # object.  Often this is a dictionary that is actually the __dict__
        # of a class object.  Knowing that class object is much more
        # informative than knowing the dict object, so we remap here.
        # fixme: refactor to separate method.
        useful_object_leak_list = []
        for referrer, referred_to in object_leak_list:
            print
            print type(referrer)
            if isinstance(referrer, dict):
                referrer_parents = gc.get_referrers(referrer)
                print [type(r) for r in referrer_parents]
                for parent in referrer_parents:
                    if hasattr(parent, '__dict__'):
                        referrer = parent
                        break
            useful_object_leak_list.append((referrer, referred_to))

        print
        print useful_object_leak_list
        return useful_object_leak_list


    def get_objects(self):
        """ Always collect before we get objects from gc.
        """
        gc.collect()
        objs = gc.get_objects()

        return objs
    
    def get_new_objects(self):
        ids = self.difference_ids
        id_map = id_to_existing_objects()
        return [id_map.get(id_num, None) for id_num in ids]

def get_all_referrers(item):
    """ Return all objects that are in the reference chain to this item.

        Note: This is far from an optimal algorithm, but until speed is
              an issue, we're not going to worry about it.
    """
    gc.collect()

    # Get a mapping of ids to objects for all objects *currently* in the system.
    id_to_object = id_to_existing_objects()

    # Work with a list of ids to minimize our references to actual objects
    # and because ids are always hashable and not all objects (like dicts)
    # are.
    referrer_ids = set([id(item)])

    cur_len = 0
    while len(referrer_ids) > cur_len:
        cur_len = len(referrer_ids)
        # Convert ids back to objects for all objects currently in our
        # referrers list.
        args = [id_to_object[item_id] for item_id in referrer_ids]

        # Get references to these objects
        new_referrers = gc.get_referrers(*args)

        # Filter out any ids that didn't exist at the top of this function
        # call (items created in this function).
        new_referrer_ids = [id(item) for item in new_referrers
                            if id(item) in id_to_object]

        # Union the new referrer ids with the old set.
        referrer_ids |= set(new_referrer_ids)

    return referrer_ids

def id_to_existing_objects():
    """ Return a mapping of ids to objects for all objects in the system.
    """
    gc.collect()
    objs = gc.get_objects()
    print len(objs)
    object_dict = dict(zip([id(obj) for obj in objs], objs))
    # Remove our current stack frame from this list so that we don't hold
    # an extra reference to everything
    del object_dict[id(sys._getframe())]
    return object_dict
    

def id_dict_to_object_tuples(id_dict):
    """ Convert a dictionary of id: [id1, id2, ...] into a list of tuples
        (key_object, [value_object1, value_object2, ...] of actual objects.

        We change to tuples here, because many objects (like dicts) cannot
        be the keys in a dictionary.
    """
    object_list = []

    id_to_object = id_to_existing_objects()

    for key, values in id_dict.items():
        # If we don't find the object in the current system objects, just
        # use the id.
        object_key = id_to_object.get(key, key)
        object_values = [id_to_object.get(value, value) for value in values]
        object_list.append((object_key, object_values))

    return object_list

def filter_out_dead_objects(leak_dict):
    """
    """

    results = []

    id_to_object = id_to_existing_objects()
    for key, value in leak_dict.items():
        if id_to_object.has_key(key):
            new_key = id_to_object[key]
            results.append(new_key)

    return results

