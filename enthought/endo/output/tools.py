
###########################################################################
# File:    tools.py
# Project: docutils
# Date:    2005-07-11
# Author:  David Baer
#
# Description:
#  Utilities that are useful in generating output
#
###########################################################################

"Utilities that are useful in generating documentation"

import compiler.ast as ast
import sys
import re

sys.path.append('..')
import enthought.endo.docobjects as docobjects

def encode_entities(s):
    """ returns s, with <, >, and & replaced with proper XML entities """
    return s.replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;')

def _format_tuple_arg(a):
    result = [ ]
    for arg in a:
        if type(arg) == tuple:
            result.append(_format_tuple_arg(arg))
        else:
            result.append(arg)
    return '(' + ', '.join(result) + ')'

def format_params(argnames, defaults, context):
    """
    Format parameter list

     * argnames : list of argument names (from AST)
     * defaults : list of defaults (from AST)
     * context  : namespace.Namespace instance for linking names encountered

    Returns a string with parameters joined with commas
    """
    argstrs = [ ]
    specialargs = [ ]
    args = list(argnames)
    defs = list(defaults)

    if (context.kwargs) and (args is not None) and (len(args) >= 1):
        specialargs.append('**<span class=\"param-name\">%s</span>' % args.pop())
    if (context.varargs) and (args is not None) and (len(args) >= 1):
        specialargs.append('*<span class=\"param-name\">%s</span>' % args.pop())

    offset = len(args) - len(defs)
    for i in range(0, len(args)):
        names = args[i]
        if type(names) == tuple:
            names =  '<span class=\"param-name\">%s</span>' % _format_tuple_arg(names)
        if i >= offset:
            argstrs.append("<span class=\"param-name\">%s</span> = <span class=\"param-default\">%s</span>" % (names, unparse(defs[i - offset], context)))
        else:
            argstrs.append(names)
    if specialargs != []:
        specialargs.reverse()
        argstrs.extend(specialargs)

    return ', '.join(argstrs)

_INDENT_RE = re.compile('^[ \t]*')
def fix_indent(docstring):
    """Some docstrings are formatted like this one.

    This function removes the common indentation from all lines but the first.
    """
    # 1) Determine common indent for all lines following the first line.
    lines = docstring.split('\n')

    # don't modify empty docstrings
    if len(lines) == 0:
        return docstring

    lines[0] = _INDENT_RE.sub('', lines[0])

    indent_amount = [ ]
    for i in range(1, len(lines)):
        # don't count blank lines
        if lines[i].strip() != '':
            m = _INDENT_RE.search(lines[i])
            indent_text = m.group()

            # expand tabs to (up to) 4 spaces (avoiding much grief)
            indent_length = 0
            for j in range(0, len(indent_text)):
                if indent_text[j] == '\t':
                    indent_length += 4 - (indent_length % 4)
                else:
                    indent_length += 1
            lines[i] = _INDENT_RE.sub(' ' * indent_length, lines[i])

            indent_amount.append(indent_length)
    if len(indent_amount) == 0:
        min_indent = 0
    else:
        min_indent = min(indent_amount)

    # 2) Remove this indent.
    lines = [ lines[0] ] + [ line[min_indent:] for line in lines[1:] ]

    # 3) Put lines back together.
    docstring = '\n'.join(lines)

    return docstring

def _local_hierarchicalize_modules(module_list):
    """Generate module hierarchy from list

    ::

      returns ((top_module, [ (submodule1, [ submodule1_1, ...]),
                              (submodule2, [ ... ]), ... ]),
               number_of_modules_read_from_list)
    """
    # assumes module_list is already sorted in alphabetical order
    if len(module_list) == 0:
        return (None, 0)

    # read package name
    top_name = module_list[0].abs_name
    sub_modules = [ ]

    # scan for first index in list for which top_name is not the prefix
    i = 1
    while i < len(module_list) and \
          module_list[i].abs_name[:len(top_name) + 1] == top_name + '.':
        sub_hierarchy = _local_hierarchicalize_modules(module_list[i:])

        sub_modules.append(sub_hierarchy[0])

        step = sub_hierarchy[1]
        i += step

    return ((module_list[0], sub_modules), i)

def hierarchicalize_modules(module_list):
    """Generate module hierarchy from list

    ::

      returns [ (top_module1, [ (submodule1, [ submodule1_1, ...]),
                              (submodule2, [ ... ]), ... ]),
                (top_module2, [ ... ]),
              ]
    """
    module_list_length = len(module_list)
    num_modules = 0
    result = [ ]
    while num_modules < module_list_length:
