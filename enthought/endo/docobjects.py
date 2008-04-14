###########################################################################
# File:    docobjects.py
# Project: endo
# Date:    2005-06-09
# Author:  David Baer
# 
# Description:
#   Documentable objects
# 
###########################################################################

"""Architecture for documentable objects in Python code.

These classes correspond roughly to elements of the AST, but with
added information -- for example, linking modules to parent packages
and providing a namespace for resolving identifiers."""

import sys
import compiler.ast as ast
from enthought.endo.namespace import Namespace
from sets import Set

# need types.FunctionType and types.TypeType
import types

# import warnings as a different name for warnings that may occur
# when this module is imported, otherwise the var should be set by
# the importer so they can maintain the same warnings filters
import warnings as local_warnings
warnings = None

# Local imports
from util import alpha_sort

# traits primitives
TRAITS_PRIMITIVES = Set([ 'enthought.traits.api.' + x for x in 
                          [ 'Trait' ] ])
_trait_vars = {}
# traits base classes -- constructed later
HAS_TRAITS_BASES = Set()
# base type for all traits
CTRAIT_TYPE = None

def _is_trait(val):
    return (  # Find traits like Event = TraitFactory(Event)
              isinstance(val, enthought.traits.api.TraitFactory)
              # Find traits like ReadOnly = Ctrait(6)
              or isinstance(val, enthought.traits.api.CTrait)
              # Find both 'class BaseRange(TraitType)' and 'class TraitRange(TraitHandler)'
              or ( type(val) == types.TypeType and
                   issubclass(val, enthought.traits.api.BaseTraitHandler))
              # Find traits like DictStrAny
              or isinstance(val, enthought.traits.api.BaseTraitHandler) 
            )

# attempt to build a list of traits primitives from enthought.traits.api package
try:
    import enthought.traits.api
    _traits_vars= vars(enthought.traits.api)
    CTRAIT_TYPE = enthought.traits.api.CTrait
except ImportError:
    local_warnings.warn("enthought.traits.api not found\n")

            
TRAITS_PRIMITIVES.update([ 'enthought.traits.api.' + sym 
    for sym in _traits_vars.keys()
    if _is_trait(_traits_vars[sym]) or 
    # Find traits like Constant or Delegate
    ( ord('A') <= ord(sym[0]) <= ord('Z') and
    type(_traits_vars[sym]) == types.FunctionType ) ])

_temp = [ sym for sym in _traits_vars.keys()
          if isinstance(_traits_vars[sym], enthought.traits.api.MetaHasTraits) and
             issubclass(_traits_vars[sym], enthought.traits.api.HasTraits) ]
HAS_TRAITS_BASES.update([ 'enthought.traits.api.' + sym for sym in _temp ] +
                        [ 'enthought.traits.has_traits.' + sym for sym in _temp ])

# attempt to build add traits.ui primitives to the list
try:
    import enthought.traits.ui.api
    _traits_vars = vars(enthought.traits.ui.api)
except ImportError:
    local_warnings.warn("enthought.traits.ui.api not found\n")
    
TRAITS_PRIMITIVES.update([ 'enthought.traits.ui.api.' + sym 
    for sym in _traits_vars.keys() if _is_trait(_traits_vars[sym]) ])
HAS_TRAITS_BASES.update([ 'enthought.traits.ui.api.' + sym 
            for sym in _traits_vars.keys()
            if isinstance(_traits_vars[sym], enthought.traits.api.MetaHasTraits) 
            and issubclass(_traits_vars[sym], enthought.traits.api.HasTraits) ] )

    
def _indent_multiline_string(s, indent):
    i = ' ' * indent
    return ''.join([ '%s%s\n' % (i, line) for line in s.split('\n') ])

def _eval_context(obj, dotted_name):
    if dotted_name == '':
        return obj
    components = dotted_name.split('.')
    front = components[0]
    rest = '.'.join(components[1:])
    if obj.__dict__.has_key(front):
        return _eval_context(obj.__dict__[front], rest)
    else:
        raise KeyError, front

def import_obj(name):
    pos = name.rfind('.')
    if pos != -1:
        components = name.split('.')
        last = len(components) - 1
        while last > 0:
            try:
                module_name = '.'.join(components[:last])
                rest = '.'.join(components[last:])
                module_obj = __import__(module_name)
                attr_obj = _eval_context(module_obj, rest)
                return attr_obj
            except:
                last -= 1
    raise ImportError, name

