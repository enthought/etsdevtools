#-------------------------------------------------------------------------------
#
#  Useful trait definitions.
#
#  Written by: David C. Morrill
#
#  Date: 07/21/2006
#
#  (c) Copyright 2006 by David C. Morrill
#
#-------------------------------------------------------------------------------

""" Copyright 2006 by David C. Morrill """

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from traits.api \
    import Trait, TraitType, TraitHandler, TraitError

from traitsui.value_tree \
    import SingleValueTreeNodeObject, TraitsNode

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

# Mapping from standard Python-like relation to legal method name version:
RelationMap = {
    '>=': 'ge',
    '>':  'gt',
    '<=': 'le',
    '<':  'lt',
    '=':  'eq',
    '==': 'eq',
    '!=': 'ne'
}

#-------------------------------------------------------------------------------
#  Trait definitions:
#-------------------------------------------------------------------------------

class TraitValueHandler ( TraitHandler ):

    #---------------------------------------------------------------------------
    #  Validates that the value is a valid trait 'node':
    #---------------------------------------------------------------------------

    def validate ( self, object, name, value ):
        """ Validates that the value is a valid trait 'node'.
        """
        if (isinstance( value, SingleValueTreeNodeObject ) and
            isinstance( value.parent, TraitsNode )):
            return ( value.parent.value, value.name[1:] )

        raise TraitError

# Define the trait:
TraitValue = Trait( None, TraitValueHandler() )

#-------------------------------------------------------------------------------
#  'Size' trait:
#-------------------------------------------------------------------------------

class Size ( TraitType ):

    is_mapped     = True
    default_value = ''
    info_text = "a size of the form: ['<='|'<'|'>='|'>'|'='|'=='|'!=']ddd"

    def value_for ( self, value ):
        if isinstance( value, basestring ):
            value = value.strip()
            if len( value ) == 0:
                return ( 'ignore', 0 )

            relation = '<='
            c        = value[0]
            if c in '<>!=':
                relation = c
                value    = value[1:]
                c        = value[0:1]
                if c == '=':
                    relation += c
                    value     = value[1:]
                value = value.lstrip()

            relation = RelationMap[ relation ]

            try:
                size = int( value )
                if size >= 0:
                   return ( relation, size )
            except:
                pass

        raise TraitError

    mapped_value = value_for

    def post_setattr ( self, object, name, value ):
        object.__dict__[ name + '_' ] = value


    def as_ctrait ( self ):
        """ Returns a CTrait corresponding to the trait defined by this class.
        """
        # Tell the C code that the 'post_setattr' method wants the modified
        # value returned by the 'value_for' method:
        return super( Size, self ).as_ctrait().setattr_original_value( True )