#        hierarchy, num = _local_hierarchicalize_modules(module_list)
#        result.append(hierarchy)
#        num_modules += num
#        module_list = module_list[num:]

        top_mod = module_list[num_modules]
        #print "Inserting %s" % top_mod
        _insert_into(result, top_mod, 0)
        num_modules += 1

    return result



def _insert_into(hierarchy, module, level):
    """ Inserts a module into a hierarchy based on comparing the module names
    at *level* of the package hierarchy.

    Parameters
    ----------
    hierarchy : list of (DocObject, hierarchy) tuples
        The tree to insert into; either the list or the sub-hierarchy list can
        be empty.
    module : Module
        The module to insert
    level : integer
        The level of the package hierarchy at which to compare module names
    """
    mod_len = len(module.name_list)
    for root in hierarchy:
        root_mod = root[0]
        subs = root[1]
        if ((level < mod_len) and (level < len(root_mod.name_list))):
            if (module.name_list[level] == root_mod.name_list[level]):
                _insert_into(subs, module, level+1)
                return
        if ((root_mod.abs_name == module.abs_name) and (not root_mod.is_concrete())):
            # replace placeholder
            root_mod = module
            return
    # The module doesn't match any existing roots
    if mod_len > level+1:
        # need a placeholder at this level
        from enthought.endo.docobjects import _OpaqueRef
        base_name = '.'.join(module.name_list[:level+1])
        hierarchy.append( (_OpaqueRef.new_ref(base_name), []) )
        _insert_into(hierarchy, module, level)
        return
    elif mod_len == level+1:
        hierarchy.append((module, []))
        return

def object_link(obj):
    "return a URL linking to the documentation for obj"
    if not obj.is_concrete():
        return ''

    if isinstance(obj, docobjects.Module):
        # modules have their own page
        link = "%s.html" % obj.abs_name
    elif isinstance(obj, docobjects.Class):
        # so do classes
        return class_link(obj)
    else:
        # everything else is identified with an id= attr on its container's
        # page
        name_re = re.compile(r'\.' + obj.name + '$')
        module_name = name_re.sub('', obj.abs_name)
        link = "%s.html#%s" % (module_name, obj.name)

    return link

def class_link(obj):
    "return a URL linking to the class page for obj"
    return "%s.html" % obj.abs_name