def check_trait_import(name):
    obj = import_obj(name)
    return type(obj) == CTRAIT_TYPE

def check_has_traits_import(name):
    obj = import_obj(name)
    return issubclass(obj, enthought.traits.api.HasTraits)

class DocObject(Namespace):
    """ documentable object parent class

    Notable attributes:
    
     - name   : name of object
     - file   : filename (path relative to top of tree) of file in which object
                is defined
     - lineno : line on which object is defined
     - parent_module:
                DocObject for module in which the object is defined
     - docstring:
                documentation for object (Python docstring if available)
     - children:
                DocObject nodes that are "children" of this object
    
                (e.g. class methods, attributes)
    """
    def __init__(self, name, abs_name, file, lineno, parent_module = None,
                 docstring = "", children = [ ]):
        """Constructor

          Don't call this directly -- instead, use the fromAST static methods
          
          - name     : object name
          - abs_name : dotted object name
          - file     : file where defined
          - lineno   : line number of definition
          - parent_module : module object where defined
          - docstring: documentation
          - children : list of children
        """
        Namespace.__init__(self, parent_module, name)
        self.name_list = abs_name.split('.')
        self.abs_name = abs_name
        self.file = file
        self.lineno = lineno
        if docstring is None:
            self.docstring = ""
        else:
            self.docstring = docstring
        self.children = children
        self.parent_module = parent_module

    def _find_children(options, filename, ast_children, module_object,
                       name_prefix = ''):
        "recursively process children in AST"
        children = [ ]
        for child in ast_children:
            if isinstance(child, ast.Class):
                if child.name[0] == '_' and not options.include_protected:
                    continue
                child_object = Class.fromAST(options, filename, child,
                                             module_object)
                name_in_module = child.name
                if name_prefix:
                    name_in_module = name_prefix + '.' + name_in_module
            elif isinstance(child, ast.Function):
                if child.name[0] == '_' and child.name[:2] != '__' \
                       and not options.include_protected:
                    continue
                child_object = Function.fromAST(options, filename, child,
                                                module_object)
                name_in_module = child.name
                if name_prefix:
                    name_in_module = name_prefix + '.' + name_in_module
            elif isinstance(child, ast.Assign):
                if len(child.nodes) != 1 or not isinstance(child.nodes[0], ast.AssName):
                    continue
                # single attr assignment
                attr_name = child.nodes[0].name
                    
                # check for protected attribute
                if attr_name[0] == '_' and not options.include_protected:
                    continue

                # check for function with same name
                objs = [ x for x in children if isinstance(x, Function)
                         and x.name == attr_name ]
                if len(objs) > 0:
                    func_obj = objs[0]

                    # check for function name on RHS
                    rhs_expr = child.expr
                    if isinstance(rhs_expr, ast.CallFunc) and \
                           isinstance(rhs_expr.node, ast.Name):
                        self_ref = False
                        params = [ ]
                        for arg in rhs_expr.args:
                            if isinstance(arg, ast.Name) and arg.name == func_obj.name:
                                self_ref = True
                            else:
                                params.append(arg)
                        if self_ref:
                            # don't record assignment -- need to qualify
                            # function definition
                            qualification = rhs_expr.node.name

                            # TODO: give 'qualification' more info
                            func_obj.qualifications.append(qualification)
                            
                            # do not append this as an attribute
                            continue
                                
                    
                child_object = Attribute.fromAST(options, filename, child,
                                                     module_object)
                name_in_module = child.nodes[0].name
                if name_prefix:
                    name_in_module = name_prefix + '.' + name_in_module
            else:
                continue

            # at this point, child_object, name_in_module are assigned
            module_object.bind(name_in_module, child_object)
            children.append(child_object)

        return children

    _find_children = staticmethod(_find_children)

    def fromAST(*args):
        "abstract -- don't call this"
        # should fail
        assert False
    fromAST = staticmethod(fromAST)

    def get_descendants(self, node_type = None):
        """get all descendants of this node (generator)

           - node_type (optional) : if specified, only children that are
             instances of node_type will be returned
        """
        if node_type is None: node_type = DocObject

        if isinstance(self, node_type):
            yield self

        for child in self.children:
            for d in child.get_descendants(node_type):
                yield d

    def _divide_list(the_list):
        "split list into object types (attr_list, class_list, func_list, trait_list)"
        attr_children = [ ]
        class_children = [ ]
        func_children = [ ]
        traits_children = [ ]

        #print "Checking type of items:"
        # build up lists, adding names for easy alphabetization
        for child in the_list:
            #print "\t%s" % child.name
            if isinstance(child, Function):
                func_children.append((child.name, child))
            elif isinstance(child, Class):
                class_children.append((child.name, child))
            elif isinstance(child, Attribute):
                if child.is_trait():
                    traits_children.append((child.name, child))
                else:
                    attr_children.append((child.name, child))

        # sort by name
        alpha_sort(attr_children)
        alpha_sort(class_children)
        alpha_sort(func_children)
        alpha_sort(traits_children)

        # discard names
        attr_children = [ x[1] for x in attr_children ]
        class_children = [ x[1] for x in class_children ]
        func_children = [ x[1] for x in func_children ]
        traits_children = [ x[1] for x in traits_children ]

        return attr_children, class_children, func_children, traits_children

    _divide_list = staticmethod(_divide_list)
    
    def divide_children(self):
        """
        Split children of documentable object
        
        Returns tuple: (attr_children, class_children, func_children, trait_children)
        """
        return self._divide_list(self.children)

    def toString(self, indent = 0, step = 4):
        result = self.print_node(indent)
        result += ''.join([ child.toString(indent + step, step) for child in self.children ])
        return result

    def is_pkg_index(self):
        "return True if object is a package index (i.e. __init__.py)"
        return self.file[-11:] == '__init__.py'

    def is_concrete(self):
        """return True if object is in code that has been scanned,
        False if it is an external ref"""
        return True

    def index(self):
        "Return dictionary of modules, indexed by name"
        result = Namespace.index(self)
        return dict([ (k, v) for k, v in result.items() if isinstance(v, Module) ])

    def bind(self, name, obj):
        "Bind name to obj in this object's (self's) namespace"
        Namespace.bind(self, name, obj)
        DocObject.GLOBAL[self.name + '.' + name] = obj

    def resolve_global(self, name):
        return DocObject.GLOBAL.get(name)

    def __repr__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.abs_name)

    GLOBAL = { }

