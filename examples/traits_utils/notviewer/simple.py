""" A simple example of the NotViewer in action.

This script opens a simple Traits UI view together with the Traits
notification viewer window. Start the recording and play with the traits to
see what happens behind the scenes.
"""

from traits.api import *
from traitsui.api import *
from etsdevtools.traits_utils.notviewer import NotViewer


class Foo(HasTraits):
    a = Int

    def _a_changed(self):
        pass

    b = Int

    def _b_changed(self):
        pass


class Bar(HasTraits):
    foo = Instance(Foo)

    twice_a = Int

    moo = Range(1, 100)

    @on_trait_change('foo.a')
    def _react_to_foo_a(self):
        self.twice_a = self.foo.a * 2
        self.foo.b = self.foo.a + 1
        self.foo.b = self.foo.a + 2

    traits_view = View(
        Item('object.foo.a'),
        Item('twice_a'),
        Item('moo'),
    )


foo = Foo(a=32)

bar = Bar(foo=foo)

notviewer = NotViewer()
ui = notviewer.edit_traits()

bar.configure_traits()
