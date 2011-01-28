###########################################################################
# File:    util.py
# Project: enthought.endo
# Date:    2008-3-05
# Author:  Janet Swisher
#
# Description:
#   Utility functions
#
###########################################################################
import types

def alpha_sort(lst):
    """Sorts a list in place alphabetically, rather than lexicographically.

    Ties are broken lexicographically; i.e., 'Car' sorts before 'car'.
    Handles lists of strings, and lists of tuples whose first item is a string.
    From http://www.answermysearches.com/python-how-to-sort-alphabetically/319/
    """
    if len(lst) > 0:
        if type(lst[0]) == types.StringType:
            lst.sort(key=lambda s: (s.lower(), s))
        elif type(lst[0]) == types.TupleType and type(lst[0][0]) == types.StringType:
            lst.sort(key=lambda t: (t[0].lower(), t[0]))