class _OpaqueRef(DocObject):
    """
    An opaque reference refers to an object that is outside of the package
    being documented or is otherwise inaccessible to the document tool.

    Opaque references are uniquely specified by their fqn, so that they can
    be tested for identity with a well-known name (e.g.
    enthought.traits.HasTraits)

    This class is for internal use only.  Instances of this class are created
    by the import resolver and are exposed only through Namespace.resolve().
    Use obj.abs_name == NAME to test whether the contextual obj references the
    absolute NAME.
    """
    def __init__(self, abs_name):
        pos = abs_name.rfind('.')
        if pos == -1:
            name = abs_name
        else:
            name = abs_name[pos+1:]
        DocObject.__init__(self, name, abs_name, '', 0, None)

    def is_concrete(self):
        return False

    ALL_REF = { }

    def new_ref(abs_name):
        if _OpaqueRef.ALL_REF.has_key(abs_name):
            return _OpaqueRef.ALL_REF[abs_name]
        else:
            result = _OpaqueRef(abs_name)
            _OpaqueRef.ALL_REF[abs_name] = result
            return result
    new_ref = staticmethod(new_ref)

class Module(DocObject):
    """ documentable module """

    def __init__(self, name, file, lineno, docstring = "",
                 children = [ ]):
        abs_name = name
        name = name.split('.')[-1]
        DocObject.__init__(self, name, abs_name, file, lineno, None,
                           docstring, children)

        # not detectable through AST -- set this later
        self.sub_modules = [ ]

        # these need to be resolved with a second pass, once all package modules
        #  have been read, so that we can resolve identifiers in the module
        #  namespace
        self.unresolved_imports = [ ]

        # this is for debugging purposes -- it really should stay empty if everything
        #  is resolved
        self.unresolved_names = [ ]

    def add_sub_module(self, module_obj):
        """ Add module to package """
        self.sub_modules.append(module_obj)
        
    def sort_sub_modules(self):
        """ Sort submodules by name """
        sm = [ (m.name, m) for m in self.sub_modules ]
        alpha_sort(sm)
        sm = [ m[1] for m in sm ]

        self.sub_modules = sm

    def fromAST(options, name, filename, module_node):
        """Create module object from AST module node

           - options : command line options
           - name : name of module
           - filename : file name of module code
           - module_node : AST node for module
        """
        assert isinstance(module_node, ast.Module)

        # read docstring
        docstring = module_node.doc

        # create object first, add children later (needed for linking back to
        #  module node)
        result = Module(name, filename, module_node.lineno, docstring, [ ])

        # scan children
        children = DocObject._find_children(options, filename,
                                            module_node.node.nodes, result)

        # add children
        result.children = children

        # locate imports and mark for later resolution
        for stmt in module_node.node.nodes:
            if isinstance(stmt, ast.Import) or isinstance(stmt, ast.From):
                result.unresolved_imports.append(stmt)

        # return module object
        return result
    fromAST = staticmethod(fromAST)

    def resolve_imports(self, module_db, visited = Set()):
        """
        module_db is a mapping of fully qualified module names to module objects

        visited is the set of visited module objects -- ensures that we don't
           
        """

        name_prefix = self.name_prefix()

        # prevent circular traversal
        if self in visited:
            return
        visited.add(self)

        i = 0
        num = len(self.unresolved_imports)

        # we will be placing names we couldn't resolve back on the list,
        #  but in no case do we want to make a second attempt!
        while i < num:
            i += 1
            dep = self.unresolved_imports[0]
            self.unresolved_imports = self.unresolved_imports[1:]

            if isinstance(dep, ast.Import):
                # goody -- this is easy

                for module_name, alias in dep.names:
                    if alias is None:
                        alias = module_name

                    # locate the module we're importing
                    if module_db.has_key(module_name):
                        # absolute import
                        target_module = module_db[module_name]
                    elif module_db.has_key(name_prefix + module_name):
                        # relative import
                        target_module = module_db[name_prefix + module_name]
                    else:
                        # couldn't locate module -- punt

                        # add module as an opaque reference
                        self.bind(alias, _OpaqueRef.new_ref(module_name))

                        # resolve other names
                        continue

                    # we have been successful in locating the module
                    #  -- now bind it in this module's namespace
                    self.bind(alias, target_module)

            elif isinstance(dep, ast.From):
                module_name = dep.modname

                # locate the module we're importing from
                if module_db.has_key(module_name):
                    # absolute import
                    abs_name = module_name
                    target_module = module_db[module_name]
                elif module_db.has_key(name_prefix + module_name):
                    # relative import
                    abs_name = name_prefix + module_name
                    target_module = module_db[abs_name]
                else:
                    # couldn't locate module -- punt

                    # bind imported names as opaque references
                    for name, alias in dep.names:
                        if name == '*':
                            # can't create opaque references without names
                            self.unresolved_names.append(module_name)
                            continue

                        if alias is None:
                            alias = name

                        self.bind(alias, _OpaqueRef.new_ref(module_name + '.' + name))

                    # try to resolve other imports
                    continue

                sub_prefix = abs_name
                if target_module.is_pkg_index():
                    sub_prefix += '.'
                else:
                    dot = sub_prefix.rfind('.')

                    # if dot present, name prefix is everything up to and
                    #   including the last dot in the name
                    #   (e.g. enthought.docutils.docobjects becomes
                    #   'enthought.docutils.')
                    if dot == -1:
                        sub_prefix = ''
                    else:
                        sub_prefix = sub_prefix[:dot+1]

                # resolve all symbols in target module
                target_module.resolve_imports(module_db, visited)

                for name, alias in dep.names:
                    if name == '*':
                        # import all names from target module
                        self.copy(target_module)
                    else:
                        if alias is None:
                            alias = name

                        # attempt to resolve name
                        target = target_module.resolve(name)
                        if target is None:
                            # this shouldn't happen, but be prepared
                            self.unresolved_names.append(abs_name + '.' + name)
                        else:
                            # duplicate binding in this namespace
                            self.bind(alias, target)

                # end loop through "from ... import ... as ..., ... as ..."

            # end if

        # end while loop
        
        ###  keep silent for now -- useful for debugging
        #if len(self.unresolved_names) > 0:
        #    warnings.warn("unresolved names in module %s\n" % self.name)
        #    for n in self.unresolved_names:
        #        sys.stderr.write("   - %s\n" % n)

    def is_package(self):
        return self.file[-11:] == '__init__.py'

    def name_prefix(self):
        "Return module prefix (i.e. 'enthought.' for enthought.chaco)"
        if self.is_package():
            return self.abs_name + '.'
        else:
            pos = self.abs_name.rfind('.')
            if pos == -1:
                return self.abs_name + '.'
            else:
                return self.abs_name[:pos+1]
    
    def get_imported_objects(self):
        """
        return all objects in this module's namespace but which are not
        defined in this module

        result format: [ (local_name, obj), (local_name, obj), ... ]
        """
        result = [ (name, obj) for name, obj in self.get_objects() 
                    if obj.parent_module is not self ]
        alpha_sort(result)
        return result
        
    def print_node(self, indent):
        indent_str = " " * indent
        indented_docstring = _indent_multiline_string(self.docstring, indent)
        return """
%s%s (%s)
%s----------------------------------------------------------------------
%s
""" % (indent_str, self.name, self.file, indent_str, indented_docstring)

