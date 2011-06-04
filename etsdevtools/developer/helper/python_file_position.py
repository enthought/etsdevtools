#-------------------------------------------------------------------------------
#
#  Defines the PythonFilePosition class, a plugin interchange object that
#  extends the base FilePosition class by adding Python specific information,
#  such as package, module, class and method information.
#
#  Written by: David C. Morrill
#
#  Date: 08/05/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from etsdevtools.developer.helper.file_position \
    import FilePosition

from traits.api \
    import Str

#-------------------------------------------------------------------------------
#  'PythonFilePosition' class:
#-------------------------------------------------------------------------------

class PythonFilePosition ( FilePosition ):

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The package name associated with the file position:
    package_name = Str

    # The module name associated with the file position:
    module_name = Str

    # The class name associated with the file position:
    class_name = Str

    # The method name associated with the file position:
    method_name = Str