def unparse(e, context = None, trait_mode = False):
    """Unparse an AST node to text

      * e is an AST expression
      * context (optional) is a namespace for resolving (+ linking) identifiers
      * trait_mode is True if resolved identifiers inside strings should be linked
    """
    if isinstance(e, ast.Add):
        result = '(%s + %s)' % (unparse(e.left, context, trait_mode), unparse(e.right, context, trait_mode))
    elif isinstance(e, ast.And):
        result = '(' + ' and '.join([ unparse(n, context, trait_mode) for n in e.nodes ]) + ')'
    elif isinstance(e, ast.AssAttr):
        result = '%s.%s' % (unparse(e.expr, context, trait_mode), unparse(e.attrname, context, trait_mode))
    elif isinstance(e, ast.AssList):
        result = '[' + ','.join([ unparse(n, context, trait_mode) for n in e.nodes ]) + ']'
    elif isinstance(e, ast.AssName):
        result = unparse(e.name, context, trait_mode)
    elif isinstance(e, ast.AssTuple):
        result = '(' + ','.join([ unparse(n, context, trait_mode) for n in e.nodes ]) + ')'
    elif isinstance(e, ast.Assert):
        result = 'assert %s' % unparse(e.test, context, trait_mode)
        if e.fail is not None:
            result += ', %s' % unparse(e.fail, context, trait_mode)
    elif isinstance(e, ast.Assign):
        result = ''.join([ '%s = ' % unparse(n, context, trait_mode) for n in e.nodes ]) + unparse(e.expr, context, trait_mode)
    elif isinstance(e, ast.AugAssign):
        result = unparse(e.node, context, trait_mode) + ' %s= ' % e.op + unparse(e.expr, context, trait_mode)
    elif isinstance(e, ast.Backquote):
        result = '`' + unparse(e.expr, context, trait_mode) + '`'
    elif isinstance(e, ast.Bitand):
        result = '(' + ' &amp; '.join([ unparse(n, context, trait_mode) for n in e.nodes ]) + ')'
    elif isinstance(e, ast.Bitor):
        result = '(' + ' | '.join([ unparse(n, context, trait_mode) for n in e.nodes ]) + ')'
    elif isinstance(e, ast.Bitxor):
        result = '(' + ' ^ '.join([ unparse(n, context, trait_mode) for n in e.nodes ]) + ')'
    elif isinstance(e, ast.Break):
        result = 'break'
    elif isinstance(e, ast.CallFunc):
        result = unparse(e.node, context, trait_mode) + '(' + ', '.join([ unparse(a, context, trait_mode)
                                                          for a in e.args ])
        if e.star_args:
            result += ', *%s' % unparse(e.star_args, context, trait_mode)
        if e.dstar_args:
            result += ', **%s' % unparse(e.dstar_args, context, trait_mode)
        result += ')'
    elif isinstance(e, ast.Class):
        result = '&lt;&lt;class %s(%s)&gt;&gt;' % (unparse(e.name, context, trait_mode), ', '.join([ unparse(b, context, trait_mode) for b in e.bases ]))
    elif isinstance(e, ast.Compare):
        result = unparse(e.expr, context, trait_mode) + ' '.join([ '%s %s' % (unparse(o[0], context, trait_mode), unparse(o[1], context, trait_mode)) for o in e.ops ])
    elif isinstance(e, ast.Const):
        if isinstance(e.value, basestring):
            # if string contains newlines, format it prettily
            if e.value.find('\n') != -1:
                if e.value.find('"""') == -1:
                    result = '"""' + encode_entities(e.value) + '"""'
                else:
                    result = "'''" + encode_entities(e.value) + "'''"
            else:
                # for trait definitions, we may want to link to identifiers
                # that are inside strings
                if trait_mode and context is not None:
                    c = context
                    while not isinstance(c, docobjects.Module):
                        c = c.parent_module

                    target = c.resolve(e.value)
                    if target is not None and target.is_concrete():
                        if isinstance(target, docobjects.Class):
                            link = class_link(target)
                        else:
                            link = object_link(target)
                        result = '<a href="%s">%s</a>' % (link, repr(e.value))
                    else:
                        result = encode_entities(repr(e.value))
                else:
                    result = encode_entities(repr(e.value))
        else:
            result = encode_entities(repr(e.value))
    elif isinstance(e, ast.Continue):
        result = 'continue'
    elif isinstance(e, ast.Dict):
        result = '{ ' + ', '.join([ "%s : %s" % (key, value) for key, value in e.items ]) + ' }'
    elif isinstance(e, ast.Discard):
        result = unparse(e.expr, context, trait_mode)
    elif isinstance(e, ast.Div):
        result = '(%s / %s)' % (unparse(e.left, context, trait_mode), unparse(e.right, context, trait_mode))
    elif isinstance(e, ast.Ellipsis):
        result = '...'
    elif isinstance(e, ast.Exec):
        result = 'exec ' + unparse(e.expr, context, trait_mode)
        if e.locals:
            result += ', ' + unparse(e.locals, context, trait_mode)
        if e.globals:
            result += ', ' + unparse(e.globals, context, trait_mode)
    elif isinstance(e, ast.For):
        result = '[[for]]'
    elif isinstance(e, ast.From):
        result = '[[from ... import]]'
    elif isinstance(e, ast.Function):
        result = '[[function %s]]' % e.name
    elif isinstance(e, ast.Getattr):
        result = '%s.%s' % (unparse(e.expr, context, trait_mode), e.attrname)
    elif isinstance(e, ast.Global):
        result = 'global ' + ', '.join(e.names)
    elif isinstance(e, ast.If):
        result = '[[if]]'
    elif isinstance(e, ast.Import):
        result = '[[import]]'
    elif isinstance(e, ast.Invert):
        result = '~(%s)' % unparse(e.expr, context, trait_mode)
    elif isinstance(e, ast.Keyword):
        result = '%s = %s' % (e.name, unparse(e.expr, context, trait_mode))
    elif isinstance(e, ast.Lambda):
        result = 'lambda '
        params = [ ]
        for i in range(0, len(e.argnames)):
            param = unparse(e.argnames[i], context, trait_mode)
            if i < len(e.defaults):
                param += ' = %s' % unparse(e.defaults[i], context, trait_mode)
            params.append(param)
        result += ', '.join(params)
        result += ': %s' % unparse(e.code, context, trait_mode)
    elif isinstance(e, ast.LeftShift):
        result = '(%s &lt;&lt; %s)' % (unparse(e.left, context, trait_mode), unparse(e.right, context, trait_mode))
    elif isinstance(e, ast.List):
        result = '[ ' + ', '.join([ unparse(n, context, trait_mode) for n in e.nodes ]) + ' ]'
    elif isinstance(e, ast.ListComp):
        result = '[ %s ' + ' '.join([ unparse(q, context, trait_mode) for q in e.quals ]) + ' ]'
    elif isinstance(e, ast.ListCompFor):
        result = 'for %s in %s%s' % (unparse(e.assign, context, trait_mode),
                                     unparse(e.list, context, trait_mode),
                                     ''.join([ ' %s' % unparse(i, context, trait_mode)
                                               for i in e.ifs ]))
    elif isinstance(e, ast.ListCompIf):
        result = 'if ' + unparse(e.test, context, trait_mode)
    elif isinstance(e, ast.Mod):
        result = '(%s mod %s)' % (unparse(e.left, context, trait_mode), unparse(e.right, context, trait_mode))
    elif isinstance(e, ast.Module):
        result = '[[module]]'
    elif isinstance(e, ast.Mul):
        result = '(%s * %s)' % (unparse(e.left, context, trait_mode), unparse(e.right, context, trait_mode))
    elif isinstance(e, ast.Name):
        if context is not None:
            c = context
            while not isinstance(c, docobjects.Module):
                c = c.parent_module

            target = c.resolve(e.name)
            if target is not None and target.is_concrete():
                if isinstance(target, docobjects.Class):
                    link = class_link(target)
                else:
                    link = object_link(target)
                result = '<a href="%s">%s</a>' % (link, e.name)
            else:
                result = e.name
        else:
            result = e.name
    elif isinstance(e, ast.Not):
        result = 'not(%s)' % unparse(e.expr, context, trait_mode)
    elif isinstance(e, ast.Or):
        result = '(' + ' or '.join([ unparse(n, context, trait_mode) for n in e.nodes ]) + ')'
    elif isinstance(e, ast.Pass):
        result = 'pass'
    elif isinstance(e, ast.Power):
        result = '(%s ** %s)' % (unparse(e.left, context, trait_mode), unparse(e.right, context, trait_mode))
    elif isinstance(e, ast.Print):
        result = '[[print]]'
    elif isinstance(e, ast.Printnl):
        result = '[[printnl]]'
    elif isinstance(e, ast.Raise):
        result = '[[raise]]'
    elif isinstance(e, ast.Return):
        result = 'return %s' % unparse(e.value, context, trait_mode)
    elif isinstance(e, ast.RightShift):
        result = '(%s &gt;&gt; %s)' % (unparse(e.left, context, trait_mode), unparse(e.right, context, trait_mode))
    elif isinstance(e, ast.Slice):
        result = '%s[' % unparse(e.expr, context, trait_mode)
        if e.lower: result += unparse(e.lower, context, trait_mode)
        result += ':'
        if e.upper: result += unparse(e.upper, context, trait_mode)
    elif isinstance(e, ast.Sliceobj):
        result = ':'.join([ unparse(n, context, trait_mode) for n in e.nodes ])
    elif isinstance(e, ast.Stmt):
        result = '[[stmt]]'
    elif isinstance(e, ast.Sub):
        result = '(%s - %s)' % (unparse(e.left, context, trait_mode), unparse(e.right, context, trait_mode))
    elif isinstance(e, ast.Subscript):
        result = unparse(e.expr, context, trait_mode) + ''.join([ '[%s]' % unparse(s, context, trait_mode) for s in e.subs ])
    elif isinstance(e, ast.TryExcept):
        result = '[[try-except]]'
    elif isinstance(e, ast.TryFinally):
        result = '[[try-finally]]'
    elif isinstance(e, ast.Tuple):
        result = '(' + ', '.join([ unparse(n, context, trait_mode) for n in e.nodes ]) + ')'
    elif isinstance(e, ast.UnaryAdd):
        result = '+%s' % e.expr
    elif isinstance(e, ast.UnarySub):
        result = '-%s' % e.expr
    elif isinstance(e, ast.While):
        result = '[[while]]'
    elif isinstance(e, ast.Yield):
        result = 'yield %s' % unparse(e.value, context, trait_mode)
    elif isinstance(e, basestring):
        result = e
    else:
        result = '???'

    return result