class Function(DocObject):
    """ documentable function """
    def __init__(self, name, file, lineno, argnames, defaults, parent_module, 
                 varargs=0, kwargs=0, docstring = "", children = [ ]):
        DocObject.__init__(self, name, parent_module.abs_name + '.' + name,
                           file, lineno, parent_module, docstring, children)
        self.argnames = argnames
        self.defaults = defaults
        self.varargs = varargs
        self.kwargs = kwargs

        # qualifications to function (e.g. 'staticmethod')
        self.qualifications = [ ]

    def fromAST(options, filename, function_node, module_object):
        """Create function object from AST function node

           - options : command line options
           - filename : file name of function code
           - function_node : AST node for function
           - module_object : docobjects.Module instance for parent module
        """
        assert isinstance(function_node, ast.Function)

        docstring = function_node.doc
        argnames = function_node.argnames
        defaults = function_node.defaults

        return Function(function_node.name, filename, function_node.lineno,
                        argnames, defaults, module_object, function_node.varargs,
                        function_node.kwargs, docstring)

    fromAST = staticmethod(fromAST)

    def print_node(self, indent):
        return ' ' * indent + 'FUNCTION %s (%s:%d)\n%s\n' % (self.name, self.file, self.lineno, _indent_multiline_string(self.docstring, indent))

class Class(DocObject):
    """ documentable class definition """
    def __init__(self, name, file, lineno, bases, parent_module,
                 docstring = "", children = [ ]):
        DocObject.__init__(self, name, parent_module.abs_name + '.' + name,
                           file, lineno, parent_module, docstring, children)
                           
        self.bases = bases

        # cache for inherited_children calls
        self._inh_result = None

    def _base_to_string(base):
        if isinstance(base, ast.Getattr):
            return Class._base_to_string(base.expr) + '.' + base.attrname
        elif isinstance(base, ast.Name):
            return base.name
        elif isinstance(base, ast.CallFunc):
            args = [Class._base_to_string(arg) for arg in base.args]
            return Class._base_to_string(base.node) + '(' + ','.join(args) + ')'
        else:
            raise TypeError, "base must be Getattr, Name, or CallFunc"
    _base_to_string = staticmethod(_base_to_string)

    def fromAST(options, filename, class_node, module_object):
        """Create class object from AST class node

           - options : command line options
           - filename : file name of class code
           - class_node : AST node for class
           - module_object : docobjects.Module instance for parent module
        """
        assert isinstance(class_node, ast.Class)

        docstring = class_node.doc
        bases = [ ]
        bases = class_node.bases

        children = [ ]
        result = Class(class_node.name, filename, class_node.lineno, bases,
                       module_object, docstring, children)

        children = DocObject._find_children(options, filename,
                                            class_node.code.nodes, result,
                                            name_prefix = class_node.name)

        result.children = children
        # add children to class namespace
        for ch in children:
            result.bind(ch.name, ch)

        return result

    fromAST = staticmethod(fromAST)

    def _inh(self):
        "build tuple of dictionaries of inherited stuff"
        if self._inh_result is not None:
            return self._inh_result
        
        result = { }
        for base in self.get_bases():
            # get inherited stuff
            if isinstance(base, Class):
                result.update(base._inh())

        result.update(dict([ (obj.name, obj) for obj in self.children ]))

        self._inh_result = result
        
        return result
        
    def inherited_children(self):
        "Like divide_children, only compiles all the objects from base classes"
        inherited_stuff = self._inh()

        # remove objects documented in current class
        for obj in self.children:
            if inherited_stuff.has_key(obj.name):
                del inherited_stuff[obj.name]

        return self._divide_list(inherited_stuff.values())
    
    def print_node(self, indent):
        super_classes = _indent_multiline_string(
                            ''.join([ 'inherits from %s\n'
                                         % self._base_to_string(sup)
                                      for sup in self.bases ]),
                            indent + 2
                        )
        return ' ' * indent + 'CLASS %s (%s:%d)\n%s\n%s\n' % (self.name, self.file, self.lineno, super_classes, _indent_multiline_string(self.docstring, indent))

    def has_traits(self):
        if self.abs_name in HAS_TRAITS_BASES:
            return True
        
        for base in self.bases:
            # each base is an ast.Name -- need to resolve it
            base_name = self._base_to_string(base)
            base_obj = self.resolve(base_name)

            if isinstance(base_obj, DocObject):
                # look for known base classes
                if base_obj.abs_name in HAS_TRAITS_BASES:
                    return True
                elif isinstance(base_obj, Class) and base_obj.has_traits():
                    return True
                elif not base_obj.is_concrete():
                    try:
                        if check_has_traits_import(base_obj.abs_name):
                            return True
                        else:
                            continue
                    except ImportError:
                        warnings.warn("%s could not be resolved -- referenced in %s:%d\n" % (base_obj.abs_name, self.file, self.lineno))

        # fall-back -- no traits
        return False

    def get_bases(self):
        result = [ self.resolve(self._base_to_string(base)) for base in self.bases ]
        result = [ base for base in result if base is not None ]

        return result

class Attribute(DocObject):
    """ documentable object definition """
    def __init__(self, name, file, lineno, parent_module, rhs_expr,
                 docstring = "", children = [ ]):
        DocObject.__init__(self, name, parent_module.abs_name + '.' + name,
                           file, lineno, parent_module, docstring, children)
        self.rhs_expr = rhs_expr

        # this needs to be set later, if at all
        self.rhs_text = ''

        # can set this later to save work
        self.known_trait = None
        
        #used for limitting recursive calls to is_trait
        self.traits_recursion_depth = 0

    def fromAST(options, filename, assign_node, module_object):
        """Create attribute object from AST assignment node

           - options : command line options
           - filename : file name of assignment code
           - assign_node : AST node for assignment statement
           - module_object : docobjects.Module instance for parent module
        """
        assert isinstance(assign_node, ast.Assign)

        # docstring left blank -- fill in by scanning comments!
        return Attribute(assign_node.nodes[0].name, filename,
                         assign_node.lineno, module_object,
                         assign_node.expr)

    fromAST = staticmethod(fromAST)

    def print_node(self, indent):
        return ' ' * indent + 'ATTRIBUTE %s (%s:%d)\n%s\n' % (self.name, self.file, self.lineno, _indent_multiline_string(self.docstring, indent))

    def is_trait(self):
        """ returns True iff attribute is a trait """
        self.traits_recursion_depth += 1
        if self.known_trait: 
            self.traits_recursion_depth -= 1
            return True
        if self.known_trait == False: 
            self.traits_recursion_depth -= 1
            return False

        if isinstance(self.parent_module, Class):
            if not self.parent_module.has_traits():
                self.traits_recursion_depth -= 1
                return False
                
        # catch attributes that would cause a stack overflow
        if (self.traits_recursion_depth > 20):
            warnings.warn("max recursion depth, object may be self-referential: " + str(self))
            self.traits_recursion_depth -= 1
            return True

        # examine rhs of assignment for traits primitives
        if isinstance(self.rhs_expr, ast.CallFunc) and \
           isinstance(self.rhs_expr.node, ast.Name):
            called_name = self.rhs_expr.node.name
            called_obj = self.resolve(called_name)
            #print "\tValue: %s" % str(called_obj)

            # known traits primitive on RHS -- this is a trait
            if called_obj is not None and called_obj.abs_name in TRAITS_PRIMITIVES:
                self.known_trait = True
                self.traits_recursion_depth -= 1
                return True
            elif isinstance(called_obj, Attribute) and called_obj.is_trait():
                self.known_trait = True
                self.traits_recursion_depth -= 1
                return True

        elif isinstance(self.rhs_expr, ast.Name):
            name = self.rhs_expr.name

            if name == 'None':
                self.traits_recursion_depth -= 1
                return False

            # The proper context for resolving names is the containing module.
            # Doing this avoids problems with code like the following:
            # --
            # A = 1
            #
            # class Spam:
            #     A = A
            # --
            context = self
            while context is not None and not isinstance(context, Module):
                context = context.parent_module

            #print 'Resolving RHS of %s (%s:%d) : %s' % (self.name,
            #                                            self.file,
            #                                            self.lineno,
            #                                            name)
            attr_obj = context.resolve(name)

            if attr_obj is None:
                # unable to resolve RHS of assignment -- not a trait, so
                #  don't worry about it
                pass
            elif attr_obj.abs_name in TRAITS_PRIMITIVES:
                # built-in traits primitive
                self.known_trait = True
                self.traits_recursion_depth -= 1
                return True
            elif isinstance(attr_obj, Attribute) and attr_obj.is_trait():
                # references user-defined trait
                self.known_trait = True
                self.traits_recursion_depth -= 1
                return True
            elif not attr_obj.is_concrete():
                # opaque reference -- need to import!
                try:
                    if check_trait_import(attr_obj.abs_name):
                        self.known_trait = True
                        self.traits_recursion_depth -= 1
                        return True
                except ImportError:
                    warnings.warn("%s could not be resolved -- referenced in %s:%d\n" % (attr_obj.abs_name, self.file, self.lineno))
                #warnings.warn("%s not found\n" % attr_obj.abs_name)

        # At this point we know the attribute definition does not use a
        # traits primitive.  It could still be a trait, however, if there
        # is a trait with the same name defined in a base class.
        if isinstance(self.parent_module, Class):
            bases = self.parent_module.get_bases()

            # check each base to see if it has a trait with the same name
            for base in bases:
                base_attr = base.resolve(self.name)
                if isinstance(base_attr, Attribute) and base_attr.is_trait():
                    self.traits_recursion_depth -= 1
                    return True
            
        # fall-through condition -- not a trait
        self.known_trait = False
        self.traits_recursion_depth -= 1
        return False

def _order_hierarchy(klass_list, klass_to_children):
    if klass_list == [ ]:
        return [ ]
    else:
        # order hierarchy for subclasses of each class
        result = [ (klass.name, klass.abs_name, klass,
                    _order_hierarchy(list(klass_to_children[klass]),
                                     klass_to_children))
                   for klass in klass_list ]

        # sort by name
        alpha_sort(result)
        result = [ r[2:] for r in result ]

        return result

def build_class_hierarchy(module_list):
    """
    ::

      Returns ( [ top_class1, top_class2, ... ],
                { top_class1 : [ subclasses, ... ],
                  top_class2 : [ subclasses, ... ],
                  ...
                } )
    """

    result = [ ]

    klass_to_children = { }
    top_klasses = Set([])

    # find all classes in documented modules
    klasses = reduce(lambda x, y: x + y, [ list(mod.get_descendants(Class)) for
                                           mod in module_list ])

    for klass in klasses:
        # trace each class to top superclasses

        ancestor_stack = [ klass ]
        while len(ancestor_stack) > 0:
            # pull next ancestor off the stack
            ancestor = ancestor_stack.pop()
            assert ancestor is not None

            # make sure that this class is in our hierarchy database
            if not klass_to_children.has_key(ancestor):
                # if not in db yet, add entry
                klass_to_children[ancestor] = Set()

            if not ancestor.is_concrete():
                # can't trace opaque references -- top class by default!
                top_klasses.add(ancestor)
                continue

            if not isinstance(ancestor, Class) and not isinstance(ancestor, Attribute):
                # can't do anything with this (?)
                continue
            
            while isinstance(ancestor, Attribute):
                rhs = ancestor.rhs_expr
                if isinstance(rhs, ast.Name):
                    ancestor = ancestor.resolve(rhs.name)
                else:
                    break

            if not isinstance(ancestor, Class):
                warnings.warn("couldn't resolve %s to class (ancestor class of %s)\n" % (ancestor.abs_name, klass.abs_name))
                continue

            bases = ancestor.get_bases()
            if len(bases) == 0:
                # this is a top class, with no base classes
                top_klasses.add(ancestor)
                continue

            # add base classes of ancestor to the stack
            ancestor_stack.extend(bases)
            
            # link child classes from parents
            for base in bases:
                if not klass_to_children.has_key(base):
                    klass_to_children[base] = Set([ancestor])
                else:
                    klass_to_children[base].add(ancestor)
            
    result = _order_hierarchy(list(top_klasses), klass_to_children)

    return result
